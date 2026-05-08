from pydantic import BaseModel, Field, field_validator
from typing import Optional
import uuid

class TrainBase(BaseModel):
    weight: int = Field(..., gt=0)
    train_cars: int = Field(..., gt=0)

class TrainCreate(TrainBase):
    pass

class TrainUpdate(TrainBase):
    pass

class TrainResponse(TrainBase):
    id: str

    class Config:
        from_attributes = True