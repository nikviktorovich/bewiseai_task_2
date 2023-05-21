import fastapi
from fastapi import Depends

import audio_converter.modules.audio.unit_of_work
import audio_converter.modules.user.domain.models
import audio_converter.modules.user.unit_of_work
import audio_converter.services.users


def get_users_uow():
    """Returns sqlalchemy bound unit of work of users module"""
    uow = audio_converter.modules.user.unit_of_work.SQLAlchemyUserUnitOfWork()
    with uow:
        yield uow


def get_audio_uow():
    """Returns sqlalchemy bound unit of work of audio module"""
    uow = audio_converter.modules.audio.unit_of_work.SQLAlchemyAudioUnitOfWork()
    with uow:
        yield uow


def get_user_by_id(
    user: int,
    uow: audio_converter.modules.user.unit_of_work.AbstractUserUnitOfWork =
        Depends(get_users_uow),
) -> audio_converter.modules.user.domain.models.User:
    return uow.users.get(user)


def get_user_by_access_token(
    access_token: str,
    uow: audio_converter.modules.user.unit_of_work.AbstractUserUnitOfWork =
        Depends(get_users_uow),
) -> audio_converter.modules.user.domain.models.User:
    return uow.users.get_by_token(access_token)


def auth_user(
    user: int,
    access_token: str,
    uow: audio_converter.modules.user.unit_of_work.AbstractUserUnitOfWork =
        Depends(get_users_uow),
) -> audio_converter.modules.user.domain.models.User:
    return audio_converter.services.users.auth_user(
        user_id=user,
        access_token=access_token,
        uow=uow,
    )
