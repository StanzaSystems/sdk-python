import logging
import sys
from typing import Any

import boto3
from getstanza.configuration import StanzaConfiguration
from getstanza_sqs import StanzaSQSClient

# SQS Example Service
NAME = "sqs-example"
RELEASE = "0.0.1"
ENV = "dev"
DEBUG = False

if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

# Log basic service details at startup
logging.info("service init, name:%s, release:%s, env:%s", NAME, RELEASE, ENV)

# Init Stanza fault tolerance library
try:
    client = StanzaSQSClient(
        StanzaConfiguration(
            # api_key="YOUR-API-KEY-HERE",  # or via STANZA_API_KEY environment variable
            service_name=NAME,  # or via STANZA_SERVICE_NAME environment variable
            service_release=RELEASE,  # or via STANZA_SERVICE_RELEASE environment variable
            environment=ENV,  # or via STANZA_ENVIRONMENT environment variable
        )
    )
except ValueError as exc:
    logging.exception(exc)
    sys.exit(1)

sqs = boto3.resource("sqs")
queue = client.stanza_guard(
    sqs.get_queue_by_name(QueueName="JkGuardTesting"), "FamousQuotes"
)


def process_message(message):
    logging.info("Received incoming SQS message: %r", message)


if __name__ == "__main__":
    logging.info("Starting SQS example, listening for messages...")

    while True:
        messages: list[Any] = queue.receive_messages(MaxNumberOfMessages=1)
        for message in messages:
            process_message(message)
            message.delete()
