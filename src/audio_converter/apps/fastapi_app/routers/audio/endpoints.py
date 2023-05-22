import uuid
from typing import Annotated

import fastapi
import fastapi.responses
from fastapi import Depends
from fastapi import Query
from fastapi import UploadFile

import audio_converter.common.errors
import audio_converter.services.converter
import audio_converter.services.unit_of_work
import audio_converter.services.users
import audio_converter.services.uuid
from audio_converter.apps.fastapi_app import dependencies
from audio_converter.apps.fastapi_app.routers.audio import serializers


router = fastapi.APIRouter(prefix='/record')


@router.post('/')
def add_audio(
    user_id: Annotated[int, Query(alias='user')],
    access_token_hex: Annotated[str, Query(alias='access_token')],
    audio: UploadFile,
    request: fastapi.Request,
    uow: audio_converter.services.unit_of_work.AbstractUnitOfWork =
        Depends(dependencies.get_uow),
):
    if audio.content_type not in ['audio/wav', 'audio/x-wav']:
        raise audio_converter.common.errors.BadAudioFormatError(
            'Wrong audio format, wav-file expected',
        )

    user = audio_converter.services.users.auth_user(
        user_id=user_id,
        access_token=audio_converter.services.uuid.parse_uuid(hex=access_token_hex),
        uow=uow,
    )

    converted = audio_converter.services.converter.convert_wav_to_mp3_and_save(
        user=user,
        wav_file=audio.file, # type: ignore
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
    uow: audio_converter.services.unit_of_work.AbstractUnitOfWork =
        Depends(dependencies.get_uow),
):
    user = audio_converter.services.users.auth_user(
        user_id=user_id,
        access_token=audio_converter.services.uuid.parse_uuid(hex=access_token_hex),
        uow=uow,
    )

    audio = uow.audio.get(
        audio_uuid=audio_converter.services.uuid.parse_uuid(hex=audio_uuid_hex),
    )

    if audio.user != user:
        raise audio_converter.common.errors.AuthError(
            f'You are not the owner of the audio',
        )

    audio_path = audio_converter.services.converter.get_audio_path(audio)
    return fastapi.responses.FileResponse(audio_path, media_type='audio/mpeg')
