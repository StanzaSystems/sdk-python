"""Extends python-request's Session to integrate with Stanza."""

import asyncio
import logging

from getstanza.client import StanzaClient
from getstanza.guard import Guard
from getstanza.propagation import StanzaContext
from requests import PreparedRequest, Request, Response, Session


class StanzaSession(Session):
    """
    A subclass of python-requests Session that allows for easily wrapping
    outgoing HTTP requests with Stanza guards.
    """

    def __init__(self, guard_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__guard_name = guard_name
        self.__client = StanzaClient.getInstance()

    def prepare_request(self, request: Request) -> PreparedRequest:
        """Constructs a PreparedRequest with additional baggage headers."""

        # TODO: Add headers to 'request' to add baggage here.

        return super().prepare_request(request)

    def request(self, *args, **kwargs) -> Response:
        """Calls 'request' along with additional baggage and guard checks."""

        StanzaContext.get()

        # TODO: We need to confirm this in both async and sync contexts.

        event_loop = None
        try:
            event_loop = asyncio.get_running_loop()
        except RuntimeError:
            pass  # This is fine and means that no loop is running.
        finally:
            logging.debug(
                "XXX: Event loop result while calling 'request': %r", event_loop
            )

        # TODO: Pass in feature and boost from baggage to guard constructor.

        logging.debug("XXX: HUB %r", self.__client.hub)

        if self.__client.hub is not None:
            logging.debug("XXX: RUNNING GUARD")

            # Initialize and run the guard. It's important that initialize on
            # the current thread so that the incoming baggage can be read from.
            guard = Guard(
                self.__client.hub,
                self.__guard_name,
                feature_name=None,
                priority_boost=None,
                default_weight=None,
                tags=None,
            )
            asyncio.run_coroutine_threadsafe(
                guard.run(), self.__client.hub.event_loop
            ).result()

            # 🪵 Check for and log any returned error messages
            if guard.error:
                logging.debug("XXX: Guard ERROR")
                logging.error(guard.error)

            # 🚫 Stanza Guard has *blocked* this workflow log the error and
            # raise an HTTPException with a 429 response code.
            if guard.blocked():
                logging.debug("XXX: Guard BLOCKED")
                logging.error(guard.block_message, extra={"reason": guard.block_reason})
                return self.__make_response(guard)

            logging.debug("XXX: Making outgoing HTTP request as guard future resolved")

        return super().request(*args, **kwargs)

    def __make_response(self, guard: Guard) -> Response:
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
