"""
An adapter to ease integration of Stanza with applications that send or consume
AWS SQS messages.
"""

from .sqs_client import StanzaSQSClient

__all__ = ["StanzaSQSClient"]
