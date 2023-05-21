import dataclasses
from typing import Any

import audio_converter.modules.user.domain.models


@dataclasses.dataclass
class Audio:
    uuid: Any
    user_id: int
    user: audio_converter.modules.user.domain.models.User
    audio_filepath: str
