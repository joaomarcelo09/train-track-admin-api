import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_line(client: AsyncClient, user_data):
    token = await get_token(client, user_data)
    line_data = {"name": "Line 1"}
    response = await client.post("/lines", json=line_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Line 1"
    assert "id" in data

@pytest.mark.asyncio
async def test_create_line_duplicate_name(client: AsyncClient, user_data):
    token = await get_token(client, user_data)
    line_data = {"name": "Line 1"}
    await client.post("/lines", json=line_data, headers={"Authorization": f"Bearer {token}"})
    response = await client.post("/lines", json=line_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]

@pytest.mark.asyncio
async def test_list_lines(client: AsyncClient, user_data):
    token = await get_token(client, user_data)
    line_data = {"name": "Line 1"}
    await client.post("/lines", json=line_data, headers={"Authorization": f"Bearer {token}"})
    response = await client.get("/lines", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

@pytest.mark.asyncio
async def test_update_line(client: AsyncClient, user_data):
    token = await get_token(client, user_data)
    create_response = await client.post("/lines", json={"name": "Line 1"}, headers={"Authorization": f"Bearer {token}"})
    line_id = create_response.json()["id"]
    response = await client.put(f"/lines/{line_id}", json={"name": "Line 2"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["name"] == "Line 2"

@pytest.mark.asyncio
async def test_delete_line(client: AsyncClient, user_data):
    token = await get_token(client, user_data)
    create_response = await client.post("/lines", json={"name": "Line 1"}, headers={"Authorization": f"Bearer {token}"})
    line_id = create_response.json()["id"]
    response = await client.delete(f"/lines/{line_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 204

async def get_token(client: AsyncClient, user_data):
    await client.post("/auth/register", json=user_data)
    login_response = await client.post("/auth/login", json=user_data)
    return login_response.json()["access_token"]