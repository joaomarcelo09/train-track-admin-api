from typing import Optional, Dict, Any, List
import uuid
from .base_repository import BaseRepository
from ..database.connection import get_database

class LineRepository(BaseRepository):
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.lines

    async def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        line = await self.collection.find_one({"id": id})
        return line

    async def get_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        line = await self.collection.find_one({"name": name})
        return line

    async def get_all(self) -> list:
        cursor = self.collection.find()
        lines = await cursor.to_list(length=None)
        return lines

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        line_id = str(uuid.uuid4())
        line = {"id": line_id, **data}
        await self.collection.insert_one(line)
        return line

    async def update(self, id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        result = await self.collection.update_one({"id": id}, {"$set": data})
        if result.modified_count:
            line = await self.collection.find_one({"id": id})
            return line
        return None

    async def delete(self, id: str) -> bool:
        result = await self.collection.delete_one({"id": id})
        return result.deleted_count > 0

    async def name_exists(self, name: str, exclude_id: str = None) -> bool:
        query = {"name": name}
        if exclude_id:
            query["id"] = {"$ne": exclude_id}
        count = await self.collection.count_documents(query)
        return count > 0