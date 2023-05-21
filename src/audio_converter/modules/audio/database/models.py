import uuid

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

import audio_converter.database.orm
import audio_converter.modules.user.database.models


class AudioMeta(audio_converter.database.orm.Base):
    uuid = Column(String, primary_key=True)
    user_id = Column(Integer)
    user = relationship(audio_converter.modules.user.database.models.User)


class AudioBlob(audio_converter.database.orm.Base):
    uuid = Column(String, primary_key=True)
    audio_filepath = Column(String)
