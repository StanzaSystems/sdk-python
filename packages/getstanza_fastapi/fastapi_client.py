import asyncio
import inspect
from functools import WRAPPER_ASSIGNMENTS
from typing import Optional

from fastapi import Request
from getstanza.client import StanzaClient
from getstanza.configuration import StanzaConfiguration
from getstanza_fastapi.fastapi_guard import StanzaGuard

# TODO: Check for weird background worker / thread id behavior when wrapping
# synchronous handlers with the async decorator. If it's an issue for some
# reason, then make a separate synchronous decorator. Otherwise just leave it
# as it is.


class StanzaFastAPIClient(StanzaClient):
    """
    SDK client that assists with integrating FastAPI services with Stanza Hub,
    and managing the active service and guard configurations.
    """

    def __init__(self, config: StanzaConfiguration):
        super().__init__(config)

    def stanza_guard(
        self,
        guard_name: str,
        feature_name: Optional[str] = None,
        priority_boost: Optional[int] = None,
        tags=None,
    ):
        """Wrap your FastAPI handler with a Stanza guard."""

        def decorator(wrapped):
            wrapped_parameters = inspect.signature(wrapped).parameters.values()

            # We need to make sure that an argument with type 'fastapi.Request'
            # is passed into the handler so that FastAPI gives us request
            # information needed to propagate baggage. If the handler we're
            # wrapping doesn't inject it, then return a wrapper that asks for
            # it.
            wrapper = (
                self.__wrapper_without_request(
                    wrapped,
                    guard_name,
                    feature_name=feature_name,
                    priority_boost=priority_boost,
                    tags=tags,
                )
                if any(p.annotation == Request for p in wrapped_parameters)
                else self.__wrapper_with_request(
                    wrapped,
                    guard_name,
                    feature_name=feature_name,
                    priority_boost=priority_boost,
                    tags=tags,
                )
            )

            # Merge the calling signatures of our decorator with the signature
            # of the handler being passed into it so FastAPI injects the needed
            # dependencies needed by us and also whatever the handler itself
            # needs.
            #
            # The only potential conflicting field is a positional argument
            # with the 'fastapi.Request' type (name and exact position doesn't
            # matter to FastAPI, just the type). That's handled by choosing the
            # wrapper based on whether it's provided by the handler or not.
            wrapper.__signature__ = inspect.Signature(
                parameters=[
                    # Use parameters from the wrapper, save for *args and
                    # **kwargs. These need to come first to ensure any query
                    # parameters with defaults in-use by the handler come after
                    # any positional arguments that we add.
                    *filter(
                        lambda p: p.kind
                        not in (
                            inspect.Parameter.VAR_POSITIONAL,
                            inspect.Parameter.VAR_KEYWORD,
                        ),
                        inspect.signature(wrapper).parameters.values(),
                    ),
                    # Use all parameters from the handler that we're wrapping.
                    *wrapped_parameters,
                ],
                return_annotation=inspect.signature(wrapped).return_annotation,
            )

            # Borrowed from functools, this copies over attributes from the
            # wrapped function into the wrapper such as name and docs so that
            # the wrapper looks like the wrapped function.
            for attr in WRAPPER_ASSIGNMENTS:
                try:
                    value = getattr(wrapped, attr)
                except AttributeError:
                    pass
                else:
                    setattr(wrapper, attr, value)

            return wrapper

        return decorator

    def __wrapper_with_request(
        self,
        wrapped,
        guard_name: str,
        feature_name: Optional[str] = None,
        priority_boost: Optional[int] = None,
        tags=None,
    ):
        async def wrapper(request: Request, *args, **kwargs):
            async with StanzaGuard(
                request,
                guard_name,
                feature_name=feature_name,
                priority_boost=priority_boost,
                tags=tags,
            ):
                return (
                    await result
                    if asyncio.iscoroutine(result := wrapped(*args, **kwargs))
                    else result
                )

        return wrapper

    def __wrapper_without_request(
        self,
        wrapped,
        guard_name: str,
        feature_name: Optional[str] = None,
        priority_boost: Optional[int] = None,
        tags=None,
    ):
        async def wrapper(*args, **kwargs):
            request = None
            for key, value in kwargs.items():
                if isinstance(value, Request):
                    request = kwargs[key]
                    break

            # This should never happen in practice in runtime. This check exists
            # just to make the type checker happy.
            if request is None:
                raise AttributeError(
                    "Stanza cannot find argument with type 'fastapi.Request' in "
                    "the request handler arguments."
                )

            async with StanzaGuard(
                request,
                guard_name,
                feature_name=feature_name,
                priority_boost=priority_boost,
                tags=tags,
            ):
                return (
                    await result
                    if asyncio.iscoroutine(result := wrapped(*args, **kwargs))
                    else result
                )

        return wrapper
