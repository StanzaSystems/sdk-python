import inspect

from fastapi import Request
from getstanza.client import StanzaClient
from getstanza.configuration import StanzaConfiguration
from getstanza_fastapi.fastapi_guard import StanzaGuard


class StanzaFastAPIClient(StanzaClient):
    """
    SDK client that assists with integrating FastAPI services with Stanza Hub,
    and managing the active service and guard configurations.
    """

    def __init__(self, config: StanzaConfiguration):
        super().__init__(config)

    def stanza_guard(self, handler):
        """Wrap your FastAPI handler with a Stanza guard."""

        # TODO: Confirm that request bodies pass without issue. Query
        # parameters and path parameters have already been verified.

        handler_parameters = inspect.signature(handler).parameters.values()

        # We need to make sure that an argument with type 'fastapi.Request' is
        # passed into the handler so that FastAPI gives us request information
        # needed to propagate baggage. If the handler we're wrapping doesn't
        # inject it, then return a wrapper that asks for it.
        wrapper = (
            _wrapper_without_request(handler)
            if any(p.annotation == Request for p in handler_parameters)
            else _wrapper_with_request(handler)
        )

        # Merge the calling signatures of our decorator with the signature of
        # the handler being passed into it so FastAPI injects the needed
        # dependencies needed by us and also whatever the handler itself needs.
        #
        # The only potential conflicting field is a positional argument with
        # the 'fastapi.Request' type (name and exact position doesn't matter to
        # FastAPI, just the type). That's handled by choosing the wrapper based
        # on whether it's provided by the handler or not.
        wrapper.__signature__ = inspect.Signature(
            parameters=[
                # Use parameters from the wrapper, save for *args and **kwargs.
                # These need to come first to ensure any query parameters with
                # defaults in-use by the handler come after any positional
                # arguments that we add.
                *filter(
                    lambda p: p.kind
                    not in (
                        inspect.Parameter.VAR_POSITIONAL,
                        inspect.Parameter.VAR_KEYWORD,
                    ),
                    inspect.signature(wrapper).parameters.values(),
                ),
                # Use all parameters from the handler that we're wrapping.
                *handler_parameters,
            ],
            return_annotation=inspect.signature(handler).return_annotation,
        )

        return wrapper


def _wrapper_with_request(handler):
    async def wrapper(request: Request, *args, **kwargs):
        with StanzaGuard(request):
            return await handler(*args, **kwargs)

    return wrapper


def _wrapper_without_request(handler):
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

        with StanzaGuard(request):
            return await handler(*args, **kwargs)

    return wrapper
