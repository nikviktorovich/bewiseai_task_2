from typing import BinaryIO

import audio_converter.adapters.audio_manager
import audio_converter.adapters.converter
import audio_converter.adapters.uuid
import audio_converter.modules.audio.domain.models
import audio_converter.modules.user.domain.models
import audio_converter.services.unit_of_work


def convert_wav_to_mp3_and_save(
    uuid_provider: audio_converter.adapters.uuid.UUIDProvider,
    converter: audio_converter.adapters.converter.AudioConverter,
    audio_manager: audio_converter.adapters.audio_manager.AudioManager,
    wav_file: BinaryIO,
    user: audio_converter.modules.user.domain.models.User,
    uow: audio_converter.services.unit_of_work.UnitOfWork,
) -> audio_converter.modules.audio.domain.models.Audio:
    """Converts wav audio file to mp3 and saves it to database
    
    Args:
        uuid_provider: uuid provider adapter instance
        converter: audio converter adapter instance
        audio_manager: audio manager adapter instance
        wav_file: wav file stream to convert from
        user: user domain model
        uow: unit of work instance

    Returns:
        Generated mp3 file db entry

    Raises:
        audio_converter.common.errors.BadAudioFormatError: If the file is
            an invalid wav-file
    """
    mp3_uuid = uuid_provider.generate()

    with converter.convert(wav_file) as mp3_stream:
        instance = audio_manager.save(
            audio_uuid=mp3_uuid,
            user=user,
            audio_stream=mp3_stream,
        )
    
    uow.audio.add(instance)
    
    return instance
