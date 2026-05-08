from typing import List

from pydantic import BaseModel, Field


class SimulationRunRequest(BaseModel):
    train_id: str = Field(..., min_length=1)
    line_id: str = Field(..., min_length=1)


class SimulationTrackPayload(BaseModel):
    length: int
    bending: int
    elevation: int


class SimulationTrainPayload(BaseModel):
    weight: int
    train_cars: int


class SimulationLinePayload(BaseModel):
    id: str
    name: str
    total_length: int


class SimulationCalcPayload(BaseModel):
    train: SimulationTrainPayload
    line: SimulationLinePayload
    tracks: List[SimulationTrackPayload]


class SimulationPointTrack(BaseModel):
    length: int
    bending: int
    elevation: int


class SimulationPoint(BaseModel):
    track_index: int
    distance: int
    electricity_usage: int
    track: SimulationPointTrack


class SimulationResult(BaseModel):
    total_energy: int
    points: List[SimulationPoint]
