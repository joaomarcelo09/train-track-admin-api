from motor.motor_asyncio import AsyncIOMotorClient
from ..core.config import settings

client: AsyncIOMotorClient = None
database = None

async def connect_to_mongo():
    global client, database
    client = AsyncIOMotorClient(settings.mongodb_url)
    database = client[settings.database_name]

async def close_mongo_connection():
    global client
    if client:
        client.close()

def get_database():
    return database