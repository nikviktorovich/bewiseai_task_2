import io
import os.path
import uuid

import pydub
import pydub.exceptions

import audio_converter.config
import audio_converter.modules.audio.domain.models
import audio_converter.modules.audio.unit_of_work
import audio_converter.modules.user.domain.models


def convert_wav_to_mp3(wav_file: io.IOBase, mp3_filepath: str) -> str:
    """Converts wav audio file to mp3 and returns filepath to the mp3
    
    Args:
        wav_file: wav file handler
        mp3_filepath: path to the new generated mp3-file
    
    Returns:
        Result mp3-file path relative to the media path

    Raises:
        pydub.exceptions.CouldntDecodeError: If the file is an invalid wav-file
    """
    wav_segment: pydub.AudioSegment = pydub.AudioSegment.from_wav(wav_file)
    wav_segment.export(mp3_filepath)
    return mp3_filepath


def convert_wav_to_mp3_and_save(
    user: audio_converter.modules.user.domain.models.User,
    wav_file: io.IOBase,
    uow: audio_converter.modules.audio.unit_of_work.AbstractAudioUnitOfWork,
) -> str:
    """Converts wav audio file to mp3, saves it to a file and into a database
    
    Args:
        wav_file: wav file handler

    Returns:
        Generated mp3 file path relative to the media path

    Raises:
        pydub.exceptions.CouldntDecodeError: If the file is an invalid wav-file
    """
    mp3_uuid = uuid.uuid4().hex
    mp3_relative_path = f'{mp3_uuid}.mp3'
    mp3_filepath = _get_media_file_path(mp3_relative_path)
    convert_wav_to_mp3(wav_file, mp3_filepath)
    _save_mp3_to_db(
        user=user,
        mp3_uuid=mp3_uuid,
        mp3_filepath=mp3_filepath,
        uow=uow,
    )
    return mp3_relative_path


def _save_mp3_to_db(
    user: audio_converter.modules.user.domain.models.User,
    mp3_uuid: str,
    mp3_filepath: str,
    uow: audio_converter.modules.audio.unit_of_work.AbstractAudioUnitOfWork,
) -> None:
    instance = audio_converter.modules.audio.domain.models.Audio(
        uuid=mp3_uuid,
        user_id=user.id,
        user=user,
        audio_filepath=mp3_filepath,
    )
    uow.audio.add(instance)


def _get_media_file_path(filepath: str) -> str:
    media_path = audio_converter.config.get_media_path()
    return os.path.join(media_path, filepath)
