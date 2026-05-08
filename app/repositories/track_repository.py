from typing import Optional, Dict, Any, List
import uuid
from .base_repository import BaseRepository
from ..database.connection import get_database

class TrackRepository(BaseRepository):
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.tracks

    async def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        track = await self.collection.find_one({"id": id})
        return track

    async def get_all(self, filters: Dict[str, Any] = None) -> list:
        query = filters or {}
        cursor = self.collection.find(query)
        tracks = await cursor.to_list(length=None)
        return tracks

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        track_id = str(uuid.uuid4())
        track = {"id": track_id, **data}
        await self.collection.insert_one(track)
        return track

    async def update(self, id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        result = await self.collection.update_one({"id": id}, {"$set": data})
        if result.modified_count:
            track = await self.collection.find_one({"id": id})
            return track
        return None

    async def delete(self, id: str) -> bool:
        result = await self.collection.delete_one({"id": id})
        return result.deleted_count > 0

    async def get_by_line(self, line_id: str) -> list:
        cursor = self.collection.find({"id_line": line_id})
        tracks = await cursor.to_list(length=None)
        return tracks

    async def get_summary_by_line(self, line_id: str) -> Optional[Dict[str, Any]]:
        pipeline = [
            {"$match": {"id_line": line_id}},
            {
                "$group": {
                    "_id": "$id_line",
                    "total_length": {"$sum": "$length"},
                    "average_elevation": {"$avg": "$elevation"},
                    "max_elevation": {"$max": "$elevation"},
                    "average_bending": {"$avg": "$bending"},
                    "track_count": {"$sum": 1}
                }
            }
        ]
        result = await self.collection.aggregate(pipeline).to_list(length=1)
        return result[0] if result else None