"""Example of adding Stanza fault tolerance guards to a FastAPI application."""

import logging
import sys

import requests
from fastapi import FastAPI, HTTPException, Request, status
from getstanza.configuration import StanzaConfiguration
from getstanza_fastapi.fastapi_client import StanzaFastAPIClient
from getstanza_fastapi.fastapi_guard import StanzaGuard

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
    stanza_client = StanzaFastAPIClient(
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
@stanza_client.stanza_guard("FamousQuotes")
async def quote():
    """Returns a random quote from ZenQuotes using Requests"""

    # ✅ Stanza Guard has *allowed* this workflow, business logic goes here.
    try:
        resp = requests.get("https://zenquotes.io/api/random", timeout=10)
    except (ConnectionError, TimeoutError) as req_exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=req_exc
        ) from req_exc

    # 🎉 Happy path, our "business logic" succeeded
    if resp.status_code is status.HTTP_200_OK:
        return resp.json()

    # 😭 Sad path, our "business logic" failed
    raise HTTPException(status_code=resp.status_code, detail=resp.text)


@app.get("/async_context_manager_quote")
async def async_context_manager_quote(request: Request):
    """Returns a random quote from ZenQuotes using Requests"""

    async with StanzaGuard(request, "FamousQuotes"):
        # ✅ Stanza Guard has *allowed* this workflow, business logic goes here.
        try:
            resp = requests.get("https://zenquotes.io/api/random", timeout=10)
        except (ConnectionError, TimeoutError) as req_exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=req_exc
            ) from req_exc

        # 🎉 Happy path, our "business logic" succeeded
        if resp.status_code is status.HTTP_200_OK:
            return resp.json()

        # 😭 Sad path, our "business logic" failed
        raise HTTPException(status_code=resp.status_code, detail=resp.text)


@app.get("/sync_context_manager_quote")
def sync_context_manager_quote(request: Request):
    """Returns OK if server is healthy"""

    with StanzaGuard(request, "FamousQuotes"):
        # ✅ Stanza Guard has *allowed* this workflow, business logic goes here.
        try:
            resp = requests.get("https://zenquotes.io/api/random", timeout=10)
        except (ConnectionError, TimeoutError) as req_exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=req_exc
            ) from req_exc

        # 🎉 Happy path, our "business logic" succeeded
        if resp.status_code is status.HTTP_200_OK:
            return resp.json()

        # 😭 Sad path, our "business logic" failed
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
