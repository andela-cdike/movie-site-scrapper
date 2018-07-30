from rest_framework.exceptions import APIException


class SiteFetchException(Exception):
    """Raise this error when fetching the page results in an error"""


class InvalidPageStructureException(Exception):
    """
    Raise this error when there is a AttributeError/IndexError.
    This usually means the page structure has changed
    """


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'


class ServerException(APIException):
    status_code = 500
    default_detail = 'An error occured on the server'
    default_code = 'server_exception'
