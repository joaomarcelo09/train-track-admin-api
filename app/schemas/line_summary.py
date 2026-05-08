from typing import Optional, Dict, Any
import uuid

class LineSummary(BaseModel):
    line_id: str
    total_length: int
    average_elevation: float
    max_elevation: int
    average_bending: float
    tracks: int

    class Config:
        from_attributes = True