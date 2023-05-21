import dataclasses
from typing import Any

import audio_converter.modules.user.domain.models


@dataclasses.dataclass
class AudioMeta:
    uuid: Any
    user_id: int
    user: audio_converter.modules.user.domain.models.User


@dataclasses.dataclass
class AudioBlob:
    uuid: str
    audio_filepath: str
