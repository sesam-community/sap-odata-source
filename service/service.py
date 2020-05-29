#!/usr/bin/env python3

from flask import Flask, Response, request, abort
from sesamutils.flask import serve
from sesamutils import sesam_logger
from sesamutils import VariablesConfig
import json
import requests
import sys
import time

# Set env.vars
required_env_vars = ["SERVICE_URL", "USERNAME", "PASSWORD"]
optional_env_vars = ["LOG_LEVEL", ("AUTH_TYPE", "basic")]

env_vars = VariablesConfig(required_env_vars, optional_env_vars=optional_env_vars)

# Set logging
logger = sesam_logger("sap-odata-source")

# Check that all required env.vars are supplied
if not env_vars.validate():
    sys.exit(1)

# Authentication
auth = None
if env_vars.AUTH_TYPE.lower() == "basic":
    auth = (env_vars.USERNAME, env_vars.PASSWORD)
else:
    logger.error(f"Unsupported authentication type: {env_vars.AUTH_TYPE}")
    sys.exit(1)

# Start the service
app = Flask(__name__)


@app.route("/<entity_set>", methods=["GET"])
def get_entity_set(entity_set):
    """service entry point"""

    format = request.args.get("$format") or "json"
    expand = request.args.get("$expand")
    since_property = request.args.get("since_property") or "lastModifiedDateTime"
    since_enabled = request.args.get("since") is not None

    full_url = f"{env_vars.SERVICE_URL}{entity_set}?$format={format}"

    if expand:
        full_url += f"&$expand={expand}"

    if since_enabled and since_property:
        since = request.args.get("since")
        full_url += f"&$filter={since_property} gt '{since}'"

    return Response(process_request(url=full_url, since_enabled=since_enabled, since_property=since_property),
                    mimetype="application/json")


def process_request(url, since_enabled, since_property):
    """fetch entities from given Odata url and dumps back to client as JSON stream"""

    logger.debug(f"since_enabled: {since_enabled}")
    logger.debug(f"since_property: {since_property}")

    yield '['
    first = True
    count = 0  # number of entities

    while url:
        logger.info(f"Request url: {url}")
        response = requests.get(url, auth=auth)

        if not response.ok:
            abort(response.status_code)

        data = response.json()
        entities = None

        # Entities of interest are either returned as { "d": { <entities> } }
        # or as { "d": { "results": [<entities>] } }

        # Try to fetch entities from "results" first
        if "results" in data.get("d"):
            entities = data["d"].get("results")

        # Then try to fetch from "d"
        if entities is None:  # explicitly check on None to not overwrite empty "results" list
            entities = data.get("d")

        # Stop if there are no entities to process
        if not entities:
            break

        # Make single entity a list so that the for-loop below can be used regardless
        if not isinstance(entities, type(list())):
            entities = [entities]

        for entity in entities:

            if not first:
                yield ','
            else:
                first = False

            # Convert dates one level deep
            for key in entity:

                value = entity.get(key)

                # Dates are represented as strings in SAP so all non-string values can be skipped
                if not isinstance(value, str):
                    continue

                if value and "/Date(" in value:
                    iso_date = sap_epoch_to_iso_date(value)
                    # logger.debug(f"{key}: {value} --> {iso_date}")
                    entity[key] = iso_date

            # entity["_updated"] = entity.get(since_property)
            # entity["_updated"] = time.gmtime('%Y-%m-%dT%H:%M:%S')  # set current GMT time
            entity["_updated"] = time.strftime('%Y-%m-%dT%H:%M:%S')  # set current local time

            count += 1
            yield json.dumps(entity)

        url = data["d"].get("__next")

    logger.info(f"Fetched {count} entities")
    yield ']'


def sap_epoch_to_iso_date(sap_epoch):
    """ Convert SAP date string in UTC milliseconds to local ISO date """

    epoch_string = str(sap_epoch).replace("/Date(", "").replace(")/", "")  # isolate epoch time
    epoch_ms = epoch_string.replace("+0000", "")  # epoch in ms (UTC)
    epoch_timestamp = int(epoch_ms) / 1000  # epoch in seconds (UTC)
    dt = time.localtime(epoch_timestamp)  # local time
    # dt = time.gmtime(epoch_timestamp)  # GMT time
    dt_formatted = time.strftime('%Y-%m-%dT%H:%M:%S', dt)  # ISO formatted

    return dt_formatted


if __name__ == "__main__":
    serve(app)
