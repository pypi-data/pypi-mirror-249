"""Exceptions used by pyarcticspas."""
from http import HTTPStatus


class SpaException(Exception):
    """Base class for all exceptions in the library."""


class InvalidHTTPCodeError(SpaException):
    """Invalid HTTP error code received."""

    code: int


class SpaHTTPException(SpaException):
    """Exceptions that come from the HTTP API."""

    code: int

    def __init__(self, code: int):
        if code < 100 or code > 599:
            raise InvalidHTTPCodeError(code)
        self.code = code

    @property
    def msg(self) -> str:
        """Generate HTTP exception message from code."""
        return HTTPStatus(self.code).phrase


class TooManyRequestsError(SpaHTTPException):
    """Remote API is temporarily overloaded."""


class UnauthorizedError(SpaHTTPException):
    """Authentication failed."""


class ServerError(SpaHTTPException):
    """Remote server issue."""


class ClientError(SpaHTTPException):
    """HTTP client error, not implemented."""


class RedirectionError(SpaHTTPException):
    """HTTP redirections are not implemented."""


class EmptyResponseError(SpaHTTPException):
    """HTTP response did not contain parsed data."""


class InformationError(SpaHTTPException):
    """HTTP information codes are not implemented."""
