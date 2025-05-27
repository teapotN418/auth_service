import pytest
from httpx import ASGITransport, AsyncClient

from src.app.main import app
from .conftest import baseurl

@pytest.mark.anyio
async def test_root():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url=baseurl
    ) as ac:
        response = await ac.get("/")
    assert response.status_code == 200

@pytest.mark.anyio
async def test_create_user():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url=baseurl
    ) as ac:
        response = await ac.post(
            "/users/register",
            json={"email": "test_reg@mail.com", "password": "12345"},
        )
    assert response.status_code == 200
    assert response.json() == {
        "email": "test_reg@mail.com",
        "role": "user",
        "id": 1,
    }

# def test_create_existing():
#     response = client.post(
#         "/users/register",
#         json={"email": "test_reg@mail.com", "password": "12345"},
#     )
#     assert response.status_code == 409

# def user_auth():
#     response = client.post(
#         "/users/auth/login",
#         json={"email": "test_reg@mail.com", "password": "12345"},
#     )
#     assert response.status_code == 200

# @pytest.fixture
# def user_auth_cookies():
#     response = client.post(
#         "/users/auth/login",
#         json={"email": "test_reg@mail.com", "password": "12345"},
#     )
#     return response.cookies

# def test_read_user_me(user_auth_cookies):
#     response = client.get("/users/me", cookies=user_auth_cookies)
#     assert response.status_code == 200

# from .conftest import client
# import pytest
# import pytest_asyncio

# def test_read_main():
#     response = client.get("/")
#     assert response.status_code == 200

# @pytest.mark.asyncio
# async def test_create_user():
#     response = await client.post(
#         "/users/register",
#         json={"email": "test_reg@mail.com", "password": "12345"},
#     )
#     assert response.status_code == 200
#     assert response.json() == {
#         "email": "test_reg@mail.com",
#         "role": "user",
#         "id": 1,
#     }

# @pytest.mark.asyncio
# async def test_create_existing():
#     response = await client.post(
#         "/users/register",
#         json={"email": "test_reg@mail.com", "password": "password"},
#     )
#     assert response.status_code == 409

# @pytest_asyncio.fixture
# async def user_auth_cookies():
#     response = await client.post(
#         "/users/auth/login",
#         json={"email": "test_reg@mail.com", "password": "password"},
#     )
#     assert response.status_code == 200
#     return response.cookies

# @pytest.mark.asyncio
# async def test_read_user_me(user_auth_cookies):
#     response = await client.get("/users/me", cookies=user_auth_cookies)
#     assert response.status_code == 200

# @pytest.mark.asyncio
# async def test_read_user_me(user_auth_cookies):
#     response = await client.put(
#         "/users/auth/login",
#         json={"password": "test_reg@mail.com", "password": "abcde"},
#         cookies=user_auth_cookies,
#     )
#     assert response.status_code == 200

