from typing import List

import sqlalchemy.orm

import audio_converter.common.errors
from audio_converter.modules.user.domain import models


class AbstractUserRepository:
    """Abstract user repository"""
    def list(self, **filters) -> List[models.User]:
        """Returns list of all matching instances
        
        Args:
            filters: Keyword request filters
        """
        raise NotImplementedError()
    

    def get(self, user_id: int) -> models.User:
        """Returns an instance with the specified id
        
        Raises:
            EntityNotFoundError: If unable to find the specified entity
        """
        raise NotImplementedError()
    

    def get_by_token(self, access_token: str) -> models.User:
        """Returns an instance with the specified access token
        
        Raises:
            EntityNotFoundError: If unable to find the specified user by token
        """
        raise NotImplementedError()


    def add(self, instance: models.User) -> models.User:
        """Adds an instance to repository"""
        raise NotImplementedError()


class SQLAlchemyUserRepository(AbstractUserRepository):
    """User repository implementation bound to SQLAlchemy session"""
    session: sqlalchemy.orm.Session


    def __init__(self, session: sqlalchemy.orm.Session) -> None:
        self.session = session


    def _get_instance_set(self) -> sqlalchemy.orm.Query:
        return self.session.query(models.User)


    def list(self, **filters) -> List[models.User]:
        instances = self._get_instance_set().filter_by(**filters).all()
        return instances
    

    def get(self, user_id: int) -> models.User:
        instance = self._get_instance_set().filter_by(id=user_id).first()
        
        if instance is None:
            raise audio_converter.common.errors.EntityNotFoundError(
                f'Unable to find a user with id={user_id}',
            )
        
        return instance
    

    def get_by_token(self, access_token: str) -> models.User:
        instances = self._get_instance_set().filter_by(access_token=access_token)
        instance = instances.first()
        
        if instance is None:
            raise audio_converter.common.errors.EntityNotFoundError(
                f'Unable to find a user with access_token={access_token}',
            )
        
        return instance
    

    def add(self, instance: models.User) -> models.User:
        self.session.add(instance)
        return instance
