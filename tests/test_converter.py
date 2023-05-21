import os
import os.path
import uuid

import pytest

import audio_converter.config
import audio_converter.services.converter


@pytest.mark.usefixtures('detour_media_path')
def test_audio_converter():
    wav_filepath = 'test_wav.wav'
    mp3_uuid = uuid.uuid4().hex

    media_path = audio_converter.config.get_media_path()
    wav_full_path = os.path.join(media_path, wav_filepath)
    mp3_full_path = os.path.join(media_path, f'{mp3_uuid}.mp3')

    with open(wav_full_path, 'rb') as wav_file:
        _ = audio_converter.services.converter.convert_wav_to_mp3(
            wav_file,
            mp3_full_path,
        )
    
    assert os.path.exists(mp3_full_path)
    os.remove(mp3_full_path)
