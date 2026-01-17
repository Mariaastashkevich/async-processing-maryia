from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db.config import get_settings
from functools import lru_cache


@lru_cache()
def get_sync_engine():
    settings = get_settings()
    return create_engine(
        url=settings.DATABASE_URL_psycopg,
        echo=True,
        pool_size=5,
        max_overflow=10,
    )


@lru_cache()
def get_async_engine():
    settings = get_settings()
    return create_async_engine(
        url=settings.DATABASE_URL_asyncpg,
        echo=True,
        pool_size=5,
        max_overflow=10,
    )


def get_session_factory():
    return sessionmaker(get_sync_engine())


def get_async_session_factory():
    return async_sessionmaker(get_async_engine())


