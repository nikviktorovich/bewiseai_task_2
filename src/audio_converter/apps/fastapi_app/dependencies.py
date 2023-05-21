import uuid

from fastapi import Depends

import audio_converter.common.errors
import audio_converter.modules.audio.unit_of_work
import audio_converter.modules.user.domain.models
import audio_converter.modules.user.unit_of_work
import audio_converter.services.users
import audio_converter.services.converter


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


def get_audio_and_user_uow():
    """Returns sqlalchemy bound unit of work of audio and user modules"""
    uow = audio_converter.modules.audio.unit_of_work.SQLAlchemyAudioAndUserUnitOfWork()
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


def get_audio_path(
    id: str,
    user: int,
    access_token: str,
    uow: audio_converter.modules.audio.unit_of_work.AbstractAudioAndUserUnitOfWork =
        Depends(get_audio_and_user_uow),
) -> str:
    user_instance = audio_converter.services.users.auth_user(
        user_id=user,
        access_token=uuid.UUID(hex=access_token),
        uow=uow,
    )

    audio_uuid = uuid.UUID(hex=id)
    audio = uow.audio.get(audio_uuid)

    if audio.user.access_token != user_instance.access_token:
        raise audio_converter.common.errors.AuthError(
            'You have no access to this audio file',
        )

    audio_abs_path = audio_converter.services.converter._get_media_file_path(
        audio.audio_filepath,
    )
    return audio_abs_path
