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
        guard: str,
        feature: Optional[str] = None,
        priority_boost: Optional[int] = None,
        tags=None,
    ):
        self.name = guard
        self.feature = feature
        self.priority_boost = priority_boost
        self.tags = tags

        self.__start = datetime.now(timezone.utc)
        self.__config: Optional[V1GuardConfig] = None

        # TODO: Use enumerations or constants here, no magic numbers.
        self.__local_status = 0
        self.__quota_status = 0
        self.__token_status = 0

    async def allowed(self) -> bool:
        """Check if the Guard is currently allowing traffic."""

        # Always allow traffic when 'report only' is set.
        if self.__config and self.__config.report_only:
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

    async def blocked(self) -> bool:
        """Check if the Guard is currently disallowing traffic."""

        return not self.allowed()

    async def end(self):
        """Called when the guarded logic comes to an end."""

        pass
