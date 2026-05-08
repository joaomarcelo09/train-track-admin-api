import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_track(client: AsyncClient, user_data):
    token = await get_token(client, user_data)
    line_response = await client.post("/lines", json={"name": "Test Line"}, headers={"Authorization": f"Bearer {token}"})
    line_id = line_response.json()["id"]

    track_data = {
        "id_line": line_id,
        "length": 5000,
        "bending": 5,
        "elevation": 100
    }
    response = await client.post("/tracks", json=track_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    data = response.json()
    assert data["length"] == 5000
    assert "id" in data

@pytest.mark.asyncio
async def test_create_track_invalid_line(client: AsyncClient, user_data):
    token = await get_token(client, user_data)
    track_data = {
        "id_line": "invalid-line-id",
        "length": 5000,
        "bending": 5,
        "elevation": 100
    }
    response = await client.post("/tracks", json=track_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400
    assert "does not exist" in response.json()["detail"]

@pytest.mark.asyncio
async def test_track_filters(client: AsyncClient, user_data):
    token = await get_token(client, user_data)
    line_response = await client.post("/lines", json={"name": "Test Line"}, headers={"Authorization": f"Bearer {token}"})
    line_id = line_response.json()["id"]

    tracks = [
        {"id_line": line_id, "length": 1000, "bending": 2, "elevation": 50},
        {"id_line": line_id, "length": 2000, "bending": 3, "elevation": 100},
        {"id_line": line_id, "length": 3000, "bending": 4, "elevation": 150},
    ]
    for track in tracks:
        await client.post("/tracks", json=track, headers={"Authorization": f"Bearer {token}"})

    response = await client.get(f"/tracks?line={line_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

    response = await client.get(f"/tracks?length=2000", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["length"] == 2000

@pytest.mark.asyncio
async def test_get_line_summary(client: AsyncClient, user_data):
    token = await get_token(client, user_data)
    line_response = await client.post("/lines", json={"name": "Test Line"}, headers={"Authorization": f"Bearer {token}"})
    line_id = line_response.json()["id"]

    tracks = [
        {"id_line": line_id, "length": 1000, "bending": 2, "elevation": 50},
        {"id_line": line_id, "length": 2000, "bending": 4, "elevation": 100},
    ]
    for track in tracks:
        await client.post("/tracks", json=track, headers={"Authorization": f"Bearer {token}"})

    response = await client.get(f"/lines/{line_id}/summary", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["total_length"] == 3000
    assert data["tracks"] == 2
    assert data["max_elevation"] == 100

async def get_token(client: AsyncClient, user_data):
    await client.post("/auth/register", json=user_data)
    login_response = await client.post("/auth/login", json=user_data)
    return login_response.json()["access_token"]