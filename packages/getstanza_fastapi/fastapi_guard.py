from fastapi import Request

# TODO: How do we pass baggage to all outgoing calls?

# TODO: How do we get baggage from request headers in this context?


class StanzaGuard:
    """Helps wrap a FastAPI request handler with a guard.

    Implementation is derived from the contextlib.ContextDecorator with
    some additional modifications to support our use-case.
    """

    def __init__(self, request: Request):
        self.__request = request

    def __enter__(self):
        print("Entering:", self.__request)
        return self

    def __exit__(self, *exc):
        print("Leaving:", exc)
