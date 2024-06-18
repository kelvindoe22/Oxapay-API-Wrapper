import json
from requests.exceptions import RequestException

class OxapayError(Exception):
    """Base error for all exceptions in this library."""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class ParamRequiredError(OxapayError):
    """Raised when a required parameter is not included in a request"""
    def __init__(self, param, action):
        super().__init__("{} parameter required to {}".format(param, action))
    
class APIError(OxapayError):
    """Raised for errors related to interacting with the Oxapay server"""
    def __init__(self, status_code, body, json_body):
        self.status_code = status_code
        self.body = body
        self.json_body = json_body
    
        super().__init__("Status code {} : {}".format(self.status_code, json_body['message']))

class ConnectionError(OxapayError):
    """Raised for errors when trying to connect to Oxapay server"""
    def __init__(self, exception):
        if isinstance(exception, RequestException):
            msg = "Unexpected error communicating with Oxapay"
            err = "{} : {}".format(type(exception).__name__, str(exception))
        else:
            msg = (
                "Unexpected error communicating with Oxapay. "
                "Local Configuration Issue"
            )
            err = "A {} was raised".format(type(exception).__name__)
            if str():
                err += " with error message {}".format(str(exception))
            else:
                err += " with no error message"
        super().__init__(msg + '\n\n' + err) 

class InvalidResponseError(OxapayError):
    def __init__(self):
        super().__init__("Invalid response received from server. Please try again in a few minutes")