"""
An adapter to ease integration of Stanza with FastAPI applications.
"""

from .fastapi_client import StanzaFastAPIClient
from .fastapi_guard import StanzaGuard

__all__ = ["StanzaFastAPIClient", "StanzaGuard"]
