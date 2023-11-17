class GuardError(Exception):
    """Base class of all guard related exceptions."""

    def __init__(self) -> None:
        super().__init__("")
