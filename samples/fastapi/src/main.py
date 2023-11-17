"""Example of adding Stanza fault tolerance guards to a FastAPI application."""

import logging
import sys

import requests
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from getstanza.client import StanzaClient
from getstanza.configuration import StanzaConfiguration

# FastAPI Example Service
NAME = "fastapi-example"
RELEASE = "0.0.1"
ENV = "dev"
DEBUG = True

if DEBUG:
    logging.basicConfig(level=logging.DEBUG)

# Log basic service details at startup
logging.info("service init, name:%s, release:%s, env:%s", NAME, RELEASE, ENV)


# Init Stanza fault tolerance library
try:
    config = StanzaConfiguration(
        # api_key="YOUR-API-KEY-HERE",  # or via STANZA_API_KEY environment variable
        service_name=NAME,  # or via STANZA_SERVICE_NAME environment variable
        service_release=RELEASE,  # or via STANZA_SERVICE_RELEASE environment variable
        environment=ENV,  # or via STANZA_ENVIRONMENT environment variable
    )
    stanza_client = StanzaClient(config)
    stanza_client.init()
except ValueError as exc:
    logging.exception(exc)
    sys.exit(1)

# Alternate popular python HTTP frameworks:
# - AIOHTTP
# - Flask
# - Django
app = FastAPI(title=NAME, version=RELEASE, debug=DEBUG)


@app.get("/healthz")
def health():
    """Returns OK if server is healthy"""
    return "OK"


@app.get("/quote", response_class=PlainTextResponse)
async def quote():
    """Returns a random quote from ZenQuotes using Requests"""

    # stz = await stanza.Guard(stanza.ContextWithHeaders, "QuoteGuard")

    try:
        resp = requests.get("https://zenquotes.io/api/random", timeout=10)
    except (ConnectionError, TimeoutError) as err:
        logging.error(err)
        return ""

    if resp.status_code != requests.codes["ok"]:
        logging.error("Error: %s %s", resp.status_code, resp.text)
        return ""

    try:
        data = resp.json()
    except requests.exceptions.JSONDecodeError as err:
        logging.error("Error: %s %s", resp.status_code, err.strerror)
        return ""

    return "‟" + data[0]["q"] + "” -" + data[0]["a"] + "\n"
