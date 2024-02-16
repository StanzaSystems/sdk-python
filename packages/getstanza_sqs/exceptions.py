from botocore.exceptions import BotoCoreError


class GuardError(BotoCoreError):
    """Raised when a guard fails with an error."""

    fmt = "An unspecified guard error occurred"


class GuardBlockedError(BotoCoreError):
    """Raised when a blocked guard is preventing a request from going out."""

    fmt = "Stanza blocked guard {guard_name}"
