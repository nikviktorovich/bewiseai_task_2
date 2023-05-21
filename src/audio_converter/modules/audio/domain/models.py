import dataclasses
import uuid

import audio_converter.modules.user.domain.models


@dataclasses.dataclass
class Audio:
    uuid: uuid.UUID
    user_id: int
    user: audio_converter.modules.user.domain.models.User
    audio_filepath: str
