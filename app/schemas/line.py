from pydantic import BaseModel, Field
from typing import Optional

class LineBase(BaseModel):
    name: str = Field(..., min_length=1)

class LineCreate(LineBase):
    pass

class LineUpdate(LineBase):
    pass

class LineResponse(LineBase):
    id: str

    class Config:
        from_attributes = True