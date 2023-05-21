import fastapi
from fastapi import Depends
from fastapi import UploadFile

import audio_converter.common.errors
import audio_converter.modules.user.domain.models
import audio_converter.services.converter
from audio_converter.apps.fastapi_app import dependencies
from audio_converter.apps.fastapi_app.routers.audio import serializers
from audio_converter.modules.audio import unit_of_work


router = fastapi.APIRouter(prefix='/record')


@router.post('/')
def add_audio(
    audio: UploadFile,
    request: fastapi.Request,
    user: audio_converter.modules.user.domain.models.User =
        Depends(dependencies.auth_user),
    uow: unit_of_work.AbstractAudioUnitOfWork = Depends(dependencies.get_audio_uow),
):
    if audio.content_type not in ['audio/wav', 'audio/x-wav']:
        raise audio_converter.common.errors.BadAudioFormatError(
            'Wrong audio format, wav-file expected',
        )
    
    converted = audio_converter.services.converter.convert_wav_to_mp3_and_save(
        user=user,
        wav_file=audio.file, # type: ignore
        uow=uow,
    )
    uow.commit()
    
    url = request.url.replace_query_params(
        id=converted.uuid,
        user=user.id,
        access_token=user.access_token,
    )

    return serializers.AudioRead(
        uuid=converted.uuid, # type: ignore
        user_id=converted.user.id,
        audio_url=str(url),
    )
