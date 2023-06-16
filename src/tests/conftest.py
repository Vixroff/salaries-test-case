import asyncio
import os
import sys
from datetime import date
from typing import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

sys.path = ['', '..'] + sys.path[1:]

from database import Base, get_async_session
from main import app
from app.models import User, Salary
from app.utils import get_hashed_password, create_access_token


def get_test_database_url():
    user = os.getenv("TEST_DB_USER", "postgres")
    password = os.getenv("TEST_DB_PASSWORD", "password")
    host = os.getenv("TEST_DB_HOST", "test-db")
    port = os.getenv("TEST_DB_PORT", 6000)
    db = os.getenv("TEST_DB_NAME", "database")
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"

test_engine = create_async_engine(get_test_database_url())
async_session_maker = async_sessionmaker(test_engine, expire_on_commit=False, autoflush=False)
async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest_asyncio.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        yield async_client


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(autouse=True)
async def init_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
async def test_user_data():
    return {
        "username": "user",
        "password": "password"
    }


@pytest_asyncio.fixture(scope="session")
async def test_user_credentials(test_user_data: dict):
    credentials = {
        "Authorization": f"Bearer {create_access_token(test_user_data['username'])}"
    }
    return credentials


@pytest_asyncio.fixture
async def create_test_user(test_user_data):
    async with async_session_maker() as async_session:
        test_user = User(
            username=test_user_data["username"],
            hashed_password=get_hashed_password(test_user_data["password"])
        )
        test_user_salary = Salary(
            salary=1000.00,
            increase_date=date.today()
        )
        test_user.salary = test_user_salary
        async_session.add(test_user)
        await async_session.commit()


@pytest_asyncio.fixture(scope="session")
async def other_user_data():
    return {
        "username": "user1",
        "password": "password1"
    }


@pytest_asyncio.fixture
async def create_other_user(other_user_data):
    async with async_session_maker() as async_session:
        other_user = User(
            username=other_user_data["username"],
            hashed_password=get_hashed_password(other_user_data["password"])
        )
        other_user_salary = Salary(
            salary=2000.00,
            increase_date=date.today()
        )
        other_user.salary = other_user_salary
        async_session.add(other_user)
        await async_session.commit()
