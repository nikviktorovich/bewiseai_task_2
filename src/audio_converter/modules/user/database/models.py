import uuid

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.dialects import postgresql

import audio_converter.database.orm
import audio_converter.services.uuid_generator


class User(audio_converter.database.orm.Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    access_token = Column(
        postgresql.UUID(as_uuid=True),
        unique=True,
        nullable=False,
        default=audio_converter.services.uuid_generator.generate_uuid,
    )
