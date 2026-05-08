from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from ..services.line_service import LineService
from ..schemas.line import LineCreate, LineResponse
from ..auth.jwt_handler import get_current_user

router = APIRouter(prefix="/lines", tags=["Lines"])

@router.post("", response_model=LineResponse, status_code=status.HTTP_201_CREATED)
async def create_line(line_data: LineCreate, current_user = Depends(get_current_user)):
    service = LineService()
    try:
        return await service.create_line(line_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.get("", response_model=List[LineResponse])
async def list_lines(current_user = Depends(get_current_user)):
    service = LineService()
    return await service.get_all_lines()

@router.get("/{line_id}", response_model=LineResponse)
async def get_line(line_id: str, current_user = Depends(get_current_user)):
    service = LineService()
    line = await service.get_line(line_id)
    if not line:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Line not found")
    return line

@router.put("/{line_id}", response_model=LineResponse)
async def update_line(line_id: str, line_data: LineCreate, current_user = Depends(get_current_user)):
    service = LineService()
    try:
        line = await service.update_line(line_id, line_data)
        if not line:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Line not found")
        return line
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.delete("/{line_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_line(line_id: str, current_user = Depends(get_current_user)):
    service = LineService()
    deleted = await service.delete_line(line_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Line not found")