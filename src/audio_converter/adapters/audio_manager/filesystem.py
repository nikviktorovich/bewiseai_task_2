import os.path
import uuid
from typing import BinaryIO
from typing import Generator
from typing import Optional

import audio_converter.modules.audio.domain.models
import audio_converter.modules.user.domain.models
from audio_converter.adapters.audio_manager import abstract


class FilesystemAudioManager(abstract.AudioManager):
    media_path: str
    file_extension: Optional[str]


    def __init__(
        self,
        media_path: str,
        file_extension: Optional[str] = None,
    ) -> None:
        self.media_path = media_path
        self.file_extension = file_extension


    def save(
        self,
        audio_uuid: uuid.UUID,
        user: audio_converter.modules.user.domain.models.User,
        audio_stream: BinaryIO,
    ) -> audio_converter.modules.audio.domain.models.Audio:
        file_extension = f'.{self.file_extension}' or ''
        relative_audio_path = f'{audio_uuid}{file_extension}'
        absolute_audio_path = os.path.join(self.media_path, relative_audio_path)

        with open(absolute_audio_path, 'wb') as file:
            file.write(audio_stream.read())

        return audio_converter.modules.audio.domain.models.Audio(
            uuid=audio_uuid,
            user_id=user.id,
            user=user,
            audio_filepath=relative_audio_path
        )


    def load(
        self,
        audio: audio_converter.modules.audio.domain.models.Audio,
    ) -> BinaryIO:
        relative_audio_path = audio.audio_filepath
        absolute_audio_path = os.path.join(self.media_path, relative_audio_path)
        return open(absolute_audio_path, 'rb')
    

    def load_iterator(
        self,
        audio: audio_converter.modules.audio.domain.models.Audio,
    ) -> Generator[bytes, None, None]:
        with self.load(audio) as f:
            yield from f
