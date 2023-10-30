"""Example of adding Stanza fault tolerance guards to a FastAPI application."""

import logging

import requests
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

# FastAPI Example Service
NAME = "fastapi-example"
RELEASE = "0.0.1"
ENV = "dev"
DEBUG = True

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
