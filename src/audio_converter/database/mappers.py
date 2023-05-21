import sqlalchemy.orm
from sqlalchemy.orm import relationship

import audio_converter.modules.audio.database.models
import audio_converter.modules.audio.domain.models
import audio_converter.modules.user.database.models
import audio_converter.modules.user.domain.models


def start_mappers() -> None:
    registry = sqlalchemy.orm.registry()

    registry.map_imperatively(
        audio_converter.modules.audio.domain.models.Audio,
        audio_converter.modules.audio.database.models.Audio,
        properties={
            'user': relationship(audio_converter.modules.user.domain.models.User),
        }
    )

    registry.map_imperatively(
        audio_converter.modules.user.domain.models.User,
        audio_converter.modules.user.database.models.User,
    )
