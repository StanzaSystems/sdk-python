import datetime
import logging
from enum import Enum
from typing import Iterable, Optional

import grpc
from getstanza.configuration import StanzaConfiguration
from stanza.hub.v1 import common_pb2, config_pb2, quota_pb2, quota_pb2_grpc
from stanza.hub.v1.common_pb2 import Config, Local, Quota, Token


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

    def __init__(
        self,
        quota_service: quota_pb2_grpc.QuotaServiceStub,
        stanza_config: StanzaConfiguration,
        guard_config: config_pb2.GuardConfig,
        guard_config_status: Config,
        guard_name: str,
        feature_name: Optional[str] = None,
        priority_boost: Optional[int] = None,
        default_weight: Optional[float] = None,
        tags=None,
    ):
        self.stanza_config = stanza_config
        self.guard_name = guard_name
        self.feature_name = feature_name
        self.priority_boost = priority_boost
        self.default_weight = default_weight
        self.tags = tags

        self.success = GuardedStatus.GUARDED_SUCCESS
        self.failure = GuardedStatus.GUARDED_FAILURE

        self.__guard_config = guard_config
        self.__quota_service = quota_service
        self.__quota_token: Optional[str] = None

        self.__config_status = guard_config_status
        self.__local_status = Local.LOCAL_NOT_EVAL
        self.__token_status = Token.TOKEN_NOT_EVAL
        self.__quota_status = Quota.QUOTA_NOT_EVAL

        self.__cached_leases: list[quota_pb2.TokenLease] = []

        self.__error_message = None
        self.__start = None

    async def run(self, tokens: Optional[Iterable[str]] = None):
        """Run all guard checks and update guard statuses."""

        try:
            # Config state check
            if not self.__check_config():
                return

            # Local check
            if not self.__check_local():
                return

            # Ingress token check
            if not await self.__check_token(tokens):
                return

            # Quota check
            await self.__check_quota()

        finally:
            if not self.__error_message:
                if self.allowed():
                    self.__allowed()
                else:
                    self.__blocked()

    def __log(self) -> str:
        return "guard={}, config_state={}, local_reason={}, token_reason={}, quota_reason={}".format(
            self.guard_name,
            Config.Name(self.__config_status),
            Local.Name(self.__local_status),
            Token.Name(self.__token_status),
            Quota.Name(self.__quota_status),
        )

    def __allowed(self):
        # TODO: OTEL meter (AllowedCount) and trace span
        logging.debug("Stanza allowed, %s", self.__log())
        self.__start = datetime.datetime.now()

    def __blocked(self):
        # TODO: OTEL meter (BlockedCount) and trace span
        logging.debug("Stanza blocked, %s", self.__log())

    def __failopen(self, error_message: str) -> bool:
        # TODO: OTEL meter (FailOpenCount) and trace span
        self.__error_message = error_message
        logging.debug(error_message)
        logging.debug("Stanza failed open, %s", self.__log())
        return False

    def __check_config(self) -> bool:
        """Check guard configuration."""
        if self.__guard_config is not None:
            return True
        else:
            return self.__failopen(Config.Name(self.__config_status))

    def __check_local(self) -> bool:
        """Local check is not currently supported by this SDK."""
        self.__local_status = Local.LOCAL_NOT_SUPPORTED
        return True

    async def __check_token(self, tokens: Optional[Iterable[str]] = None) -> bool:
        """Validate using the ingress token if configured to do so."""

        if not self.__guard_config.validate_ingress_tokens:
            self.__token_status = Token.TOKEN_EVAL_DISABLED
            return True

        if not tokens:
            self.__token_status = Token.TOKEN_NOT_VALID
            return False

        tokens_info: Iterable[quota_pb2.TokenInfo] = []
        for token in tokens:
            tokens_info.append(
                quota_pb2.TokenInfo(
                    token=token,
                    guard=common_pb2.GuardSelector(
                        name=self.guard_name, environment=self.stanza_config.environment
                    ),
                )
            )

        validate_token_request = quota_pb2.ValidateTokenRequest(tokens=tokens_info)
        try:
            validate_token_response = self.__quota_service.ValidateToken(
                request=validate_token_request,
                metadata=self.stanza_config.metadata,
            )
        except grpc.RpcError as rpc_error:
            return self.__failopen(rpc_error.debug_error_string())  # type: ignore

        return validate_token_response.valid

    async def __check_quota(self) -> bool:
        """Quota check using token leases."""

        if not self.__guard_config.check_quota:
            self.__quota_status = Quota.QUOTA_EVAL_DISABLED
            return True

        # TODO: Check baggage for stz-feat and stz-boost

        # TODO: Check for matching cached leases first

        token_lease_request = quota_pb2.GetTokenLeaseRequest(
            selector=common_pb2.GuardFeatureSelector(
                guard_name=self.guard_name,
                feature_name=self.feature_name,
                environment=self.stanza_config.environment,
                tags=[],
            ),
            client_id=self.stanza_config.client_id,
            priority_boost=self.priority_boost,
            default_weight=self.default_weight,
        )

        try:
            token_lease_response = self.__quota_service.GetTokenLease(
                request=token_lease_request,
                metadata=self.stanza_config.metadata,
            )
        except grpc.RpcError as rpc_error:
            return self.__failopen(rpc_error.debug_error_string())  # type: ignore

        if token_lease_response.granted:
            if len(token_lease_response.leases) > 1:
                # TODO: cache extra leases
                logging.debug("Extra leases: %s", len(token_lease_response.leases) - 1)

            self.__quota_token = token_lease_response.leases[0].token
            self.__quota_status = Quota.QUOTA_GRANTED
            return True
        else:
            self.__quota_status = Quota.QUOTA_BLOCKED
            return False

    def error(self) -> Optional[str]:
        """If there was an error, return the message as a string."""
        return self.__error_message

    def allowed(self) -> bool:
        """Check if the Guard is currently allowing traffic."""

        # Always allow traffic when 'report only' is set.
        if self.__guard_config and self.__guard_config.report_only:
            return True

        # Allow if all of the following checks have succeeded.
        if (
            self.__local_status != Local.LOCAL_BLOCKED
            and self.__quota_status != Quota.QUOTA_BLOCKED
            and self.__token_status != Token.TOKEN_NOT_VALID
        ):
            return True

        # Disallow by default.
        return False

    def blocked(self) -> bool:
        """Check if the Guard is currently disallowing traffic."""

        return not self.allowed()

    def block_message(self) -> Optional[str]:
        """Returns the reason for the block as a human readable string."""
        if self.__local_status is Local.LOCAL_BLOCKED:
            return "Local resource exhausted. Please try again later."

        if self.__token_status is Token.TOKEN_NOT_VALID:
            return "Invalid or expired X-Stanza-Token."

        if self.__quota_status is Quota.QUOTA_BLOCKED:
            return "Stanza quota exhausted. Please try again later."

        return None

    def block_reason(self) -> Optional[str]:
        """Returns the reason for the block as a string."""

        if self.__local_status is Local.LOCAL_BLOCKED:
            return Local.Name(self.__local_status)

        if self.__token_status is Token.TOKEN_NOT_VALID:
            return Token.Name(self.__token_status)

        if self.__quota_status is Quota.QUOTA_BLOCKED:
            return Quota.Name(self.__quota_status)

        return None

    def quota_token(self) -> Optional[str]:
        """Returns the quota token for this request."""
        return self.__quota_token

    def end(self, status: int):
        """Called when the guarded logic comes to an end."""
