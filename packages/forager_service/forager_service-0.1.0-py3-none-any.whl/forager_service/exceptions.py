"""Exceptions for Forager project."""


class ForagerException(Exception):
    """General exception for project."""

    pass


class ArgumentError(ForagerException):
    """Error with not correct arguments."""

    pass


class ArgumentValidationError(ForagerException):
    """Validation error, wrong type etc."""

    pass


class ForagerAPIError(ForagerException):
    """API error."""

    pass


class ForagerKeyError(ForagerException):
    """Error, if key presents in storage."""

    pass
