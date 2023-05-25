import uuid
from typing import Dict
from typing import List

import audio_converter.common.errors
import audio_converter.modules.audio.domain.models
import audio_converter.modules.audio.repositories
import audio_converter.services.unit_of_work


class FakeAudioRepository(audio_converter.modules.audio.repositories.AudioRepository):
    audio_set: Dict[uuid.UUID, audio_converter.modules.audio.domain.models.Audio]


    def __init__(
        self,
        data: List[audio_converter.modules.audio.domain.models.Audio],
    ) -> None:
        self.audio_set = {audio.uuid: audio for audio in data}


    def list(
        self,
        **filters,
    ) -> List[audio_converter.modules.audio.domain.models.Audio]:
        return list(self.audio_set.values())
    

    def get(
        self,
        audio_uuid: str,
    ) -> audio_converter.modules.audio.domain.models.Audio:
        if audio_uuid not in self.audio_set:
            raise audio_converter.common.errors.EntityNotFoundError(
                f'Unable to find an audio with id={audio_uuid}',
            )
        return self.audio_set[audio_uuid]


    def add(
        self,
        instance: audio_converter.modules.audio.domain.models.Audio,
    ) -> audio_converter.modules.audio.domain.models.Audio:
        self.audio_set[instance.uuid] = instance
        return instance


class FakeAudioUOW(audio_converter.services.unit_of_work.UnitOfWork):
    audio: FakeAudioRepository


    def __init__(self, repo: FakeAudioRepository) -> None:
        self.audio = repo


    def commit(self) -> None:
        pass
    

    def rollback(self) -> None:
        pass
    

    def __enter__(
        self,
    ) -> audio_converter.services.unit_of_work.UnitOfWork:
        return self
    

    def __exit__(self, *args, **kwargs) -> None:
        pass
