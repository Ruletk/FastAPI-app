from typing import Generator, Any
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text as sa_text
from starlette.testclient import TestClient
from main import app
import os
from db.models import Base
import settings
import asyncio
from db.session import get_db
import asyncpg


CLEAN_TABLES = [
    "users",
]


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def run_migrations():
    os.system("alembic init tests/alembic")
    os.system(
        'alembic -c tests/alembic.ini revision --autogenerate -m "test running migrations"'
    )
    os.system("alembic -c tests/alembic.ini upgrade head")


@pytest.fixture(scope="session")
async def async_session_test():
    engine = create_async_engine(settings.TEST_DATABASE_URL, future=True, echo=True)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    yield async_session


@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_session_test):
    """Clean data in all tables before running test function"""
    async with async_session_test() as session:
        async with session.begin():
            for table_for_cleaning in CLEAN_TABLES:
                await session.execute(
                    sa_text(f"""TRUNCATE TABLE {table_for_cleaning};""")
                )


async def _get_test_db():
    test_engine = create_async_engine(
        settings.TEST_DATABASE_URL, future=True, echo=True
    )

    test_async_session = sessionmaker(
        test_engine, expire_on_commit=False, class_=AsyncSession
    )

    yield test_async_session()


@pytest.fixture(scope="function")
async def client() -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
async def asyncpg_pool():
    url = settings.TEST_DATABASE_URL.replace("+asyncpg", "")
    async with await asyncpg.create_pool(url) as pool:
        yield pool


@pytest.fixture
async def get_user_from_database(asyncpg_pool):
    async def get_user_from_database_by_uuid(user_id: str):
        async with asyncpg_pool.acquire() as conn:
            return await conn.fetch(
                """SELECT * FROM users WHERE user_id = $1;""", user_id
            )

    return get_user_from_database_by_uuid


@pytest.fixture
async def create_user_in_database(asyncpg_pool):
    async def create_user_in_database(
        user_id: str, nickname: str, email: str, is_active: bool
    ):
        async with asyncpg_pool.acquire() as conn:
            return await conn.execute(
                """INSERT INTO users VALUES ($1, $2, $3, $4)""",
                user_id,
                nickname,
                email,
                is_active,
            )

    return create_user_in_database
