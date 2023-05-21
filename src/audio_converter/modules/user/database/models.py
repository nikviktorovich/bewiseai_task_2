import uuid

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

import audio_converter.database.orm


class User(audio_converter.database.orm.Base):
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    access_token = Column(
        String,
        unique=True,
        nullable=False,
        default=uuid.uuid4,
    )
