import os

import sqlalchemy
import sqlalchemy.engine


def get_postgres_connection_url() -> str:
    """Returns postgresql database connection url"""
    # Using environ[...] instead of environ.get(...) to raise exception
    # in case of missing some of the crucial variables
    db_name = os.environ['POSTGRES_DB']
    username = os.environ['POSTGRES_USER']
    password = os.environ['POSTGRES_PASSWORD']
    host = os.environ.get('POSTGRES_HOST', '127.0.0.1')
    port = os.environ.get('POSTGRES_PORT', '5432')
    connection_url = f'postgresql://{username}:{password}@{host}:{port}/{db_name}'
    return connection_url


def get_database_engine() -> sqlalchemy.engine.Engine:
    connection_url = get_postgres_connection_url()
    engine = sqlalchemy.create_engine(url=connection_url)
    return engine


def get_media_path() -> str:
    """Returns path to media directory"""
    media_path = os.environ['MEDIA_PATH']
    return media_path
