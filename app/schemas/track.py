from pydantic import BaseModel, Field, validator
from typing import Optional

class TrackBase(BaseModel):
    id_line: str
    length: int = Field(..., gt=0)
    bending: int = Field(..., ge=0)
    elevation: int

class TrackCreate(TrackBase):
    pass

class TrackUpdate(TrackBase):
    pass

class TrackResponse(TrackBase):
    id: str

    class Config:
        from_attributes = True