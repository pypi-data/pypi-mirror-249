"""Exceptions for Forager project."""


class ForagerError(Exception):
    """General exception for project."""


class ArgumentError(ForagerError):
    """Error with not correct arguments."""


class ArgumentValidationError(ForagerError):
    """Validation error, wrong type etc."""


class ForagerAPIError(ForagerError):
    """API error."""


class ForagerKeyError(ForagerError):
    """Error, if key presents in storage."""
