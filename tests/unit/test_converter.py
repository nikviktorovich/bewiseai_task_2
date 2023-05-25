import os
import os.path

import pytest

import audio_converter.adapters.uuid
import audio_converter.config
import audio_converter.modules.user.domain.models
import audio_converter.services.converter
import audio_converter.services.uuid
from .. import common


@pytest.mark.usefixtures('detour_media_path')
def test_audio_converter(
    uuid_provider: audio_converter.adapters.uuid.UUIDProvider,
):
    test_user = audio_converter.modules.user.domain.models.User(
        id=1,
        username='someuser',
        access_token=uuid_provider.generate(),
    )
    wav_filepath = 'test_wav.wav'

    media_path = audio_converter.config.get_media_path()
    wav_full_path = os.path.join(media_path, wav_filepath)

    repo = common.FakeAudioRepository([])
    uow = common.FakeAudioUOW(repo)
    with open(wav_full_path, 'rb') as wav_file:
        mp3_audio = audio_converter.services.converter.convert_wav_to_mp3_and_save(
            user=test_user,
            wav_file=wav_file,
            uow=uow
        )
    
    # Asserting that audio set is not empty
    assert uow.audio.audio_set
    
    mp3_full_path = audio_converter.services.converter.get_audio_path(mp3_audio)
    assert os.path.exists(mp3_full_path)
    os.remove(mp3_full_path)
