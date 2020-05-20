#!/usr/bin/env python3

from flask import Flask, Response, request, abort
import requests
from sesamutils.flask import serve
from sesamutils import VariablesConfig
from sesamutils import sesam_logger
import sys
import json
import time

# set env.vars
required_env_vars = ["SERVICE_URL", "USERNAME", "PASSWORD"]
optional_env_vars = ["LOG_LEVEL", ("AUTH_TYPE", "basic"), "SINCE_PROPERTY"]

env_vars = VariablesConfig(required_env_vars, optional_env_vars=optional_env_vars)

# set logging
logger = sesam_logger("sap-odata-source")

# check that all required env.vars are supplied
if not env_vars.validate():
    sys.exit(1)

# authentication
auth = None
if env_vars.AUTH_TYPE.lower() == "basic":
    auth = (env_vars.USERNAME, env_vars.PASSWORD)
else:
    logger.error(f"Unsupported authentication type: {env_vars.AUTH_TYPE}")
    sys.exit(1)

# start the service
app = Flask(__name__)


@app.route("/<entity_set>", methods=["GET"])
def get_entity_set(entity_set):
    """service entry point"""

    format = request.args.get("$format") if request.args.get("$format") is not None else "json"
    expand = request.args.get("$expand")

    full_url = f"{env_vars.SERVICE_URL}{entity_set}?$format={format}"

    if expand:
        full_url += f"&$expand={expand}"

    since_enabled = request.args.get("since") is not None
    since_property = env_vars.SINCE_PROPERTY

    if since_enabled and since_property:
        since = request.args.get("since")
        full_url += f"&$filter={since_property} gt '{since}'"

    return Response(process_request(url=full_url, since_enabled=since_enabled, since_property=since_property),
                    mimetype="application/json")


def process_request(url, since_enabled, since_property):
    """fetch entities from given Odata url and dumps back to client as JSON stream"""

    yield '['
    first = True
    count = 0

    while url:
        logger.info(f"Request url: {url}")
        response = requests.get(url, auth=auth)

        if not response.ok:
            abort(response.status_code)

        data = response.json()

        entities = data["d"].get("results") or data.get("d")
        if not entities:
            break

        # Make single entity a list
        if type(entities) is not type([]):
            tmp = list()
            tmp.append(entities)
            entities = tmp

        for entity in entities:
            if not first:
                yield ','
            else:
                first = False

            # Convert dates one level deep
            for key in entity:

                # logger.debug(f"key: '{key}' value: '{entity[key]}'")
                value = entity[key]

                # Dates are represented as strings in SAP so we can skip all non-string values
                if type(value) is not type(""):
                    continue

                if value and "/Date(" in value:
                    local_iso_date = sap_epoch_to_iso_date(value)
                    # logger.debug(f"{key}: {value} --> {local_iso_date}")
                    entity[key] = local_iso_date

            if since_enabled:
                entity["_updated"] = entity[since_property]

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
    local_dt = time.localtime(epoch_timestamp)  # local timezone
    local_dt_formatted = time.strftime('%Y-%m-%dT%H:%M:%S%z', local_dt)  # ISO formatted

    return local_dt_formatted


if __name__ == "__main__":
    serve(app)
