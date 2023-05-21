import uuid

import audio_converter.common.errors
import audio_converter.services.uuid_generator
from audio_converter.modules.user.domain import models
from audio_converter.modules.user import unit_of_work


def create_user(
    username: str,
    uow: unit_of_work.AbstractUserUnitOfWork,
) -> models.User:
    access_token = audio_converter.services.uuid_generator.generate_uuid()
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
    uow: unit_of_work.AbstractUserUnitOfWork,
) -> models.User:
    user = uow.users.get(user_id)

    if user.access_token != access_token:
        raise audio_converter.common.errors.InvalidAccessTokenError(
            'Provided access token is invalid',
        )
    
    return user
