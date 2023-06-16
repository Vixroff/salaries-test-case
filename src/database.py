import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import declarative_base


def get_database_url():
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "password")
    host = os.getenv("DB_HOST", "db")
    port = os.getenv("DB_PORT", 5432)
    db = os.getenv("DB_NAME", "database")
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"

engine = create_async_engine(get_database_url())
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


Base = declarative_base()
