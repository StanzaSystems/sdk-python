from datetime import datetime, timezone
from typing import Optional

from getstanza.hub.models.v1_guard_config import V1GuardConfig


class Guard:
    """
    Generic Guard class that implements logic for interacting with Stanza
    Guards. All framework-specific logic is kept out of this implementation.
    """

    def __init__(
        self,
        config: V1GuardConfig,
        guard_name: str,
        feature_name: Optional[str] = None,
        priority_boost: Optional[int] = None,
        tags=None,
    ):
        self.config = config
        self.guard_name = guard_name
        self.feature_name = feature_name
        self.priority_boost = priority_boost
        self.tags = tags

        self.__start = datetime.now(timezone.utc)

        # TODO: Use enumerations or constants here, no magic numbers.
        self.__local_status = 0
        self.__quota_status = 0
        self.__token_status = 0

    def allowed(self) -> bool:
        """Check if the Guard is currently allowing traffic."""

        # Always allow traffic when 'report only' is set.
        if self.config and self.config.report_only:
            return True

        # Allow if all of the following checks have succeeded.
        # if (
        #     self.__local_status != Local.LOCAL_BLOCKED
        #     and self.__quota_status != Quota.QUOTA_BLOCKED
        #     and self.__token_status != Token.TOKEN_NOT_VALID
        # ):
        #     return True

        # Disallow by default.
        return False

    def blocked(self) -> bool:
        """Check if the Guard is currently disallowing traffic."""

        return not self.allowed()

    def end(self):
        """Called when the guarded logic comes to an end."""
