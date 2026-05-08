from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from ..services.train_service import TrainService
from ..schemas.train import TrainCreate, TrainResponse
from ..auth.jwt_handler import get_current_user

router = APIRouter(prefix="/trains", tags=["Trains"])

@router.post("", response_model=TrainResponse, status_code=status.HTTP_201_CREATED)
async def create_train(train_data: TrainCreate, current_user = Depends(get_current_user)):
    service = TrainService()
    return await service.create_train(train_data)

@router.get("", response_model=List[TrainResponse])
async def list_trains(current_user = Depends(get_current_user)):
    service = TrainService()
    return await service.get_all_trains()

@router.get("/{train_id}", response_model=TrainResponse)
async def get_train(train_id: str, current_user = Depends(get_current_user)):
    service = TrainService()
    train = await service.get_train(train_id)
    if not train:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Train not found")
    return train

@router.put("/{train_id}", response_model=TrainResponse)
async def update_train(train_id: str, train_data: TrainCreate, current_user = Depends(get_current_user)):
    service = TrainService()
    train = await service.update_train(train_id, train_data)
    if not train:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Train not found")
    return train

@router.delete("/{train_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_train(train_id: str, current_user = Depends(get_current_user)):
    service = TrainService()
    deleted = await service.delete_train(train_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Train not found")