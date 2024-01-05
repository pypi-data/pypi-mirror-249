class ONEcityAPIException(Exception):
    """Base class for exceptions in this module."""
    pass


class RequestFailedException(ONEcityAPIException):
    """Exception raised for errors in the request.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
