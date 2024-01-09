import asyncio
import logging
import threading
from types import TracebackType
from typing import Optional

from fastapi import HTTPException, Request, status
from getstanza.client import StanzaClient
from getstanza.guard import GuardedStatus

# TODO: How do we pass baggage to all outgoing calls?

# TODO: How do we get baggage from the FastAPI request object?

# TODO: Check if errors can be returned from FastAPI without exceptions, and if
# so then consider checking for that case and emitting a fail in that scenario.

# TODO: Make sure that the synchronous context manager doesn't mess with token
# caching and consumption when the first guard that gets called is a
# synchronous guard. We made it threadsafe, but background tasks might get
# started on the wrong loop.
#
# === CONFIRMED ISSUE AS SUSPECTED ===
#
# Idea: Have a way to communicate with the loop on the main thread and schedule
# it on that one instead of getting the current loop on the current thread when
# starting the background workers.
#
# Alternate Idea: Start the background worker early before the first guard is
# initialized. This should not incur any measurable or meaningful runtime cost.

# TODO: We may need to handle 429 errors differently. For example, if the
# server is using a custom data envelope format for the error, we want to be
# able to use theirs instead of hardcoding it into the application.


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

    def __enter__(self):
        logging.debug(
            "=== Sync ENTER for guard '%s' on thread '%s' ===",
            self.__guard_name,
            threading.get_ident(),
        )
        event_loop = None
        try:
            event_loop = asyncio.get_running_loop()
        except RuntimeError:
            pass  # This is fine and means that no loop is running.

        if event_loop is not None:
            raise RuntimeError(
                "A StanzaGuard context manager cannot be used synchronously in "
                "an asynchronous context. Please use as follows:\n\n"
                "'async with StanzaGuard(request, guard_name, ...)'"
            )

        asyncio.run(self.__execute_guard())

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ):
        logging.debug(
            "=== Sync EXIT for guard '%s' on thread '%s' ===",
            self.__guard_name,
            threading.get_ident(),
        )
        exit_status = self.__guard.success if exc_val is None else self.__guard.failure
        message = str(exc_val) if exc_val else None

        return self.__end_guard(exit_status, message)

    async def __aenter__(self):
        logging.debug(
            "=== Async ENTER for guard '%s' on thread '%s' ===",
            self.__guard_name,
            threading.get_ident(),
        )
        return await self.__execute_guard()

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ):
        logging.debug(
            "=== Async EXIT for guard '%s' on thread '%s' ===",
            self.__guard_name,
            threading.get_ident(),
        )
        exit_status = self.__guard.success if exc_val is None else self.__guard.failure
        message = str(exc_val) if exc_val else None

        return self.__end_guard(exit_status, message)

    async def __execute_guard(self):
        """
        Runs the guard this context manager was made for. If the guard blocks
        then an HTTPException with HTTP code 429 will be raised.
        """

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

    def __end_guard(self, exit_status: GuardedStatus, message: Optional[str]):
        """End the guard and collect metrics so that can be communicated."""

        if message:
            logging.debug("Exiting with status '%s': %s", exit_status.name, message)
        else:
            logging.debug("Exiting with status '%s'", exit_status.name)

        self.__guard.end(exit_status)
