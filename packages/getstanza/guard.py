import asyncio
import datetime
import logging
import threading
import time
from collections import defaultdict
from datetime import timedelta
from enum import Enum
from typing import Iterable, MutableMapping, Optional, cast

import getstanza.client
import grpc
from getstanza.configuration import StanzaConfiguration
from stanza.hub.v1 import common_pb2, config_pb2, quota_pb2, quota_pb2_grpc
from stanza.hub.v1.common_pb2 import Config, Local, Quota, Token

# Definition for the 200ms deadline for communicated consumed tokens to Hub.
# Specification Link: https://github.com/StanzaSystems/sdk-spec#token-leases
BATCH_TOKEN_CONSUME_INTERVAL = 0.2

# Contains all cached leases returned by Hub that haven't been used yet.
cached_leases: MutableMapping[tuple, list[quota_pb2.TokenLease]] = {}
cached_leases_lock = threading.Lock()

# Contains all leases that have been consumed, but not yet communicated to Hub.
consumed_leases: defaultdict[str, list[quota_pb2.TokenLease]] = defaultdict(list)
consumed_leases_lock = threading.Lock()

# An asynchronous task that flushes consumed leases to Hub every ~200ms.
batch_token_consumer_task: Optional[asyncio.Task] = None
batch_token_consumer_task_lock = threading.Lock()


class GuardedStatus(Enum):
    """Indicate success or failure of the guarded code block"""

    GUARDED_UNKNOWN = 0
    GUARDED_SUCCESS = 1
    GUARDED_FAILURE = 2


class Guard:
    """
    Generic Guard class that implements logic for interacting with Stanza
    Guards. All framework-specific logic is kept out of this implementation.
    """

    @property
    def success(self):
        return GuardedStatus.GUARDED_SUCCESS

    @property
    def failure(self):
        return GuardedStatus.GUARDED_FAILURE

    @property
    def error(self) -> Optional[str]:
        """If there was an error, return the message as a string."""

        return self.__error_message

    @property
    def block_message(self) -> Optional[str]:
        """Returns the reason for the block as a human readable string."""

        if self.__local_status is Local.LOCAL_BLOCKED:
            return "Local resource exhausted. Please try again later."

        if self.__token_status is Token.TOKEN_NOT_VALID:
            return "Invalid or expired X-Stanza-Token."

        if self.__quota_status is Quota.QUOTA_BLOCKED:
            return "Stanza quota exhausted. Please try again later."

        return None

    @property
    def block_reason(self) -> Optional[str]:
        """Returns the reason for the block as a string."""

        if self.__local_status is Local.LOCAL_BLOCKED:
            return Local.Name(self.__local_status)

        if self.__token_status is Token.TOKEN_NOT_VALID:
            return Token.Name(self.__token_status)

        if self.__quota_status is Quota.QUOTA_BLOCKED:
            return Quota.Name(self.__quota_status)

        return None

    @property
    def quota_token(self) -> Optional[str]:
        """Returns the quota token for this request."""

        return self.__quota_token

    @property
    def guard_config(self) -> config_pb2.GuardConfig:
        """The active guard configuration."""

        return self.__guard_config

    @guard_config.setter
    def guard_config(self, value):
        if self.__guard_config is not None:
            raise AttributeError(
                f"Guard '{self.__guard_name}' has already been initialized "
                f"with a configuration.",
            )

        self.__guard_config = value

    @property
    def __cached_lease_key(self):
        """Returns the cache key needed to find cached leases for the guard."""

        return (
            cast(str, self.__stanza_config.environment),
            self.__guard_name,
            self.__feature_name,
            self.__priority_boost,
        )

    @property
    def __consumed_lease_key(self):
        """Returns the key needed to group consumed leases by env."""

        return cast(str, self.__stanza_config.environment)

    def __init__(
        self,
        quota_service: quota_pb2_grpc.QuotaServiceStub,
        stanza_config: StanzaConfiguration,
        guard_config: config_pb2.GuardConfig,
        guard_config_status: int,
        guard_name: str,
        feature_name: Optional[str] = None,
        priority_boost: Optional[int] = None,
        default_weight: Optional[float] = None,
        tags=None,
    ):
        global batch_token_consumer_task

        self.__quota_service = quota_service
        self.__stanza_config = stanza_config
        self.__guard_config = guard_config
        self.__guard_name = guard_name
        self.__feature_name = feature_name
        self.__priority_boost = priority_boost
        self.__default_weight = default_weight
        self.__tags = tags

        self.__quota_token: Optional[str] = None
        self.__error_message: Optional[str] = None
        self.__start: Optional[datetime.datetime] = None

        self.__config_status = guard_config_status
        self.__local_status = Local.LOCAL_NOT_EVAL
        self.__token_status = Token.TOKEN_NOT_EVAL
        self.__quota_status = Quota.QUOTA_NOT_EVAL

        # Start the task to flush consumed token leases if not already started.
        with batch_token_consumer_task_lock:
            if batch_token_consumer_task is None:
                loop = asyncio.get_running_loop()
                batch_token_consumer_task = loop.create_task(batch_token_consumer())
                batch_token_consumer_task.add_done_callback(handle_batch_token_consumer)

    async def run(self, tokens: Optional[Iterable[str]] = None) -> bool:
        """Run all guard checks and update guard statuses."""

        try:
            # Config state check
            try:
                self.__config_status = self.__check_config()
            except Exception:
                logging.exception(
                    "Received unexpected exception while checking guard config"
                )
                self.__config_status = Config.CONFIG_NOT_FOUND

            if (
                self.__config_status != Config.CONFIG_CACHED_OK
                and self.__config_status != Config.CONFIG_FETCHED_OK
            ):
                return self.allowed()

            # Local (Sentinel) check
            try:
                self.__local_status = self.__check_local()
            except Exception:
                logging.exception(
                    "Received unexpected exception while checking Sentinel"
                )
                self.__local_status = Local.LOCAL_ERROR

            if self.__local_status == Local.LOCAL_BLOCKED:
                return self.allowed()

            # Ingress token check
            try:
                self.__token_status = self.__check_token(tokens)
            except Exception:
                logging.exception(
                    "Received unexpected exception while checking ingress tokens"
                )
                self.__token_status = Token.TOKEN_VALIDATION_ERROR

            if self.__local_status == Token.TOKEN_NOT_VALID:
                return self.allowed()

            # Quota check
            try:
                self.__quota_status, self.__quota_token = self.__check_quota()
            except Exception:
                logging.exception(
                    "Received unexpected exception while checking Sentinel"
                )
                self.__quota_status = Quota.QUOTA_ERROR

            return self.allowed()
        finally:
            if not self.__error_message:
                if self.allowed():
                    self.__allowed()
                else:
                    self.__blocked()

    def __check_config(self) -> Config:
        """Check guard configuration."""

        return (
            Config.CONFIG_CACHED_OK
            if self.__guard_config is not None
            else Config.CONFIG_NOT_FOUND
        )

    def __check_local(self) -> Local:
        """Local check is not currently supported by this SDK."""

        return Local.LOCAL_NOT_SUPPORTED

    def __check_token(self, tokens: Optional[Iterable[str]] = None) -> Token:
        """Validate using the ingress token if configured to do so."""

        if not self.__guard_config.validate_ingress_tokens:
            return Token.TOKEN_EVAL_DISABLED

        if not tokens:
            return Token.TOKEN_NOT_VALID

        tokens_info = list(
            map(
                lambda token: quota_pb2.TokenInfo(
                    token=token,
                    guard=common_pb2.GuardSelector(
                        environment=self.__stanza_config.environment,
                        name=self.__guard_name,
                    ),
                ),
                tokens or [],
            )
        )

        # TODO: Handle validation timeout.

        try:
            validate_token_response = cast(
                quota_pb2.ValidateTokenResponse,
                self.__quota_service.ValidateToken(
                    request=quota_pb2.ValidateTokenRequest(tokens=tokens_info),
                    metadata=self.__stanza_config.metadata,
                ),
            )
        except grpc.RpcError as rpc_error:
            self.__failopen(rpc_error.debug_error_string())  # type: ignore
            return Token.TOKEN_VALIDATION_ERROR

        return (
            Token.TOKEN_VALID
            if validate_token_response.valid
            else Token.TOKEN_NOT_VALID
        )

    def __check_quota(self) -> tuple[Quota, Optional[str]]:
        """Quota check using token leases."""

        if not self.__guard_config.check_quota:
            return Quota.QUOTA_EVAL_DISABLED, None

        # TODO: Check baggage for stz-feat and stz-boost

        # Check to see if a cached lease can be found using the guard selector.
        if cached_lease := self.__consume_cached_token_lease():
            logging.debug("Found a valid cached token lease: %s", cached_lease.token)

            return Quota.QUOTA_GRANTED, cached_lease.token

        token_lease_request = quota_pb2.GetTokenLeaseRequest(
            selector=common_pb2.GuardFeatureSelector(
                environment=self.__stanza_config.environment,
                guard_name=self.__guard_name,
                feature_name=self.__feature_name,
                tags=[],
            ),
            client_id=self.__stanza_config.client_id,
            priority_boost=self.__priority_boost,
            default_weight=self.__default_weight,
        )

        try:
            logging.debug(
                "Requesting a token lease with selector: "
                "(environment = %s, guard = %s, feature = %s, priority = %s)",
                self.__stanza_config.environment,
                self.__guard_name,
                self.__feature_name,
                self.__priority_boost,
            )

            token_lease_response = cast(
                quota_pb2.GetTokenLeaseResponse,
                self.__quota_service.GetTokenLease(
                    request=token_lease_request,
                    metadata=self.__stanza_config.metadata,
                ),
            )
        except grpc.RpcError as rpc_error:
            self.__failopen(rpc_error.debug_error_string())  # type: ignore
            return Quota.QUOTA_BLOCKED, None

        # Immediately consume a lease upon being granted token leases, and
        # cache the rest for later use; otherwise set quota status to BLOCKED.
        if token_lease_response.granted:
            lease = token_lease_response.leases[0]
            self.__consume_token_lease(lease)

            logging.debug(
                "Received %d token leases: %s",
                len(token_lease_response.leases),
                token_lease_response.leases,
            )

            if len(token_lease_response.leases) > 1:
                self.__set_cached_token_leases(token_lease_response.leases[1:])

            return Quota.QUOTA_GRANTED, lease.token

        logging.debug("Token lease request has been denied")

        return Quota.QUOTA_BLOCKED, None

    def allowed(self) -> bool:
        """Check if the Guard is currently allowing traffic."""

        # Always allow traffic when 'report only' is set.
        if self.__guard_config and self.__guard_config.report_only:
            return True

        # Allow if all of the following checks have succeeded.
        return (
            (
                self.__config_status == Config.CONFIG_CACHED_OK
                or self.__config_status == Config.CONFIG_FETCHED_OK
            )
            and self.__local_status != Local.LOCAL_BLOCKED
            and self.__quota_status != Quota.QUOTA_BLOCKED
            and self.__token_status != Token.TOKEN_NOT_VALID
        )

    def blocked(self) -> bool:
        """Check if the Guard is currently disallowing traffic."""

        return not self.allowed()

    def end(self, status: GuardedStatus):
        """Called when the guarded logic comes to an end."""

        # TODO: Collect success / failure metrics here.

    def __log(self) -> str:
        """Returns all of the current status state of the guild."""

        return "guard={}, config_state={}, local_reason={}, token_reason={}, quota_reason={}".format(
            self.__guard_name,
            Config.Name(self.__config_status),
            Local.Name(self.__local_status),
            Token.Name(self.__token_status),
            Quota.Name(self.__quota_status),
        )

    def __allowed(self):
        """Log an allowed event to OTEL."""

        # TODO: OTEL meter (AllowedCount) and trace span
        logging.debug("Stanza allowed, %s", self.__log())
        self.__start = datetime.datetime.now()

    def __blocked(self):
        """Log a blocked event to OTEL."""

        # TODO: OTEL meter (BlockedCount) and trace span
        logging.debug("Stanza blocked, %s", self.__log())

    def __failopen(self, error_message: str):
        """Log a failopen event to OTEL."""

        # TODO: OTEL meter (FailOpenCount) and trace span
        self.__error_message = error_message
        logging.debug(error_message)
        logging.debug("Stanza failed open, %s", self.__log())

    def __consume_cached_token_lease(self) -> Optional[quota_pb2.TokenLease]:
        """Scans cached leases and finds the first valid and unexpired lease."""

        with cached_leases_lock:
            if self.__cached_lease_key not in cached_leases:
                return None

            # Scan through leases until a valid and unexpired one is found. Any
            # invalid leases found during this process are discarded.
            while len(cached_leases[self.__cached_lease_key]) > 0:
                cached_lease = cached_leases[self.__cached_lease_key].pop(0)
                if self.__check_token_lease(cached_lease):
                    self.__consume_token_lease(cached_lease)
                    return cached_lease

    def __set_cached_token_leases(self, leases: Iterable[quota_pb2.TokenLease]):
        """Replaces all cached token leases with a new set of leases."""

        _leases = list(leases)

        # If Hub doesn't return an expiration date for any of the leases, infer
        # it using the duration_msec field associated with the lease.
        for lease in _leases:
            if lease.expires_at is None:
                lease.expires_at = datetime.datetime.now() + timedelta(
                    milliseconds=lease.duration_msec
                )

        with cached_leases_lock:
            cached_leases[self.__cached_lease_key].extend(_leases)

    def __check_token_lease(self, lease: quota_pb2.TokenLease) -> bool:
        """Returns false if a token lease is expired or invalid."""

        if (
            datetime.datetime.timestamp(datetime.datetime.now())
            >= lease.expires_at.seconds
        ):
            logging.debug(
                "Discarding token lease '%s' as it is now expired", lease.token
            )
            return False  # Expired

        # TODO: Use baggage value for priority boost.

        # if baggage.priority_boost <= lease.priority_boost:
        #     logging.debug(
        #         "Discarding token lease '%s' as the priority boost is above "
        #         "the configured priority boost (%d <= %d)",
        #         lease.token,
        #         self.priority_boost,
        #         lease.priority_boost,
        #     )
        #     return False  # Priority boost is too high.

        return True

    def __consume_token_lease(self, lease: quota_pb2.TokenLease):
        """Marks a token lease as consumed so we can notify Hub later."""

        with consumed_leases_lock:
            consumed_leases[self.__consumed_lease_key].append(lease)

        logging.debug("Currently sitting at %d consumed leases", len(consumed_leases))


async def batch_token_consumer():
    """Iterates through all consumed tokens and consumes them in batches.

    This function will loop indefinitely by an interval time as defined in
    'BATCH_TOKEN_CONSUME_INTERVAL' (e.g. 200ms).
    """

    global consumed_leases

    logging.debug("Starting batch token consumer background worker")

    # TODO: Stop this loop when SIGINT or SIGTERM signals are received.

    while True:
        start_time = time.perf_counter()

        # Quickly snatch and empty out the consumed leases so that we don't block
        # future leases from being consumed while we wait for Hub to finish
        # processing our batch request.
        with consumed_leases_lock:
            seized_leases = consumed_leases
            consumed_leases = defaultdict(list)

        tasks = []

        for environment, leases in seized_leases.items():
            tasks.append(
                asyncio.ensure_future(
                    set_token_lease_consumed(leases, environment)
                )  # type: ignore
            )

        if len(tasks) > 0:
            await asyncio.wait(tasks)

        # We measure the time it takes to consume tokens and subtract that from
        # the interval to ensure that we don't surpass the 200ms deadline as
        # defined in the specification under nominal networking conditions.
        elapsed_time = time.perf_counter() - start_time
        delay = max(BATCH_TOKEN_CONSUME_INTERVAL - elapsed_time, 0)

        if delay > 0:
            await asyncio.sleep(delay)


def handle_batch_token_consumer(task: asyncio.Task):
    """Gracefully handle and log errors from the background consumer task.

    If the task fails because of an error, it will be rescheduled and continue
    to attempt to send consumed tokens to Hub on an interval.
    """

    # TODO: Retry logic for consumed tokens that we failed to send to Hub?

    global batch_token_consumer_task

    try:
        task.result()
    except asyncio.CancelledError:
        pass  # Do not log task cancellations.
    except Exception:
        logging.exception("Received unexpected exception while consuming leases")

        with batch_token_consumer_task_lock:
            batch_token_consumer_task = asyncio.ensure_future(batch_token_consumer())
            batch_token_consumer_task.add_done_callback(handle_batch_token_consumer)


async def set_token_lease_consumed(
    leases: Iterable[quota_pb2.TokenLease],
    environment: str,
):
    """Consume a set of token leases for a given environment."""

    client = getstanza.client.StanzaClient.getInstance()

    set_token_lease_consumed_request = quota_pb2.SetTokenLeaseConsumedRequest(
        tokens=list(map(lambda lease: lease.token, leases)),
        environment=environment,
    )
    logging.debug(
        "Consuming %d token leases from environment '%s'",
        len(set_token_lease_consumed_request.tokens),
        environment,
    )

    # TODO: We should set a timeout, right?
    client.hub.quota_service.SetTokenLeaseConsumed(
        request=set_token_lease_consumed_request,
        metadata=client.config.metadata,
    )
