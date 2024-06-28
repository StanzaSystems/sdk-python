"""Extends python-request's Session to integrate with Stanza."""

import asyncio
import logging
from typing import Dict, Optional

from getstanza.client import StanzaClient
from getstanza.guard import Guard
from getstanza.propagation import http_headers_from_context
from requests import PreparedRequest, Request, Response, Session
from requests.utils import check_header_validity


class StanzaSession(Session):
    """
    A subclass of python-requests Session that allows for easily wrapping
    outgoing HTTP requests with Stanza guards.
    """

    def __init__(
        self,
        guard_name: str,
        feature_name: Optional[str] = None,
        priority_boost: Optional[int] = None,
        default_weight: Optional[float] = None,
        tags: Optional[Dict[str, str]] = None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.__guard_name = guard_name
        self.__feature_name = feature_name
        self.__priority_boost = priority_boost
        self.__default_weight = default_weight
        self.__tags = tags

        self.__client = StanzaClient.getInstance()

    def prepare_request(self, request: Request) -> PreparedRequest:
        """Constructs a PreparedRequest with additional baggage headers."""

        outgoing_headers = http_headers_from_context()
        for header in outgoing_headers.items():
            check_header_validity(header)

        request.headers = request.headers | outgoing_headers

        return super().prepare_request(request)

    def request(self, *args, **kwargs) -> Response:
        """Calls 'request' along with additional baggage and guard checks."""

        if self.__client.hub is not None:
            # Initialize and run the guard. It's important that initialize on
            # the current thread so that the incoming baggage can be read from.
            guard = Guard(
                self.__client.hub,
                self.__guard_name,
                feature_name=self.__feature_name,
                priority_boost=self.__priority_boost,
                default_weight=self.__default_weight,
                tags=self.__tags,
            )
            asyncio.run_coroutine_threadsafe(
                guard.run(), self.__client.hub.event_loop
            ).result()

            # 🪵 Check for and log any returned error messages
            if guard.error:
                logging.error(guard.error)

            # 🚫 Stanza Guard has *blocked* this workflow log the error and
            # raise an HTTPException with a 429 response code.
            if guard.blocked():
                logging.error(guard.block_message, extra={"reason": guard.block_reason})
                return self.__make_response(guard)

        return super().request(*args, **kwargs)

    @staticmethod
    def __make_response(guard: Guard) -> Response:
        """Craft a fake python-requests response with a 429 error code."""

        def json(*args, **kwargs):
            return {
                "message": guard.block_message,
                "reason": guard.block_reason,
            }

        response = Response()
        response.status_code = 429
        response.headers["Content-Type"] = "application/json"
        response.json = json

        return response
