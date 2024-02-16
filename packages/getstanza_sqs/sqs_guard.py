import asyncio
import logging
import re
import traceback
from typing import Dict, Optional

from getstanza.client import StanzaClient
from getstanza.guard import Guard
from getstanza.propagation import context_from_mapping
from getstanza_sqs.exceptions import GuardBlockedError

QUEUE_ARN_RE = r"^arn:aws:sqs:([a-zA-Z0-9-]+):([0-9]+):(.+)$"


class SQSGuard:
    """
    Wrapper around boto3 resource objects for intercepting calls.

    We don't extend directly from the Queue resource class as it is generated
    at runtime, and we can't tell boto3 to use a different class. To workaround
    this we wrap the queue resource instead and passthrough method calls to it.
    """

    def __init__(
        self,
        queue,
        guard_name: str,
        feature_name: Optional[str] = None,
        priority_boost: Optional[int] = None,
        default_weight: Optional[float] = None,
        tags: Optional[Dict[str, str]] = None,
    ):
        self.__queue = queue
        self.__guard_name = guard_name
        self.__feature_name = feature_name
        self.__priority_boost = priority_boost
        self.__default_weight = default_weight
        self.__tags = tags
        self.__client = StanzaClient.getInstance()

    def __getattribute__(self, name):
        try:
            return super().__getattribute__(name)
        except AttributeError:
            return getattr(self.__queue, name)

    def __process_message(self, message):
        """
        Guard incoming SQS messages.

        In the event that a guard blocks, we terminate the visibility timeout
        so that the message can be processed again later.
        """

        if not self.__client.hub:
            return message  # Passthrough if SDK isn't initialized yet.

        context_from_mapping(
            dict(
                (key, value["StringValue"])
                for key, value in (message.message_attributes or {}).items()
                if value["DataType"] == "String"
            )
        )

        guard = Guard(
            self.__client.hub,
            self.__guard_name,
            feature_name=self.__feature_name,
            priority_boost=self.__priority_boost,
            default_weight=self.__default_weight,
            tags=self.__tags,
        )
        asyncio.run_coroutine_threadsafe(
            guard.run(), self.__client.hub.event_loop
        ).result()

        # 🪵 Check for and log any returned error messages
        if guard.error:
            logging.error(guard.error)

        # 🚫 Stanza Guard has *blocked* this workflow log the error and
        # raise an HTTPException with a 429 response code.
        if guard.blocked():
            logging.error(guard.block_message, extra={"reason": guard.block_reason})
            raise GuardBlockedError(guard_name=self.__guard_name)

        return message

    def __reset_messages(self, messages):
        """
        Terminate the visibility timeout on a message. This should be done for
        messages that we can't process due to an error in processing the
        message, or because the guard blocked it.
        """

        logging.debug("Resetting visibility timeout for %d message(s)", len(messages))

        response = self.__queue.meta.client.change_message_visibility_batch(
            QueueUrl=self.__queue_arn_to_url(self.__queue.attributes["QueueArn"]),
            Entries=[
                {
                    "Id": message.message_id,
                    "ReceiptHandle": message.receipt_handle,
                    "VisibilityTimeout": 1,  # TODO: Make this configurable
                }
                for message in messages
            ],
        )

        for failed_message in response.get("Failed", ()):
            logging.error(
                "Unable to reset visibility timeout for SQS message "
                "(Id=%s, SenderFault=%s, Code=%s, Message=%s)",
                failed_message["Id"],
                failed_message["SenderFault"],
                failed_message["Code"],
                failed_message["Message"],
            )

        return response

    def __queue_arn_to_url(self, arn: str) -> str:
        """
        Converts an SQS queue ARN to an HTTP URL.
        """

        if result := re.match(QUEUE_ARN_RE, arn):
            region, account_id, resource_id = result.groups()
            return f"https://sqs.{region}.amazonaws.com/{account_id}/{resource_id}"

        raise ValueError(f"{arn} is not a valid ARN")

    def receive_messages(self, *args, **kwargs):
        """
        Retrieves one or more messages (up to 10), from the specified queue.
        Using the WaitTimeSeconds parameter enables long-poll support.
        """

        messages = self.__queue.receive_messages(*args, **kwargs)

        if not self.__client.hub:
            return messages  # Passthrough if SDK isn't initialized yet.

        successful_messages = []
        failed_messages = []

        for message in messages:
            try:
                successful_messages.append(self.__process_message(message))
            except GuardBlockedError:
                failed_messages.append(message)
            except Exception:
                logging.error(
                    "Unable to process SQS message: %s", traceback.format_exc()
                )
                failed_messages.append(message)

        if len(failed_messages) > 0:
            self.__reset_messages(failed_messages)

        return successful_messages
