class RepositoryError(Exception):
    """Base class for all repository errors"""


class EntityNotFoundError(RepositoryError):
    """Raised when unable to find an entity"""
