#!/usr/bin/env python3

from flask import Flask, Response, request
import requests
from sesamutils.flask import serve
from sesamutils import VariablesConfig
from sesamutils import sesam_logger
import sys
import json
import time

# set env.vars
required_env_vars = ["SERVICE_URL", "USERNAME", "PASSWORD"]
optional_env_vars = ["LOG_LEVEL", ("AUTH_TYPE", "basic")]

config = VariablesConfig(required_env_vars, optional_env_vars=optional_env_vars)

# set logging
logger = sesam_logger("sap-odata-source")

# check that all required env.vars are supplied
if not config.validate():
    sys.exit(1)

# authentication
auth = None
if config.AUTH_TYPE.lower() == "basic":
    auth = (config.USERNAME, config.PASSWORD)
else:
    logger.error(f"Unsupported authentication type: {config.AUTH_TYPE}")
    sys.exit(1)

# start the service
app = Flask(__name__)


@app.route("/<entity_set>", methods=["GET"])
def get_entity_set(entity_set):
    """service entry point"""

    format = request.args.get("$format") if request.args.get("$format") is not None else "json"
    expand = request.args.get("$expand")

    full_url = config.SERVICE_URL + entity_set + f"?$format={format}"

    if expand:
        full_url += f"&$expand={expand}"

    since_enabled = request.args.get('since') is not None
    since_property = None

    if since_enabled:
        since_property = request.args.get('since')
        query = "&$filter=" + since_property + "%20gt%20DateTime'" + request.args.get("since")
        full_url += query

    return Response(process_request(url=full_url, since_enabled=since_enabled, since_property=since_property),
                    mimetype='application/json')


def process_request(url, since_enabled, since_property):
    """fetch entities from given Odata url and dumps back to client as JSON stream"""

    first = True
    yield '['

    while url:
        logger.debug(f"Request url: {url}")
        response = requests.get(url, auth=auth)
        data = json.loads(response.text.encode("utf8"))
        # data = response.json() ?

        # FIXME: handle single entities
        entities = data["d"].get("results") or data.get("d")
        if not entities:
            break

        for entity in entities:
            if not first:
                yield ','
            else:
                first = False

            for key in entity:

                logger.debug(f"key: {key}")
                logger.debug(f"value: {entity[key]}")

                value = entity[key]

                if value and "/Date(" in value:
                    local_iso_date = sap_epoch_to_iso_date(value)
                    logger.debug(f"{key}: {local_iso_date}")
                    entity[key] = local_iso_date

            if since_enabled:
                entity['_updated'] = entity[since_property]

            yield json.dumps(entity)

        url = data["d"].get("__next")

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
