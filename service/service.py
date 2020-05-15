#!/usr/bin/env python3

from flask import Flask, Response, request
import requests
from sesamutils.flask import serve
from sesamutils import VariablesConfig
from sesamutils import sesam_logger
import sys
import json
import re

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
if config.AUTH_TYPE == "basic":
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
        url_obj = requests.get(url, auth=auth)
        data = json.loads(url_obj.text.encode("utf8"))

        # FIXME: handle single entities
        entities = data["d"].get("results") or data.get("d")
        if not entities:
            break

        for value in entities:
            if not first:
                yield ','
            else:
                first = False

            # if '@odata.id' in value:
            #     id_val = re.search(r'\((.*?)\)', value['@odata.id']).group(1).replace("'", "")
            #     value['_id'] = id_val

            if since_enabled:
                value['_updated'] = value[since_property]

            yield json.dumps(value)

        url = data["d"].get("__next")

    yield ']'


if __name__ == "__main__":
    serve(app)
