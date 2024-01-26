import asyncio
import datetime
import logging
import threading
import time
from collections import defaultdict
from datetime import timedelta, timezone
from enum import Enum
from typing import Iterable, Optional, cast

import grpc
from getstanza.hub import StanzaHub
from getstanza.otel import StanzaMeter
from getstanza.propagation import get_feature, get_priority_boost
from opentelemetry.trace import Span, StatusCode
from opentelemetry.util.types import Attributes
from stanza.hub.v1 import common_pb2, config_pb2, quota_pb2
from stanza.hub.v1.common_pb2 import Config, Local, Mode, Quota, Token

# Definition for the 200ms deadline for communicated consumed tokens to Hub.
# Specification Link: https://github.com/StanzaSystems/sdk-spec#token-leases
BATCH_TOKEN_CONSUME_INTERVAL = 0.2

DEFAULT_TIMEOUT = 300
TOKEN_LEASE_TIMEOUT = 200

# Contains all cached leases returned by Hub that haven't been used yet.
cached_leases: defaultdict[
    tuple, list[tuple[datetime.datetime, quota_pb2.TokenLease]]  # Expiration and lease
] = defaultdict(list)
cached_leases_lock = threading.Lock()

# Contains all leases that have been consumed, but not yet communicated to Hub.
consumed_leases: defaultdict[str, list[quota_pb2.TokenLease]] = defaultdict(list)
consumed_leases_lock = threading.Lock()

# An asynchronous task that flushes consumed leases to Hub every ~200ms.
batch_token_consumer_handle: Optional[asyncio.Handle] = None
batch_token_consumer_handle_lock = threading.Lock()


class GuardedStatus(Enum):
    """Indicate success or failure of the guarded code block."""

    GUARDED_UNKNOWN = 0
    GUARDED_SUCCESS = 1
    GUARDED_FAILURE = 2


class GuardEvent(Enum):
    """Possible event types a guard may emit."""

    ALLOWED = 0
    BLOCKED = 1
    FAILOPEN = 2


class TokenLeaseStatus(Enum):
    """Represents the possible statuses of a cached token lease."""

    TOKEN_LEASE_VALID = 0
    TOKEN_LEASE_EXPIRED = 1
    TOKEN_LEASE_WRONG_PRIORITY = 2


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
    def config_status(self):
        return self.__config_status

    @property
    def local_status(self):
        return self.__local_status

    @property
    def token_status(self):
        return self.__token_status

    @property
    def quota_status(self):
        return self.__quota_status

    @property
    def quota_token(self):
        return self.__quota_token

    @property
    def guard_config(self):
        return self.__guard_config

    @property
    def error(self):
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
    def __cached_lease_key(self):
        """Returns the cache key needed to find cached leases for the guard."""

        return (
            str(self.__client_config.environment or ""),
            self.__guard_name,
            self.__feature_name,
        )

    @property
    def __consumed_lease_key(self):
        """Returns the key needed to group consumed leases by env."""

        return str(self.__client_config.environment or "")

    def __init__(
        self,
        hub: StanzaHub,
        guard_name: str,
        feature_name: Optional[str] = None,
        priority_boost: Optional[int] = None,
        default_weight: Optional[float] = None,
        tags=None,
    ):
        global batch_token_consumer_handle

        self.__guard_name = guard_name
        self.__feature_name = get_feature(feature_name)
        self.__priority_boost = get_priority_boost(priority_boost) or 0
        self.__default_weight = 0 if default_weight is None else default_weight
        self.__tags = tags

        self.__event_loop = hub.event_loop
        self.__quota_service = hub.quota_service
        self.__config_manager = hub.config_manager
        self.__client_config = hub.config_manager.config

        self.__meter: Optional[StanzaMeter] = None
        self.__span: Optional[Span] = None
        self.__start: Optional[datetime.datetime] = None
        self.__quota_token: Optional[str] = None
        self.__error_message: Optional[str] = None
        self.__guard_config: Optional[config_pb2.GuardConfig] = None

        self.__mode = Mode.MODE_NORMAL
        self.__config_status = Config.CONFIG_UNSPECIFIED
        self.__local_status = Local.LOCAL_NOT_EVAL
        self.__token_status = Token.TOKEN_NOT_EVAL
        self.__quota_status = Quota.QUOTA_NOT_EVAL

        # Start the task to flush consumed token leases if not already started.
        with batch_token_consumer_handle_lock:
            if batch_token_consumer_handle is None:
                batch_token_consumer_handle = self.__event_loop.call_soon_threadsafe(
                    start_batch_token_consumer(self.__event_loop)
                )

    def __repr__(self) -> str:
        """Returns all of the current status state of the guard."""

        return "guard={}, config_state={}, local_reason={}, token_reason={}, quota_reason={}".format(
            self.__guard_name,
            Config.Name(self.__config_status),
            Local.Name(self.__local_status),
            Token.Name(self.__token_status),
            Quota.Name(self.__quota_status),
        )

    async def run(self, tokens: Optional[Iterable[str]] = None):
        """Run all guard checks and update guard statuses."""

        if self.__config_manager.otel:
            if self.__config_manager.otel.meter:
                self.__meter = self.__config_manager.otel.meter
            if self.__config_manager.otel.tracer:
                self.__span = self.__config_manager.otel.tracer.start_span(
                    "stanza-guard"
                )

        try:
            # Config state check
            if not await self.__check_config():
                return

            # Local rules check
            if not self.__check_local():
                return

            # Ingress token check
            if not self.__check_token(tokens):
                return

            # Quota check
            self.__check_quota()

        except Exception as exc:
            if self.__span:
                self.__span.record_exception(exc)

            if not self.__error_message:
                template = "an unknown exception of type {0} occurred"
                self.__error_message = template.format(type(exc).__name__)

        finally:
            if self.__error_message:
                self.__failopen()
            elif self.allowed():
                self.__allowed()
            else:
                self.__blocked()

            if self.__span:
                self.__span.end()

    async def __check_config(self) -> bool:
        """Check guard configuration."""

        if self.__guard_config is None:
            (
                self.__guard_config,
                self.__config_status,
            ) = await self.__config_manager.get_guard_config(self.__guard_name)

        if self.__guard_config is not None:
            if self.__guard_config.report_only:
                self.__mode = Mode.MODE_REPORT_ONLY
            if (
                self.__config_status == Config.CONFIG_CACHED_OK
                or self.__config_status == Config.CONFIG_FETCHED_OK
            ):
                return True

        self.__error_message = "unable to fetch guard config: {}".format(
            Config.Name(self.__config_status)
        )
        return False

    def __check_local(self) -> bool:
        """Local check is not currently supported by this SDK."""

        self.__local_status = Local.LOCAL_NOT_SUPPORTED
        return True

    def __check_token(self, tokens: Optional[Iterable[str]] = None) -> bool:
        """Validate using the ingress token if configured to do so."""

        if not self.__guard_config or not self.__guard_config.validate_ingress_tokens:
            self.__token_status = Token.TOKEN_EVAL_DISABLED
            return True

        if not tokens:
            self.__token_status = Token.TOKEN_NOT_VALID
            return False

        tokens_info = list(
            map(
                lambda token: quota_pb2.TokenInfo(
                    token=token,
                    guard=common_pb2.GuardSelector(
                        environment=self.__client_config.environment,
                        name=self.__guard_name,
                    ),
                ),
                tokens or [],
            )
        )

        try:
            validate_token_response = cast(
                quota_pb2.ValidateTokenResponse,
                self.__quota_service.ValidateToken(
                    request=quota_pb2.ValidateTokenRequest(tokens=tokens_info),
                    metadata=self.__client_config.metadata,
                    timeout=DEFAULT_TIMEOUT,
                ),
            )
        except grpc.RpcError as rpc_error:
            self.__error_message = str(rpc_error)
            self.__token_status = Token.TOKEN_VALIDATION_ERROR
            return False

        if validate_token_response.valid:
            self.__token_status = Token.TOKEN_VALID
            return True
        else:
            self.__token_status = Token.TOKEN_NOT_VALID
            return False

    def __check_quota(self) -> bool:
        """Quota check using token leases."""

        if not self.__guard_config or not self.__guard_config.check_quota:
            self.__quota_status = Quota.QUOTA_EVAL_DISABLED
            return True

        # Check to see if a cached lease can be found using the guard selector.
        if cached_lease := self.__consume_cached_token_lease():
            logging.debug("Found a valid cached token lease: %s", cached_lease.token)
            self.__quota_status = Quota.QUOTA_GRANTED
            self.__quota_token = cached_lease.token
            return True

        token_lease_request = quota_pb2.GetTokenLeaseRequest(
            selector=common_pb2.GuardFeatureSelector(
                environment=self.__client_config.environment,
                guard_name=self.__guard_name,
                feature_name=self.__feature_name,
                tags=[],
            ),
            client_id=self.__client_config.client_id,
            priority_boost=self.__priority_boost,
            default_weight=self.__default_weight,
        )

        try:
            logging.debug(
                "Requesting a token lease with selector: "
                "(environment = %s, guard = %s, feature = %s, priority boost = %s, default weight = %s)",
                self.__client_config.environment,
                self.__guard_name,
                self.__feature_name,
                self.__priority_boost,
                self.__default_weight,
            )

            token_lease_response = cast(
                quota_pb2.GetTokenLeaseResponse,
                self.__quota_service.GetTokenLease(
                    request=token_lease_request,
                    metadata=self.__client_config.metadata,
                    timeout=TOKEN_LEASE_TIMEOUT,
                ),
            )
        except grpc.RpcError as rpc_error:
            self.__error_message = str(rpc_error)
            self.__quota_status = Quota.QUOTA_ERROR
            return False

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

            self.__quota_status = Quota.QUOTA_GRANTED
            self.__quota_token = lease.token
            return True

        logging.debug("Token lease request has been denied")
        self.__quota_status = Quota.QUOTA_BLOCKED
        return False

    def allowed(self) -> bool:
        """Check if the Guard is currently allowing traffic."""

        # Allow if config is unspecified or failed to fetch the first time.
        if self.__guard_config is None and self.__config_status in [
            Config.CONFIG_UNSPECIFIED,
            Config.CONFIG_FETCH_ERROR,
            Config.CONFIG_FETCH_TIMEOUT,
        ]:
            return True

        # Always allow traffic when 'report only' is set.
        if self.__mode == Mode.MODE_REPORT_ONLY:
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
        if self.__meter:
            if self.__start:
                duration_ms = (
                    datetime.datetime.now() - self.__start
                ) / datetime.timedelta(milliseconds=1)
                self.__meter.AllowedDuration.record(duration_ms, self.__attributes())
            if status == GuardedStatus.GUARDED_SUCCESS:
                self.__meter.AllowedSuccessCount.add(1, self.__attributes())
            elif status == GuardedStatus.GUARDED_FAILURE:
                self.__meter.AllowedFailureCount.add(1, self.__attributes())
            else:
                self.__meter.AllowedUnknownCount.add(1, self.__attributes())

    def __attributes(self) -> Attributes:
        attr: Attributes = {
            "client_id": self.__client_config.client_id,
            "customer_id": str(self.__client_config.customer_id or ""),
            "environment": str(self.__client_config.environment or ""),
            "guard": self.__guard_name,
            "feature": str(self.__feature_name or ""),
            "service": str(self.__client_config.service_name or ""),
            "mode": Mode.Name(self.__mode),
            "config_state": Config.Name(self.__config_status),
            "local_reason": Local.Name(self.__local_status),
            "token_reason": Token.Name(self.__token_status),
            "quota_reason": Quota.Name(self.__quota_status),
        }
        return attr

    def __emit_event(self, guard_event: GuardEvent, message: str):
        """Log any type of guard event."""

        if message != "":
            logging.debug(f"{message}, %s", repr(self))

        if self.__meter:
            if guard_event == GuardEvent.ALLOWED:
                self.__meter.AllowedCount.add(1, self.__attributes())
            elif guard_event == GuardEvent.BLOCKED:
                self.__meter.BlockedCount.add(1, self.__attributes())
            elif guard_event == GuardEvent.FAILOPEN:
                self.__meter.FailOpenCount.add(1, self.__attributes())

        if self.__span:
            if guard_event == GuardEvent.ALLOWED:
                self.__span.add_event("Stanza allowed", self.__attributes())
                self.__span.set_status(StatusCode.OK)
            elif guard_event == GuardEvent.BLOCKED:
                self.__span.add_event("Stanza blocked", self.__attributes())
                self.__span.set_status(StatusCode.ERROR, message)
            elif guard_event == GuardEvent.FAILOPEN:
                self.__span.add_event("Stanza failed open", self.__attributes())
                self.__span.set_status(StatusCode.ERROR, message)

    def __allowed(self):
        """Log an allowed event."""

        self.__emit_event(GuardEvent.ALLOWED, "Stanza allowed")
        self.__start = datetime.datetime.now()

    def __blocked(self):
        """Log a blocked event."""

        self.__emit_event(GuardEvent.BLOCKED, "Stanza blocked")

    def __failopen(self):
        """Log a failopen event."""

        self.__emit_event(
            GuardEvent.FAILOPEN, f"Stanza failed open, {self.__error_message}"
        )

    def __consume_cached_token_lease(self) -> Optional[quota_pb2.TokenLease]:
        """Scans cached leases and finds the first valid and unexpired lease."""

        with cached_leases_lock:
            if self.__cached_lease_key not in cached_leases:
                return None

            num_discarded_leases = 0

            # Scan through leases until a valid and unexpired one is found. Any
            # invalid leases found during this process are discarded.
            for i, cached_lease in enumerate(cached_leases[self.__cached_lease_key][:]):
                expiration, lease = cached_lease
                token_status = self.__check_token_lease(lease, expiration)

                if token_status == TokenLeaseStatus.TOKEN_LEASE_VALID:
                    cached_leases[self.__cached_lease_key].pop(i)
                    self.__consume_token_lease(lease)
                    return lease
                elif token_status == TokenLeaseStatus.TOKEN_LEASE_EXPIRED:
                    logging.debug(
                        "Discarding token lease '%s' as it is now expired",
                        lease.token,
                    )
                    cached_leases[self.__cached_lease_key].pop(i - num_discarded_leases)
                    num_discarded_leases += 1
                elif token_status == TokenLeaseStatus.TOKEN_LEASE_WRONG_PRIORITY:
                    logging.debug(
                        "Not using token lease '%s' as the priority boost is above "
                        "the configured priority boost (%d <= %d)",
                        lease.token,
                        self.__priority_boost,
                        lease.priority_boost,
                    )

    def __set_cached_token_leases(self, leases: Iterable[quota_pb2.TokenLease]):
        """Replaces all cached token leases with a new set of leases."""

        leases_with_expiration: list[
            tuple[datetime.datetime, quota_pb2.TokenLease]
        ] = []

        # If Hub doesn't return an expiration date for any of the leases, infer
        # it using the duration_msec field associated with the lease.
        for lease in leases:
            expiration = (
                datetime.datetime.now() + timedelta(milliseconds=lease.duration_msec)
                if lease.expires_at.seconds == 0 and lease.expires_at.nanos == 0
                else (
                    datetime.datetime.fromtimestamp(
                        lease.expires_at.seconds, timezone.utc
                    )
                    + timedelta(microseconds=lease.expires_at.nanos / 2000)
                )
            )
            leases_with_expiration.append((expiration, lease))

        with cached_leases_lock:
            cached_leases[self.__cached_lease_key].extend(leases_with_expiration)

    def __check_token_lease(
        self,
        lease: quota_pb2.TokenLease,
        expiration: datetime.datetime,
    ) -> TokenLeaseStatus:
        """Returns false if a token lease is expired or invalid.

        Both the lease and its expiration are accepted separately. This is done
        since Hub may not specify an expiration date in the lease it returns,
        and we have to create it ourselves. The timestamp fields in the lease
        messages are immutable and cannot be changed at runtime.
        """

        if datetime.datetime.now() >= expiration:
            logging.debug(
                "%s >= %s",
                datetime.datetime.now(),
                expiration,
            )
            return TokenLeaseStatus.TOKEN_LEASE_EXPIRED
        elif self.__priority_boost > lease.priority_boost:
            return TokenLeaseStatus.TOKEN_LEASE_WRONG_PRIORITY
        else:
            return TokenLeaseStatus.TOKEN_LEASE_VALID

    def __consume_token_lease(self, lease: quota_pb2.TokenLease):
        """Marks a token lease as consumed so we can notify Hub later."""

        with consumed_leases_lock:
            consumed_leases[self.__consumed_lease_key].append(lease)

        logging.debug("Currently sitting at %d consumed leases", len(consumed_leases))


def start_batch_token_consumer(event_loop: asyncio.AbstractEventLoop):
    """Continuously run the batch token consumer on the passed in event loop.

    This function should only be wrapped in call_soon_threadsafe() and called
    with the aforementioned event loop.
    """

    def wrapper():
        task = asyncio.create_task(batch_token_consumer())
        task.add_done_callback(handle_batch_token_consumer(event_loop))

    return wrapper


async def batch_token_consumer():
    """Iterates through all consumed tokens and consumes them in batches.

    This function will loop indefinitely by an interval time as defined in
    'BATCH_TOKEN_CONSUME_INTERVAL' (e.g. 200ms).
    """

    global consumed_leases

    logging.debug("Starting batch token consumer background worker")

    while True:
        start_time = time.perf_counter()

        # Quickly snatch and empty out the consumed leases so that we don't block
        # future leases from being consumed while we wait for Hub to finish
        # processing our batch request.
        with consumed_leases_lock:
            seized_leases = consumed_leases
            consumed_leases = defaultdict(list)

        consumption_tasks: list[asyncio.Task] = []

        for environment, leases in seized_leases.items():
            consumption_tasks.append(
                asyncio.create_task(set_token_lease_consumed(leases, environment))
            )

        if len(consumption_tasks) > 0:
            await asyncio.wait(consumption_tasks)

        # We measure the time it takes to consume tokens and subtract that from
        # the interval to ensure that we don't surpass the 200ms deadline as
        # defined in the specification under nominal networking conditions.
        elapsed_time = time.perf_counter() - start_time
        delay = max(BATCH_TOKEN_CONSUME_INTERVAL - elapsed_time, 0)

        if delay > 0:
            await asyncio.sleep(delay)


def handle_batch_token_consumer(event_loop: asyncio.AbstractEventLoop):
    """Gracefully handle and log errors from the background consumer task.

    If the task fails because of an error, it will be rescheduled and continue
    to attempt to send consumed tokens to Hub on an interval.
    """

    # TODO: Retry logic for consumed tokens that we failed to send to Hub?

    def wrapper(task: asyncio.Task):
        global batch_token_consumer_handle

        try:
            task.result()
        except asyncio.CancelledError:
            pass  # Do not log task cancellations.
        except Exception:
            logging.exception("Received unexpected exception while consuming leases")

            with batch_token_consumer_handle_lock:
                batch_token_consumer_handle = event_loop.call_soon_threadsafe(
                    start_batch_token_consumer(event_loop)
                )

    return wrapper


async def set_token_lease_consumed(
    leases: Iterable[quota_pb2.TokenLease],
    environment: str,
):
    """Consume a set of token leases for a given environment."""

    import getstanza.client

    client = getstanza.client.StanzaClient.getInstance()
    if client.hub is None:
        raise RuntimeError("The Stanza SDK has not yet been initialized")

    set_token_lease_consumed_request = quota_pb2.SetTokenLeaseConsumedRequest(
        tokens=list(map(lambda lease: lease.token, leases)),
        environment=environment,
    )
    logging.debug(
        "Consuming %d token leases from environment '%s'",
        len(set_token_lease_consumed_request.tokens),
        environment,
    )

    client.hub.quota_service.SetTokenLeaseConsumed(
        request=set_token_lease_consumed_request,
        metadata=client.config.metadata,
        timeout=DEFAULT_TIMEOUT,
    )
