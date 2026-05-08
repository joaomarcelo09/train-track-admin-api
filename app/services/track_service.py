from typing import Optional, Dict, Any, List
from ..repositories.track_repository import TrackRepository
from ..schemas.track import TrackCreate, TrackResponse
from fastapi import HTTPException, status

class TrackService:
    def __init__(self):
        self.repository = TrackRepository()
        from .line_service import LineService
        self.line_service = LineService()

    async def create_track(self, track_data: TrackCreate) -> TrackResponse:
        line = await self.line_service.get_line(track_data.id_line)
        if not line:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Line with id '{track_data.id_line}' does not exist"
            )
        data = track_data.dict()
        track = await self.repository.create(data)
        return TrackResponse(**track)

    async def get_track(self, track_id: str) -> Optional[TrackResponse]:
        track = await self.repository.get_by_id(track_id)
        if track:
            return TrackResponse(**track)
        return None

    async def get_all_tracks(self, filters: Dict[str, Any] = None) -> List[TrackResponse]:
        tracks = await self.repository.get_all(filters)
        return [TrackResponse(**track) for track in tracks]

    async def update_track(self, track_id: str, track_data: TrackCreate) -> Optional[TrackResponse]:
        line = await self.line_service.get_line(track_data.id_line)
        if not line:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Line with id '{track_data.id_line}' does not exist"
            )
        track = await self.repository.update(track_id, track_data.dict())
        if track:
            return TrackResponse(**track)
        return None

    async def delete_track(self, track_id: str) -> bool:
        return await self.repository.delete(track_id)

    async def get_tracks_by_line(self, line_id: str) -> List[TrackResponse]:
        tracks = await self.repository.get_by_line(line_id)
        return [TrackResponse(**track) for track in tracks]

    async def get_summary_by_line(self, line_id: str) -> Optional[Dict[str, Any]]:
        summary = await self.repository.get_summary_by_line(line_id)
        return summary