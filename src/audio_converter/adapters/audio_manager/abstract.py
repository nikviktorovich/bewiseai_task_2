import uuid
from typing import BinaryIO
from typing import Generator

import audio_converter.modules.audio.domain.models
import audio_converter.modules.user.domain.models


class AudioManager:
    def save(
        self,
        audio_uuid: uuid.UUID,
        user: audio_converter.modules.user.domain.models.User,
        audio_stream: BinaryIO,
    ) -> audio_converter.modules.audio.domain.models.Audio:
        raise NotImplementedError()


    def load(
        self,
        audio: audio_converter.modules.audio.domain.models.Audio,
    ) -> BinaryIO:
        raise NotImplementedError()
    

    def load_iterator(
        self,
        audio: audio_converter.modules.audio.domain.models.Audio,
    ) -> Generator[bytes, None, None]:
        raise NotImplementedError()
