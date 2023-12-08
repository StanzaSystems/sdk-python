"""Example of adding Stanza fault tolerance guards to a FastAPI application."""

import logging
import sys

import requests
from fastapi import FastAPI, HTTPException, status
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
    stanza_client = StanzaClient(
        StanzaConfiguration(
            # api_key="YOUR-API-KEY-HERE",  # or via STANZA_API_KEY environment variable
            service_name=NAME,  # or via STANZA_SERVICE_NAME environment variable
            service_release=RELEASE,  # or via STANZA_SERVICE_RELEASE environment variable
            environment=ENV,  # or via STANZA_ENVIRONMENT environment variable
        )
    )
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


@app.get("/quote")
async def quote():
    """Returns a random quote from ZenQuotes using Requests"""

    # 📛 Name the Stanza Guard which protects this workflow
    stz = await stanza_client.guard("FamousQuotes")

    # 🪵 Check for and log any returned error messages
    if stz.error():
        logging.error(stz.error())

    # 🚫 Stanza Guard has *blocked* this workflow log the error and raise an HTTPException
    if stz.blocked():
        logging.error(stz.block_message(), extra={"reason": stz.block_reason()})
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={"msg": stz.block_message(), "reason": stz.block_reason()},
        )

    # ✅ Stanza Guard has *allowed* this workflow, business logic goes here.
    try:
        resp = requests.get("https://zenquotes.io/api/random", timeout=10)
    except (ConnectionError, TimeoutError) as req_exc:
        stz.end(stz.failure)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=req_exc
        ) from req_exc

    # 🎉 Happy path, our "business logic" succeeded
    if resp.status_code is status.HTTP_200_OK:
        stz.end(stz.success)
        return resp.json()

    # 😭 Sad path, our "business logic" failed
    stz.end(stz.failure)
    raise HTTPException(status_code=resp.status_code, detail=resp.text)
