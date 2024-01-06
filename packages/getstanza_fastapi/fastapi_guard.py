import logging
from types import TracebackType
from typing import Optional

from fastapi import HTTPException, Request, status
from getstanza.client import StanzaClient

# TODO: How do we pass baggage to all outgoing calls?

# TODO: How do we get baggage from request headers in this context?


class StanzaGuard:
    """Helps wrap a FastAPI request handler with a guard.

    Implementation is derived from the contextlib.ContextDecorator with
    some additional modifications to support our use-case.
    """

    def __init__(
        self,
        request: Request,
        guard_name: str,
        feature_name: Optional[str] = None,
        priority_boost: Optional[int] = None,
        tags=None,
    ):
        self.__request = request
        self.__guard_name = guard_name
        self.__feature_name = feature_name
        self.__priority_boost = priority_boost
        self.__tags = tags
        self.__client = StanzaClient.getInstance()

    # TODO: Implement sync wrappers so context manager can be used sync.

    async def __aenter__(self):
        logging.debug(
            "Entering guard (name=%s, feature=%s, priority_boost=%s, tags=%r)",
            self.__guard_name,
            self.__feature_name,
            self.__priority_boost,
            self.__tags,
        )

        # TODO: Pass in baggage from 'self.__request' after OTEL support added.
        self.__guard = await self.__client.guard(
            self.__guard_name,
            feature=self.__feature_name,
            priority_boost=self.__priority_boost,
            tags=self.__tags,
        )

        # 🪵 Check for and log any returned error messages
        if self.__guard.error:
            logging.error(self.__guard.error)

        # 🚫 Stanza Guard has *blocked* this workflow log the error and raise
        # an HTTPException with a 429 response code.
        if self.__guard.blocked():
            logging.error(
                self.__guard.block_message,
                extra={"reason": self.__guard.block_reason},
            )
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "message": self.__guard.block_message,
                    "reason": self.__guard.block_reason,
                },
            )

        # ✅ Stanza Guard has *allowed* this workflow, business logic follows.
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ):
        # TODO: Check if errors can be returned from FastAPI without
        # exceptions, and if so then consider checking for that case and
        # emitting a fail in that scenario.

        exit_status = self.__guard.success if exc_val is None else self.__guard.failure
        logging.debug("Exiting with status '%s': %r", exit_status.name, exc_val)
        self.__guard.end(exit_status)
