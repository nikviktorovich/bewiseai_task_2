import uuid

from fastapi import Depends

import audio_converter.adapters.uuid
import audio_converter.common.errors
import audio_converter.modules.user.domain.models
import audio_converter.services.converter
import audio_converter.services.users
import audio_converter.services.unit_of_work


def get_uow():
    """Returns sqlalchemy bound unit of work of users module"""
    uow = audio_converter.services.unit_of_work.UnitOfWork()
    with uow:
        yield uow


def get_uuid_provider() -> audio_converter.adapters.uuid.AbstractUUIDProvider:
    """Returns an UUID provider"""
    return audio_converter.adapters.uuid.DefaultUUIDProvider()
