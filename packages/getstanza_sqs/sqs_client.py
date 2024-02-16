import logging
import re
import threading
from collections import defaultdict
from typing import Any, Callable, Dict, Hashable, Optional

from getstanza.client import StanzaClient
from getstanza.configuration import StanzaConfiguration
from getstanza_sqs.sqs_guard import SQSGuard

QUEUE_ARN_RE = r"^arn:aws:sqs:([a-zA-Z0-9-]+):([0-9]+):(.+)$"

# Maps known (hashable) client objects to Stanza-specific events registered to them. We
# use this to ensure that we don't register event handlers more than once when
# hooking into API calls. We have to keep track of this ourselves since boto3
# doesn't provide a way for us to inspect this at runtime.
_registered_events: defaultdict[Hashable, set[str]] = defaultdict(set)
_registered_events_lock = threading.Lock()


class StanzaSQSClient(StanzaClient):
    """
    SDK client that assists with integrating SQS queue workers with Stanza Hub,
    and managing the active service and guard configurations.
    """

    def __init__(self, config: StanzaConfiguration):
        super().__init__(config)

    def stanza_guard(
        self,
        queue,
        guard_name: str,
        feature_name: Optional[str] = None,
        priority_boost: Optional[int] = None,
        default_weight: Optional[float] = None,
        tags: Optional[Dict[str, str]] = None,
    ):
        """
        Wraps a queue with a Stanza guard. This function will also hook Stanza into
        all 'provide-client-params.sqs.ReceiveMessage' events emitted by the client
        associated with the passed in queue if it's not already registered.
        """

        self.__register_stanza_event_once(
            client=queue.meta.client,
            event_name="provide-client-params.sqs.ReceiveMessage",
            handler=self.__receive_messages,
        )

        if result := re.search(QUEUE_ARN_RE, queue.attributes["QueueArn"]):
            region, account_id, resource_id = result.groups()

            logging.info(
                "Guarding queue with attributes region: %s, account-id: %s, resource-id: %s",
                region,
                account_id,
                resource_id,
            )

        return SQSGuard(
            queue,
            guard_name,
            feature_name=feature_name,
            priority_boost=priority_boost,
            default_weight=default_weight,
            tags=tags,
        )

    def __receive_messages(self, params: dict[str, Any], **kwargs) -> dict[str, Any]:
        """
        Add additional parameters to ReceiveMessage calls that Stanza needs to
        function. Specifically we add "baggage" to the "MessageAttributeNames"
        param so that OTEL baggage can be propagated.
        """

        # TODO: Use approximate stats in queue object to help optimize guard?

        if "MessageAttributeNames" not in params:
            params["MessageAttributeNames"] = []

        if "baggage" not in map(str.casefold, params["MessageAttributeNames"]):
            params["MessageAttributeNames"].append("baggage")

        return params

    def __register_stanza_event_once(self, client, event_name: str, handler: Callable):
        """Registers an event on a client if it's not already registered."""

        with _registered_events_lock:
            if event_name not in _registered_events[client]:
                event_system = client.meta.events
                event_system.register(event_name, handler)
                _registered_events[client].add(event_name)
