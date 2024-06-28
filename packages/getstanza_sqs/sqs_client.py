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
    StanzaSQSClient

    This class extends the StanzaClient class to provide additional functionality for working with AWS SQS queues.
    SDK client that assists with integrating SQS queue workers with Stanza Hub,
    and managing the active service and guard configurations.

    Attributes:
    - config: StanzaConfiguration - The configuration object for the Stanza client.

    Methods:
    - __init__(self, config: StanzaConfiguration)
      Initializes a new instance of the StanzaSQSClient class with the specified configuration.

    - stanza_guard(
        self,
        queue,
        guard_name: str,
        feature_name: Optional[str] = None,
        priority_boost: Optional[int] = None,
        default_weight: Optional[float] = None,
        tags: Optional[Dict[str, str]] = None,
    )
      Wraps a queue with a Stanza guard. This function will also hook Stanza into
      all 'provide-client-params.sqs.ReceiveMessage' events emitted by the client
      associated with the passed in queue if it's not already registered.

    - __receive_messages(params: dict[str, Any], **kwargs) -> dict[str, Any]
      Add additional parameters to ReceiveMessage calls that Stanza needs to
      function. Specifically, we add "baggage" to the "MessageAttributeNames"
      param so that OTEL baggage can be propagated.

    - __register_stanza_event_once(client, event_name: str, handler: Callable)
      Registers an event on a client if it's not already registered.
    """

    def __init__(self, config: StanzaConfiguration):
        """

        Initializes an instance of the class.

        Parameters:
            config (StanzaConfiguration): The configuration object.

        """
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
        Stanza Guard

        This method registers a stanza event once
        and creates an instance of SQSGuard to guard a queue with specified attributes.

        Wraps a queue with a Stanza guard. This function will also hook Stanza into
        all 'provide-client-params.sqs.ReceiveMessage' events emitted by the client
        associated with the passed in queue if it's not already registered.

        Parameters:
        - queue: The queue to be guarded.
        - guard_name: The name of the guard.
        - feature_name (optional): The name of the feature. Default is None.
        - priority_boost (optional): The priority boost for the guard.
        Default is None.
        - default_weight (optional): The default weight for the guard. Default is None.
        - tags (optional): Additional tags for the guard.
        Default is None.

        Returns:
        An instance of SQSGuard.
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

    @staticmethod
    def __receive_messages(params: dict[str, Any], **kwargs) -> dict[str, Any]:
        """
        Receives messages with additional parameters.
        Add additional parameters to ReceiveMessage calls that Stanza needs to
        function. Specifically, we add "baggage" to the "MessageAttributeNames"
        param so that OTEL baggage can be propagated.

        :param params: A dictionary containing the parameter values.
        :type params: dict[str, Any]
        :param kwargs: Additional keyword arguments.
        :return: A dictionary containing the modified parameter values.
        :rtype: dict[str, Any]

        note::
            The method expects the input parameters to be provided in the `params` dictionary.
            If the "MessageAttributeNames" parameter is not present in the `params` dictionary,
            it will be added with an empty list value.
            Additionally, if the "baggage" keyword
            is not present in the list of message attribute names, it will be appended.
            The
            modified `params` dictionary is then returned.
        """

        # TODO: Use approximate stats in queue object to help optimize guard?

        if "MessageAttributeNames" not in params:
            params["MessageAttributeNames"] = []

        if "baggage" not in map(str.casefold, params["MessageAttributeNames"]):
            params["MessageAttributeNames"].append("baggage")

        return params

    @staticmethod
    def __register_stanza_event_once(client, event_name: str, handler: Callable):
        """Registers an event on a client if it's not already registered."""

        with _registered_events_lock:
            if event_name not in _registered_events[client]:
                event_system = client.meta.events
                event_system.register(event_name, handler)
                _registered_events[client].add(event_name)
