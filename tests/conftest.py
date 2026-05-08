import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from motor.motor_asyncio import AsyncIOMotorClient
from app.main import app
from app.database.connection import connect_to_mongo, close_mongo_connection
from app.core.config import settings
import asyncio

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session")
async def db_client():
    client = AsyncIOMotorClient(settings.mongodb_url)
    yield client
    client.close()

@pytest_asyncio.fixture(scope="function")
async def test_db(db_client):
    db = db_client[settings.database_name]
    await db.drop_collection("users")
    await db.drop_collection("trains")
    await db.drop_collection("lines")
    await db.drop_collection("tracks")
    yield db

@pytest_asyncio.fixture(scope="function")
async def client(test_db):
    await connect_to_mongo()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    await close_mongo_connection()

@pytest.fixture
def user_data():
    return {
        "email": "test@example.com",
        "password": "password123"
    }
