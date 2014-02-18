from flask import current_app
from rallycaster.api import api
from rallycaster.helpers.serializers import jsonify_response


@api.errorhandler(Exception)
def catch_all(exc):
    """Catches all exceptions and formats a response"""

    current_app.logger.exception(exc)

    # Determine response HTTP status code depending on the exception type
    if isinstance(exc, AuthException):
        status_code = 401   # Unauthorized
    else:
        status_code = 500   # Internal Server Error

    return jsonify_response(
        status_code=status_code,
        success=False,
        error=str(exc)
    )


@api.errorhandler(404)
def not_found(error):
    return jsonify_response(
        status_code=404,
        success=False,
        error=str(error)
    )


class AuthException(Exception):
    """Exception raised during authentication"""
    pass


class DataException(Exception):
    """Exception raised by database"""
    pass


class CacheException(Exception):
    """Exception raised by memory storage"""
    pass


class InputException(Exception):
    """Exception raised if there was invalid input parameters"""
    pass


class MemStoreException(Exception):
    """Exception raised by memory storage"""
    pass


class EASEException(Exception):
    """Exception raised in EASE services layer"""
    pass
