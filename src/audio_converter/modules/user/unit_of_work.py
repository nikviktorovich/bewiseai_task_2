from typing import Optional

import sqlalchemy
import sqlalchemy.orm

import audio_converter.config
from audio_converter.modules.user import repositories


class AbstractUserUnitOfWork:
    users: repositories.AbstractUserRepository


    def commit(self) -> None:
        raise NotImplementedError()
    

    def rollback(self) -> None:
        raise NotImplementedError()
    

    def __enter__(self) -> 'AbstractUserUnitOfWork':
        raise NotImplementedError()
    

    def __exit__(self, *args, **kwargs) -> None:
        raise NotImplementedError()


class SQLAlchemyUserUnitOfWork(AbstractUserUnitOfWork):
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
    

    def __enter__(self) -> 'AbstractUserUnitOfWork':
        self.session = self.session_factory()
        self.users = repositories.SQLAlchemyUserRepository(self.session)
        return self
    

    def __exit__(self, *args, **kwargs) -> None:
        self.session.close()
