from typing import Optional, Dict, Any
from datetime import datetime
import uuid
from .base_repository import BaseRepository
from ..database.connection import get_database
from ..auth.jwt_handler import get_password_hash

class UserRepository(BaseRepository):
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.users

    async def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        user = await self.collection.find_one({"id": id})
        return user

    async def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        user = await self.collection.find_one({"email": email})
        return user

    async def get_all(self) -> list:
        cursor = self.collection.find()
        users = await cursor.to_list(length=None)
        return users

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        user_id = str(uuid.uuid4())
        hashed_password = get_password_hash(data["password"])
        user = {
            "id": user_id,
            "email": data["email"],
            "hashed_password": hashed_password,
            "created_at": datetime.utcnow()
        }
        await self.collection.insert_one(user)
        return user

    async def update(self, id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        result = await self.collection.update_one({"id": id}, {"$set": data})
        if result.modified_count:
            user = await self.collection.find_one({"id": id})
            return user
        return None

    async def delete(self, id: str) -> bool:
        result = await self.collection.delete_one({"id": id})
        return result.deleted_count > 0
