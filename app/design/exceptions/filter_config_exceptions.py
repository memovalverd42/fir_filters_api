"""
Filter Configuration exceptions
"""


class FilterConfValidationError(Exception):
    """Base class for all filter configuration validation errors."""


class MissingKeysError(FilterConfValidationError):
    """Raised when required keys are missing in the configuration."""

    def __init__(self, missing_keys: list[str]):
        super().__init__(f"Missing required keys: {', '.join(missing_keys)}")
        self.missing_keys = missing_keys


class IncorrectTypeError(FilterConfValidationError):
    """Raised when a key has an incorrect type."""

    def __init__(self, incorrect_keys: list[str]):
        super().__init__(f"Incorrect types for keys: {', '.join(incorrect_keys)}")
        self.incorrect_keys = incorrect_keys
