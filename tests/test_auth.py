import pytest
from httpx import AsyncClient
from app.auth.jwt_handler import get_password_hash, verify_password

def test_hash_and_verify_password_over_bcrypt_byte_limit():
    password = "á" * 40
    hashed_password = get_password_hash(password)

    assert verify_password(password, hashed_password)

@pytest.mark.asyncio
async def test_register_user(client: AsyncClient, user_data):
    response = await client.post("/api/auth/register", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert "id" in data

@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient, user_data):
    await client.post("/api/auth/register", json=user_data)
    response = await client.post("/api/auth/register", json=user_data)
    assert response.status_code == 409
    assert "Email already registered" in response.json()["detail"]

@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, user_data):
    await client.post("/api/auth/register", json=user_data)
    response = await client.post("/api/auth/login", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient):
    response = await client.post("/api/auth/login", json={"email": "test@example.com", "password": "wrong"})
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]

@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient, user_data):
    await client.post("/api/auth/register", json=user_data)
    login_response = await client.post("/api/auth/login", json=user_data)
    token = login_response.json()["access_token"]
    response = await client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
