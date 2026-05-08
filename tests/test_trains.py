import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_train(client: AsyncClient, user_data):
    token = await get_token(client, user_data)
    train_data = {"weight": 100, "train_cars": 5}
    response = await client.post("/trains", json=train_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    data = response.json()
    assert data["weight"] == 100
    assert data["train_cars"] == 5
    assert "id" in data

@pytest.mark.asyncio
async def test_create_train_invalid_data(client: AsyncClient, user_data):
    token = await get_token(client, user_data)
    train_data = {"weight": -1, "train_cars": 0}
    response = await client.post("/trains", json=train_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_list_trains(client: AsyncClient, user_data):
    token = await get_token(client, user_data)
    train_data = {"weight": 100, "train_cars": 5}
    await client.post("/trains", json=train_data, headers={"Authorization": f"Bearer {token}"})
    response = await client.get("/trains", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

@pytest.mark.asyncio
async def test_update_train(client: AsyncClient, user_data):
    token = await get_token(client, user_data)
    create_response = await client.post("/trains", json={"weight": 100, "train_cars": 5}, headers={"Authorization": f"Bearer {token}"})
    train_id = create_response.json()["id"]
    response = await client.put(f"/trains/{train_id}", json={"weight": 200, "train_cars": 10}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["weight"] == 200
    assert response.json()["train_cars"] == 10

@pytest.mark.asyncio
async def test_delete_train(client: AsyncClient, user_data):
    token = await get_token(client, user_data)
    create_response = await client.post("/trains", json={"weight": 100, "train_cars": 5}, headers={"Authorization": f"Bearer {token}"})
    train_id = create_response.json()["id"]
    response = await client.delete(f"/trains/{train_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 204

async def get_token(client: AsyncClient, user_data):
    await client.post("/auth/register", json=user_data)
    login_response = await client.post("/auth/login", json=user_data)
    return login_response.json()["access_token"]