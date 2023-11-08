import json
from typing import Any, Mapping

import requests


class HubError(Exception):
    """Generic HubError that is a base class of all Hub error exceptions."""

    def __init__(self, code: int, message: str, details: Mapping[str, Any]) -> None:
        super().__init__(message)

        self.code = code
        self.details = details

        print(message)


def hub_error(error: requests.exceptions.HTTPError):
    """Construct a Hub error exception associated with the response code."""

    response = json.loads(error.response.text)

    # TODO: Throw different errors based off of the code that we get?
    return HubError(response["code"], response["message"], response.get("details", {}))
