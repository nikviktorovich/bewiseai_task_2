import os.path
import uuid

import fastapi
import fastapi.responses
from fastapi import Depends
from fastapi import UploadFile

import audio_converter.common.errors
import audio_converter.modules.user.domain.models
import audio_converter.services.converter
import audio_converter.services.users
from audio_converter.apps.fastapi_app import dependencies
from audio_converter.apps.fastapi_app.routers.audio import serializers
from audio_converter.modules.audio import unit_of_work


router = fastapi.APIRouter(prefix='/record')


@router.post('/')
def add_audio(
    audio: UploadFile,
    user: int,
    access_token: str,
    request: fastapi.Request,
    uow: unit_of_work.AbstractAudioAndUserUnitOfWork =
        Depends(dependencies.get_audio_and_user_uow),
):
    if audio.content_type not in ['audio/wav', 'audio/x-wav']:
        raise audio_converter.common.errors.BadAudioFormatError(
            'Wrong audio format, wav-file expected',
        )

    user_instance = audio_converter.services.users.auth_user(
        user_id=user,
        access_token=uuid.UUID(hex=access_token),
        uow=uow,
    )

    converted = audio_converter.services.converter.convert_wav_to_mp3_and_save(
        user=user_instance,
        wav_file=audio.file, # type: ignore
        uow=uow,
    )
    uow.commit()
    
    url = request.url.replace_query_params(
        id=converted.uuid.hex,
        user=user_instance.id,
        access_token=user_instance.access_token.hex,
    )

    return serializers.AudioRead(
        uuid=converted.uuid, # type: ignore
        user_id=converted.user.id,
        audio_url=str(url),
    )


@router.get('/')
def get_audio(
    audio_path: str = Depends(dependencies.get_audio_path)
):
    if not os.path.exists(audio_path):
        raise FileNotFoundError('Unable to find the specified record')

    return fastapi.responses.FileResponse(audio_path, media_type='audio/mpeg')
