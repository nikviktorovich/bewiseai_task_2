from typing import List

import sqlalchemy.orm

import audio_converter.common.errors
from audio_converter.modules.audio.domain import models


class AbstractAudioRepository:
    """Abstract audio repository"""
    def list(self, **filters) -> List[models.Audio]:
        """Returns list of all matching instances
        
        Args:
            filters: Keyword request filters
        """
        raise NotImplementedError()
    

    def get(self, audio_uuid: str) -> models.Audio:
        """Returns an instance with the specified id
        
        Raises:
            EntityNotFoundError: If unable to find the specified entity
        """
        raise NotImplementedError()


    def add(self, instance: models.Audio) -> models.Audio:
        """Adds an instance to repository"""
        raise NotImplementedError()


class SQLAlchemyAudioRepository(AbstractAudioRepository):
    """Audio repository implementation bound to SQLAlchemy session"""
    session: sqlalchemy.orm.Session


    def __init__(self, session: sqlalchemy.orm.Session) -> None:
        self.session = session


    def _get_instance_set(self) -> sqlalchemy.orm.Query:
        return self.session.query(models.Audio)


    def list(self, **filters) -> List[models.Audio]:
        instances = self._get_instance_set().filter_by(**filters).all()
        return instances
    

    def get(self, audio_uuid: str) -> models.Audio:
        instance = self._get_instance_set().filter_by(uuid=audio_uuid).first()
        
        if instance is None:
            raise audio_converter.common.errors.EntityNotFoundError(
                f'Unable to find an audio with id={audio_uuid}',
            )
        
        return instance
    

    def add(self, instance: models.Audio) -> models.Audio:
        self.session.add(instance)
        return instance
