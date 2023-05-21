class AuthError(Exception):
    """Base class for all auth errors"""


class InvalidAccessTokenError(AuthError):
    """Invalid access token error"""
