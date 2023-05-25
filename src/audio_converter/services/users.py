import uuid

import audio_converter.common.errors
import audio_converter.services.uuid
import audio_converter.services.unit_of_work
from audio_converter.modules.user.domain import models


def create_user(
    username: str,
    uow: audio_converter.services.unit_of_work.UnitOfWork,
) -> models.User:
    existing_users = uow.users.list(username=username)

    if existing_users:
        raise audio_converter.common.errors.EntityAlreadyExists(
            f'User with this username is already exists',
        )

    access_token = audio_converter.services.uuid.generate_uuid()
    user = models.User(
        id=None,
        username=username,
        access_token=access_token,
    )
    created_user = uow.users.add(user)
    return created_user


def auth_user(
    user_id: int,
    access_token: uuid.UUID,
    uow: audio_converter.services.unit_of_work.UnitOfWork,
) -> models.User:
    user = uow.users.get(user_id)

    if user.access_token != access_token:
        raise audio_converter.common.errors.InvalidAccessTokenError(
            'Provided access token is invalid',
        )
    
    return user
