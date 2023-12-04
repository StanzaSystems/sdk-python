from enum import Enum


class GuardedStatus(Enum):
    """Indicate success or failure of the guarded code block"""

    GUARDED_UNKNOWN = 0
    GUARDED_SUCCESS = 1
    GUARDED_FAILURE = 2


class LocalStatus(Enum):
    """Local related guard reasons used by Stanza SDKs"""

    LOCAL_UNSPECIFIED = 0
    LOCAL_NOT_SUPPORTED = 1
    LOCAL_NOT_EVAL = 2
    LOCAL_EVAL_DISABLED = 3
    LOCAL_ALLOWED = 4
    LOCAL_BLOCKED = 5
    LOCAL_ERROR = 6


class TokenStatus(Enum):
    """Token related guard reasons used by Stanza SDKs"""

    TOKEN_UNSPECIFIED = 0
    TOKEN_NOT_EVAL = 1
    TOKEN_EVAL_DISABLED = 2
    TOKEN_NOT_VALID = 3
    TOKEN_VALID = 4
    TOKEN_VALIDATION_ERROR = 5
    TOKEN_VALIDATION_TIMEOUT = 6


class QuotaStatus(Enum):
    """Quota related guard reasons used by Stanza SDKs"""

    QUOTA_UNSPECIFIED = 0
    QUOTA_NOT_EVAL = 1
    QUOTA_EVAL_DISABLED = 2
    QUOTA_LOCAL_ERROR = 3
    QUOTA_BLOCKED = 4
    QUOTA_GRANTED = 5
    QUOTA_ERROR = 6
    QUOTA_TIMEOUT = 7
