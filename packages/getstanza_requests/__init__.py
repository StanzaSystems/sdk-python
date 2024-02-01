"""
An adapter to ease integration of Stanza with applications utilizing Python
Requests for outbound HTTP requests.
"""

from .stanza_session import StanzaSession

__all__ = ["StanzaSession"]
