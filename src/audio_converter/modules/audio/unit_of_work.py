from typing import Optional

import sqlalchemy
import sqlalchemy.orm

import audio_converter.config
from audio_converter.modules.audio import repositories


class AbstractAudioUnitOfWork:
    audio: repositories.AbstractAudioRepository


    def commit(self) -> None:
        raise NotImplementedError()
    

    def rollback(self) -> None:
        raise NotImplementedError()
    

    def __enter__(self) -> 'AbstractAudioUnitOfWork':
        raise NotImplementedError()
    

    def __exit__(self, *args, **kwargs) -> None:
        raise NotImplementedError()


class SQLAlchemyAudioUnitOfWork(AbstractAudioUnitOfWork):
    session_factory: sqlalchemy.orm.sessionmaker
    session: sqlalchemy.orm.Session


    def __init__(
        self,
        engine: Optional[sqlalchemy.engine.Engine] = None,
    ) -> None:
        if engine is None:
            engine = audio_converter.config.get_database_engine()
        
        self.session_factory = sqlalchemy.orm.sessionmaker(bind=engine)
    

    def commit(self) -> None:
        self.session.commit()
    

    def rollback(self) -> None:
        self.session.rollback()
    

    def __enter__(self) -> 'AbstractAudioUnitOfWork':
        self.session = self.session_factory()
        self.audio = repositories.SQLAlchemyAudioRepository(self.session)
        return self
    

    def __exit__(self, *args, **kwargs) -> None:
        self.session.close()
