import logging
from typing import Iterable, Optional

from getstanza.common import GuardedStatus, LocalStatus, QuotaStatus, TokenStatus
from getstanza.configuration import StanzaConfiguration
from getstanza.errors.hub import hub_error
from stanza.hub.v1 import common_pb2, config_pb2, quota_pb2, quota_pb2_grpc


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
        guard_name: str,
        feature_name: Optional[str] = None,
        priority_boost: Optional[int] = None,
        default_weight: Optional[float] = None,
        tags=None,
    ):
        self.stanza_config = stanza_config
        self.guard_config = guard_config
        self.guard_name = guard_name
        self.feature_name = feature_name
        self.priority_boost = priority_boost
        self.default_weight = default_weight
        self.tags = tags

        self.success = GuardedStatus.GUARDED_SUCCESS
        self.failure = GuardedStatus.GUARDED_FAILURE

        self.__quota_service = quota_service
        self.__quota_token: Optional[str] = None

        self.__local_status = LocalStatus.LOCAL_UNSPECIFIED
        self.__quota_status = QuotaStatus.QUOTA_UNSPECIFIED
        self.__token_status = TokenStatus.TOKEN_UNSPECIFIED

        self.__cached_leases: list[quota_pb2.TokenLease] = []

    async def run(self, tokens: Optional[Iterable[str]] = None):
        """Run all guard checks and update guard statuses."""

        # Config state check
        # TODO

        # Local (Sentinel) check
        self.check_local()

        # Ingress token check
        self.check_token(tokens)

        # Quota check
        await self.check_quota()

    def check_local(self):
        """Check using Sentinel."""
        self.__local_status = LocalStatus.LOCAL_NOT_SUPPORTED

    def check_token(self, tokens: Optional[Iterable[str]] = None) -> int:
        """Validate using the ingress token if configured to do so."""

        if not self.guard_config.validate_ingress_tokens:
            self.__token_status = TokenStatus.TOKEN_EVAL_DISABLED
            return self.__token_status

        raise NotImplementedError

    async def check_quota(self) -> int:
        """Quota check using token leases."""

        if not self.guard_config.check_quota:
            self.__quota_status = QuotaStatus.QUOTA_EVAL_DISABLED
            return self.__quota_status

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
        except Exception as exc:
            raise hub_error(exc) from exc

        if token_lease_response.granted:
            if len(token_lease_response.leases) > 1:
                # TODO: cache extra leases
                logging.debug("Extra leases: %s", len(token_lease_response.leases) - 1)

            self.__quota_token = token_lease_response.leases[0].token
            self.__quota_status = QuotaStatus.QUOTA_GRANTED
        else:
            self.__quota_status = QuotaStatus.QUOTA_BLOCKED

        return self.__quota_status

    def error(self) -> str:
        """If there was an error, return the message as a string."""
        return ""

    def allowed(self) -> bool:
        """Check if the Guard is currently allowing traffic."""

        # Always allow traffic when 'report only' is set.
        if self.guard_config and self.guard_config.report_only:
            return True

        # Allow if all of the following checks have succeeded.
        if (
            self.__local_status != LocalStatus.LOCAL_BLOCKED
            and self.__quota_status != QuotaStatus.QUOTA_BLOCKED
            and self.__token_status != TokenStatus.TOKEN_NOT_VALID
        ):
            return True

        # Disallow by default.
        return False

    def blocked(self) -> bool:
        """Check if the Guard is currently disallowing traffic."""

        return not self.allowed()

    def block_message(self) -> str:
        """Returns the reason for the block as a human readable string."""
        if self.__local_status is LocalStatus.LOCAL_BLOCKED:
            return ""

        if self.__token_status is TokenStatus.TOKEN_NOT_VALID:
            return "Invalid or expired X-Stanza-Token."

        if self.__quota_status is QuotaStatus.QUOTA_BLOCKED:
            return "Stanza quota exhausted. Please try again later."

        return ""

    def block_reason(self) -> str:
        """Returns the reason for the block as an enum."""

        if self.__local_status is LocalStatus.LOCAL_BLOCKED:
            return str(LocalStatus.LOCAL_BLOCKED)

        if self.__token_status is TokenStatus.TOKEN_NOT_VALID:
            return str(TokenStatus.TOKEN_NOT_VALID)

        if self.__quota_status is QuotaStatus.QUOTA_BLOCKED:
            return str(QuotaStatus.QUOTA_BLOCKED)

        return ""

    def quota_token(self) -> str:
        """Returns the quota token for this request."""
        return self.__quota_token

    def end(self, status: int):
        """Called when the guarded logic comes to an end."""
