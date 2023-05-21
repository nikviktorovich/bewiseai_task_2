from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql

import audio_converter.database.orm
import audio_converter.modules.user.database.models


class Audio(audio_converter.database.orm.Base):
    __tablename__ = 'audio'

    uuid = Column(postgresql.UUID(as_uuid=True), primary_key=True)
    user_id = Column(ForeignKey('users.id'))
    user = relationship(audio_converter.modules.user.database.models.User)
    audio_filepath = Column(String)
