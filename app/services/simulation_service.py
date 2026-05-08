from typing import Any, Dict, List

from ..schemas.simulation import SimulationCalcPayload, SimulationResult
from .calc_service import CalcServiceClient
from .line_service import LineService
from .track_service import TrackService
from .train_service import TrainService


class SimulationValidationError(Exception):
    pass


class SimulationService:
    def __init__(self, calc_client: CalcServiceClient = None):
        self.train_service = TrainService()
        self.line_service = LineService()
        self.track_service = TrackService()
        self.calc_client = calc_client or CalcServiceClient()

    async def run_simulation(self, train_id: str, line_id: str) -> SimulationResult:
        train = await self.train_service.get_train(train_id)
        if not train:
            raise SimulationValidationError("Train not found")

        line = await self.line_service.get_line(line_id)
        if not line:
            raise SimulationValidationError("Line not found")

        tracks = await self.track_service.get_tracks_by_line(line_id)
        if not tracks:
            raise SimulationValidationError("Line has no tracks")

        sorted_tracks = self._sort_tracks(tracks)
        payload = SimulationCalcPayload(
            train={
                "weight": train.weight,
                "train_cars": train.train_cars,
            },
            line={
                "id": line.id,
                "name": line.name,
                "total_length": sum(track.length for track in sorted_tracks),
            },
            tracks=[
                {
                    "length": track.length,
                    "bending": track.bending,
                    "elevation": track.elevation,
                }
                for track in sorted_tracks
            ],
        )

        result = await self.calc_client.run_simulation(payload.model_dump())
        return SimulationResult(**result)

    def _sort_tracks(self, tracks: List[Any]) -> List[Any]:
        indexed_tracks = list(enumerate(tracks))
        return [
            track
            for _, track in sorted(
                indexed_tracks,
                key=lambda indexed_track: (
                    self._route_order(indexed_track[1]),
                    indexed_track[0],
                ),
            )
        ]

    def _route_order(self, track: Any) -> int:
        route_order = getattr(track, "route_order", None)
        return route_order if route_order is not None else 0
