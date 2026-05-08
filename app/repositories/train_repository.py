from typing import Optional, Dict, Any, List
import uuid
from .base_repository import BaseRepository
from ..database.connection import get_database

class TrainRepository(BaseRepository):
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.trains

    async def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        train = await self.collection.find_one({"id": id})
        return train

    async def get_all(self) -> list:
        cursor = self.collection.find()
        trains = await cursor.to_list(length=None)
        return trains

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        train_id = str(uuid.uuid4())
        train = {"id": train_id, **data}
        await self.collection.insert_one(train)
        return train

    async def update(self, id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        result = await self.collection.update_one({"id": id}, {"$set": data})
        if result.modified_count:
            train = await self.collection.find_one({"id": id})
            return train
        return None

    async def delete(self, id: str) -> bool:
        result = await self.collection.delete_one({"id": id})
        return result.deleted_count > 0