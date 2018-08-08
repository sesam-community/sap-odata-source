"""Odata connector for Sesam.io applications"""
import os
import logging
import urllib.request
from urllib.error import HTTPError
import json
import re

from flask import Flask, Response, abort, request

SERVICE_URL = os.environ.get("SERVICE_URL", "https://services.odata.org/V4/TripPinService/")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
DATASETS = json.loads(os.environ.get("datasets", '{}'))

logging.basicConfig(level=LOG_LEVEL)

if SERVICE_URL is None:
    logging.error("Odata service URL is required!")
    exit(1)

logging.info("got service url %s", str(SERVICE_URL))

APP = Flask(__name__)

EXPOSED_URLS = {}


def process_request(url, since_enabled, since_property):
    """fetch entities from given Odata url and dumps back to client as JSON stream"""
    first = True
    yield '['

    while True:
        logging.debug("Request url: %s", url)
        url_obj = urllib.request.urlopen(url)
        data = json.loads(url_obj.read().decode())

        for value in data['value']:
            if not first:
                yield ','
            else:
                first = False

            if '@odata.id' in value:
                id_val = re.search(r'\((.*?)\)', value['@odata.id']).group(1).replace("'", "")
                value['_id'] = id_val
            if since_enabled:
                value['_updated'] = value[since_property]
            yield json.dumps(value)

        if '@odata.nextLink' not in data:
            break

        url = data['@odata.nextLink']

    yield ']'


@APP.route("/<string:url>", methods=["GET"])
def fetch_data(url):
    """service entry point"""
    if not is_endpoint_allowed(url):
        logging.warning("Url %s not allowed", url)
        abort(500)

    logging.info("Serving request to endpoint %s", url)

    query = ""
    since_property = None
    since_enabled = request.args.get('since') is not None \
                    and url in DATASETS \
                    and "since" in DATASETS[url]

    if request.args.get('since') is not None and not since_enabled:
        logging.warning("Since provided but not found in config for url %s", url)

    if since_enabled:
        since_property = DATASETS[url]["since"];
        query = "?$filter=" + since_property + "%20gt%20DateTime'" + request.args.get('since')

    return Response(process_request(SERVICE_URL + url + query, since_enabled, since_property)
                    , mimetype='application/json')


def is_endpoint_allowed(url):
    """Check if given url is in allowed url's list
    return true if url is allowed and false otherwise"""
    return url in EXPOSED_URLS


def get_endpoint_set_from_url(service_url):
    """returns available EntitySet's for given url"""
    result_set = {}
    try:
        with urllib.request.urlopen(service_url) as url:
            data = json.loads(url.read().decode())
            items = data['value']
            for item in items:
                if "EntitySet".lower() != item['kind'].lower():
                    continue
                result_set[item['name']] = item['url']
            logging.info("found endpoints %s", str(result_set.keys()))
            return result_set
    except HTTPError as exc:
        logging.critical("Could not retrieve endpoints from URL %s exception: %s"
                         , service_url, str(exc))


if __name__ == '__main__':
    logging.info("Starting service")
    EXPOSED_URLS = get_endpoint_set_from_url(SERVICE_URL)

    APP.run(debug=True, host='0.0.0.0', threaded=True, port=os.environ.get('PORT', 5000))
