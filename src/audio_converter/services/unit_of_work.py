from typing import Optional

import sqlalchemy
import sqlalchemy.orm

import audio_converter.config
import audio_converter.modules.audio
import audio_converter.modules.user


class AbstractUnitOfWork:
    audio: audio_converter.modules.audio.AbstractAudioRepository
    users: audio_converter.modules.user.AbstractUserRepository


    def commit(self) -> None:
        raise NotImplementedError()
    

    def rollback(self) -> None:
        raise NotImplementedError()
    

    def __enter__(self) -> 'AbstractUnitOfWork':
        raise NotImplementedError()
    

    def __exit__(self, *args, **kwargs) -> None:
        raise NotImplementedError()


class UnitOfWork(AbstractUnitOfWork):
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
    

    def __enter__(self) -> 'AbstractUnitOfWork':
        self.session = self.session_factory()
        self.audio = audio_converter.modules.audio.SQLAlchemyAudioRepository(
            self.session,
        )
        self.users = audio_converter.modules.user.SQLAlchemyUserRepository(
            self.session,
        )
        return self
    

    def __exit__(self, *args, **kwargs) -> None:
        self.session.close()