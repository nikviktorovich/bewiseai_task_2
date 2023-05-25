import fastapi
from fastapi import Depends

import audio_converter.services.unit_of_work
import audio_converter.services.users
from audio_converter.apps.fastapi_app import dependencies
from audio_converter.apps.fastapi_app.routers.users import serializers


router = fastapi.APIRouter(prefix='/users')


@router.post('/')
def add_user(
    user_data: serializers.UserCreate,
    uow: audio_converter.services.unit_of_work.UnitOfWork =
        Depends(dependencies.get_uow),
):
    user = audio_converter.services.users.create_user(
        username=user_data.username,
        uow=uow,
    )
    uow.commit()
    
    return serializers.UserRead(
        id=user.id,
        username=user.username,
        access_token=user.access_token.hex,
    )
