import pytest
from httpx import AsyncClient
import asyncio

from src.app.core.config import settings
from src.app.core.security import security_config
#from src.app.main import app
#from src.app.api.deps import get_db
#from src.app.db.setup import async_engine, async_session_factory

backend_url = "http://localhost:" + settings.BACKEND_PORT

db_url = settings.DATABASE_URL

# @pytest.fixture(scope="function")
# async def db_session():
#     connection = await async_engine.connect()
#     transaction = await connection.begin()
#     session = async_session_factory(autocommit=False, autoflush=False, bind=connection)
    
#     yield session
    
#     await session.close()
#     await transaction.rollback()
#     await connection.close()

# @pytest.fixture(scope="function")
# async def client(db_session):
#     app.dependency_overrides[get_db] = lambda: db_session
    
#     async with AsyncClient(app=app, base_url=backend_url) as client:
#         yield client

# @pytest.fixture(scope="session")
# def event_loop(request):
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()

from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncTransaction, AsyncConnection, AsyncSession, create_async_engine

# Importing fastapi.Depends that is used to retrieve SQLAlchemy's session
from src.app.api.deps import get_db
# Importing main FastAPI instance
from src.app.main import app

# To run async tests
pytestmark = pytest.mark.anyio

# Supply connection string
engine = create_async_engine(db_url)


# Required per https://anyio.readthedocs.io/en/stable/testing.html#using-async-fixtures-with-higher-scopes
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def connection(anyio_backend) -> AsyncGenerator[AsyncConnection, None]:
    async with engine.connect() as connection:
        yield connection

        
@pytest.fixture()
async def transaction(
    connection: AsyncConnection,
) -> AsyncGenerator[AsyncTransaction, None]:
    async with connection.begin() as transaction:
        yield transaction


# Use this fixture to get SQLAlchemy's AsyncSession.
# All changes that occur in a test function are rolled back
# after function exits, even if session.commit() is called
# in inner functions
@pytest.fixture()
async def session(
    connection: AsyncConnection, transaction: AsyncTransaction
) -> AsyncGenerator[AsyncSession, None]:
    
    async_session = AsyncSession(
        bind=connection,
        join_transaction_mode="create_savepoint",
    )

    yield async_session

    await transaction.rollback()

# Use this fixture to get HTTPX's client to test API.
# All changes that occur in a test function are rolled back
# after function exits, even if session.commit() is called
# in FastAPI's application endpoints
@pytest.fixture()
async def client(
    connection: AsyncConnection, transaction: AsyncTransaction
) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
        async_session = AsyncSession(
            bind=connection,
            join_transaction_mode="create_savepoint",
        )
        async with async_session:
            yield async_session
    
    # Here you have to override the dependency that is used in FastAPI's
    # endpoints to get SQLAlchemy's AsyncSession. In my case, it is
    # get_async_session
    app.dependency_overrides[get_db] = override_get_async_session
    yield AsyncClient(app=app, base_url=backend_url)
    del app.dependency_overrides[get_db]

    await transaction.rollback()

@pytest.fixture(scope='session')
def event_loop():
    """
    Creates an instance of the default event loop for the test session.
    """
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

# Tests showing rollbacks between functions when using API client
# async def test_api_create_profile(client: AsyncClient):
#     test_name = "test"
#     async with client as ac:
#         response = await ac.post(
#             "/api/profiles",
#             json={"name": test_name},
#         )
#         created_profile_id = response.json()["id"]

#         response = await ac.get(
#             "/api/profiles",
#         )
#         assert response.status_code == 200
#         assert len(response.json()) == 1
        
#         response = await ac.get(
#             f"/api/profiles/{created_profile_id}",
#         )
#         assert response.status_code == 200
#         assert response.json()["id"] == created_profile_id
#         assert response.json()["name"] == test_name


# async def test_client_rollbacks(client: AsyncClient):
#     async with client as ac:
#         response = await ac.get(
#             "/api/profiles",
#         )
#         assert len(response.json()) == 0