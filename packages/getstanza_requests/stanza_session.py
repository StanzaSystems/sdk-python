"""Extends python-request's Session to integrate with Stanza."""

import asyncio
import logging

from getstanza.client import StanzaClient
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

        # TODO: Double check the specification that letting the request through
        # if not initialized yet is okay.

        if self.__client.hub is not None:
            future = asyncio.run_coroutine_threadsafe(
                self.__client.guard(
                    guard_name=self.__guard_name,
                    feature=None,
                    priority_boost=None,
                    default_weight=None,
                    tags=None,
                ),
                self.__client.hub.event_loop,
            )
            future.result()

        logging.debug("XXX: Making outgoing HTTP request as guard future resolved")

        return super().request(*args, **kwargs)
