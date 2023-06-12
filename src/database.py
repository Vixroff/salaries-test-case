import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.ext.declarative import declarative_base


def get_database_url():
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "password")
    host = os.getenv("POSTGRES_HOST", "db")
    port = os.getenv("POSTGRES_PORT", 5432)
    db = os.getenv("POSTGRES_DB", "database")
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"

engine = create_async_engine(get_database_url())

async_session_maker = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


Base = declarative_base()
