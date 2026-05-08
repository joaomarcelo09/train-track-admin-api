from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional, Dict
from ..services.track_service import TrackService
from ..schemas.track import TrackCreate, TrackResponse
from ..auth.jwt_handler import get_current_user

router = APIRouter(prefix="/tracks", tags=["Tracks"])

@router.post("", response_model=TrackResponse, status_code=status.HTTP_201_CREATED)
async def create_track(track_data: TrackCreate, current_user = Depends(get_current_user)):
    service = TrackService()
    return await service.create_track(track_data)

@router.get("", response_model=List[TrackResponse])
async def list_tracks(
    line: Optional[str] = None,
    elevation: Optional[int] = None,
    bending: Optional[int] = None,
    current_user = Depends(get_current_user)
):
    filters = {}
    if line:
        filters["id_line"] = line
    if elevation is not None:
        filters["elevation"] = elevation
    if bending is not None:
        filters["bending"] = bending

    service = TrackService()
    return await service.get_all_tracks(filters)

@router.get("/{track_id}", response_model=TrackResponse)
async def get_track(track_id: str, current_user = Depends(get_current_user)):
    service = TrackService()
    track = await service.get_track(track_id)
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")
    return track

@router.put("/{track_id}", response_model=TrackResponse)
async def update_track(track_id: str, track_data: TrackCreate, current_user = Depends(get_current_user)):
    service = TrackService()
    track = await service.update_track(track_id, track_data)
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")
    return track

@router.delete("/{track_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_track(track_id: str, current_user = Depends(get_current_user)):
    service = TrackService()
    deleted = await service.delete_track(track_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")

@router.get("/lines/{line_id}/summary", response_model=Dict)
async def get_line_summary(line_id: str, current_user = Depends(get_current_user)):
    service = TrackService()
    summary = await service.get_summary_by_line(line_id)
    if not summary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No tracks found for this line")

    return {
        "line_id": line_id,
        "total_length": summary["total_length"],
        "average_elevation": round(summary["average_elevation"], 2) if summary["average_elevation"] else 0,
        "max_elevation": summary["max_elevation"],
        "average_bending": round(summary["average_bending"], 2) if summary["average_bending"] else 0,
        "tracks": summary["track_count"]
    }