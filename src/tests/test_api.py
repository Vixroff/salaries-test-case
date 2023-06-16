from http import HTTPStatus
import os

import pytest
from httpx import AsyncClient
from jose import jwt

from app.models import User


@pytest.mark.asyncio
async def test_create_user(
    async_client: AsyncClient,
    test_user_data: dict
):
    response = await async_client.post(
        "/users",
        json=test_user_data,
    )
    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.asyncio
async def test_create_user_unique_false(
    async_client: AsyncClient,
    create_test_user,
    test_user_data,
):
    response = await async_client.post(
        "/users",
        json=test_user_data
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_auth(
    async_client: AsyncClient,
    create_test_user,
    test_user_data,
):
    response = await async_client.post(
        "/auth/jwt",
        data=test_user_data
    )
    assert response.status_code == HTTPStatus.OK

    token = response.json().get("access_token")
    assert token

    payload = jwt.decode(
        token,
        str(os.getenv('JWT_SECRET_KEY')),
        algorithms=[os.getenv('JWT_ALGORITHM')]
    )
    assert test_user_data["username"] == payload.get("sub")


@pytest.mark.asyncio
async def test_auth_bad_credential(
    async_client: AsyncClient,
    test_user_data,
):
    response = await async_client.post(
        "/auth/jwt",
        data=test_user_data,
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_salary_owner(
    async_client: AsyncClient,
    create_test_user,
    test_user_credentials,
    test_user_data,
):
    response = await async_client.get(
        f"users/{test_user_data['username']}/salary",
        headers=test_user_credentials,
    )
    response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_salary_unexists(
    async_client: AsyncClient,
    test_user_credentials,
    test_user_data,
):
    response = await async_client.get(
        f"users/{test_user_data['username']}/salary",
        headers=test_user_credentials,
    )
    response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_salary_other(
    async_client: AsyncClient,
    create_test_user,
    test_user_credentials,
    test_user_data,
    other_user_data,
    create_other_user,
):
    response = await async_client.get(
        "users/{}/salary".format(other_user_data["username"]),
        headers=test_user_credentials,
    )
    response.status_code == HTTPStatus.FORBIDDEN
