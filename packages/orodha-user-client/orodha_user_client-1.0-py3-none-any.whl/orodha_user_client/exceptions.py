"""
Module containing custom exceptions for the orodha_user_client package.
"""
from http import HTTPStatus

class UrlNotFound(Exception):
    """
    Exception that is thrown when a specified URL
    cannot be found in the environment.
    """
    def __init__(self, message: str = "Service url could not be found in environment"):
        self.message = message
        super().__init__(self.message)


class UnexpectedRequestType(Exception):
    """
    Exception for when the request type given to the request factory does not
    match the list of expected requests types, i.e. PUT, POST, GET, DELETE.
    """
    def __init__(self, message: str = None):
        self.message = message
        super().__init__(self.message)


class RequestError(Exception):
    """
    A general exception for when a request to the user service
    fails for any given reason
    """
    def __init__(
        self,
        message: str=None,
        status_code: HTTPStatus=HTTPStatus.BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        super().__init__(f"{self.message}: {self.status_code}")
