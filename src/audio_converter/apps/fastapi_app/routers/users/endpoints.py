import fastapi
from fastapi import Depends

import audio_converter.services.users
from audio_converter.apps.fastapi_app import dependencies
from audio_converter.apps.fastapi_app.routers.users import serializers
from audio_converter.modules.user import unit_of_work


router = fastapi.APIRouter(prefix='/users')


@router.post('/')
def add_user(
    user_data: serializers.UserCreate,
    uow: unit_of_work.AbstractUserUnitOfWork = Depends(dependencies.get_users_uow),
):
    user = audio_converter.services.users.create_user(
        username=user_data.username,
        uow=uow,
    )
    return serializers.UserRead.from_orm(user)
