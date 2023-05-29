from typing import Annotated

import fastapi
import fastapi.responses
from fastapi import Depends
from fastapi import Query
from fastapi import UploadFile

import audio_converter.adapters.audio_manager
import audio_converter.adapters.converter
import audio_converter.adapters.uuid
import audio_converter.common.errors
import audio_converter.services.converter
import audio_converter.services.unit_of_work
import audio_converter.services.users
from audio_converter.apps.fastapi_app import dependencies
from audio_converter.apps.fastapi_app.routers.audio import serializers


router = fastapi.APIRouter(prefix='/record')


@router.post('/')
def add_audio(
    user_id: Annotated[int, Query(alias='user')],
    access_token_hex: Annotated[str, Query(alias='access_token')],
    audio: UploadFile,
    request: fastapi.Request,
    uow: audio_converter.services.unit_of_work.UnitOfWork =
        Depends(dependencies.get_uow),
    uuid_provider: audio_converter.adapters.uuid.UUIDProvider =
        Depends(dependencies.get_uuid_provider),
    converter: audio_converter.adapters.converter.AudioConverter =
        Depends(dependencies.get_audio_converter),
    audio_manager: audio_converter.adapters.audio_manager.AudioManager = 
        Depends(dependencies.get_audio_manager),
):
    user = audio_converter.services.users.auth_user(
        user_id=user_id,
        access_token=uuid_provider.parse(access_token_hex),
        uow=uow,
    )

    converted = audio_converter.services.converter.convert_wav_to_mp3_and_save(
        uuid_provider=uuid_provider,
        converter=converter,
        audio_manager=audio_manager,
        wav_file=audio.file,
        user=user,
        uow=uow,
    )
    uow.commit()
    
    # Making a wav-file url
    url = request.url.replace_query_params(
        id=converted.uuid.hex,
        user=user.id,
        access_token=user.access_token.hex,
    )

    return serializers.AudioRead(
        uuid=converted.uuid.hex,
        user_id=converted.user.id,
        audio_url=str(url),
    )


@router.get('/')
def get_audio(
    audio_uuid_hex: Annotated[str, Query(alias='id')],
    user_id: Annotated[int, Query(alias='user')],
    access_token_hex: Annotated[str, Query(alias='access_token')],
    uow: audio_converter.services.unit_of_work.UnitOfWork =
        Depends(dependencies.get_uow),
    uuid_provider: audio_converter.adapters.uuid.UUIDProvider =
        Depends(dependencies.get_uuid_provider),
    audio_manager: audio_converter.adapters.audio_manager.AudioManager = 
        Depends(dependencies.get_audio_manager),
):
    user = audio_converter.services.users.auth_user(
        user_id=user_id,
        access_token=uuid_provider.parse(access_token_hex),
        uow=uow,
    )

    audio = uow.audio.get(
        audio_uuid=uuid_provider.parse(audio_uuid_hex),
    )

    if audio.user != user:
        raise audio_converter.common.errors.AuthError(
            f'You are not the owner of the audio',
        )

    managed_stream = audio_manager.load_iterator(audio)
    return fastapi.responses.StreamingResponse(
        managed_stream,
        media_type='audio/mpeg',
    )
