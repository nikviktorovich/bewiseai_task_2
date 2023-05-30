import os
import os.path

import pytest

import audio_converter.adapters.audio_manager
import audio_converter.adapters.converter
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
    converter = audio_converter.adapters.converter.PydubAudioConverter()
    audio_manager = audio_converter.adapters.audio_manager.FilesystemAudioManager(
        media_path=media_path,
        file_extension='mp3',
    )

    with open(wav_full_path, 'rb') as wav_file:
        mp3_audio = audio_converter.services.converter.convert_wav_to_mp3_and_save(
            uuid_provider=uuid_provider,
            converter=converter,
            audio_manager=audio_manager,
            wav_file=wav_file,
            user=test_user,
            uow=uow
        )
    
    # Asserting that audio set is not empty
    assert uow.audio.audio_set

    mp3_full_path = os.path.join(media_path, f'{mp3_audio.uuid.hex}.mp3')
    assert os.path.exists(mp3_full_path)
    os.remove(mp3_full_path)
