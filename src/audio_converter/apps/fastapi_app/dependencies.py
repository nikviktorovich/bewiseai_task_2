import uuid

import sqlalchemy
import sqlalchemy.engine
from fastapi import Depends

import audio_converter.adapters.uuid
import audio_converter.common.errors
import audio_converter.config
import audio_converter.modules.user.domain.models
import audio_converter.services.converter
import audio_converter.services.users
import audio_converter.services.unit_of_work


def get_database_engine() -> sqlalchemy.engine.Engine:
    connection_url = audio_converter.config.get_postgres_connection_url()
    engine = sqlalchemy.create_engine(url=connection_url)
    return engine


def get_uow(engine: sqlalchemy.engine.Engine = Depends(get_database_engine)):
    """Returns sqlalchemy bound unit of work of users module"""
    uow = audio_converter.services.unit_of_work.SQLAlchemyUnitOfWork(engine)
    with uow:
        yield uow


def get_uuid_provider() -> audio_converter.adapters.uuid.UUIDProvider:
    """Returns an UUID provider"""
    return audio_converter.adapters.uuid.DefaultUUIDProvider()
