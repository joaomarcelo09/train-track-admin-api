from fastapi import APIRouter, Depends, HTTPException, status

from ..auth.jwt_handler import get_current_user
from ..schemas.simulation import SimulationResult, SimulationRunRequest
from ..services.calc_service import CalcServiceUnavailable
from ..services.simulation_service import SimulationService, SimulationValidationError

router = APIRouter(prefix="/simulation", tags=["Simulation"])


def get_simulation_service() -> SimulationService:
    return SimulationService()


@router.post("/run", response_model=SimulationResult)
async def run_simulation(
    request: SimulationRunRequest,
    current_user=Depends(get_current_user),
    service: SimulationService = Depends(get_simulation_service),
):
    try:
        return await service.run_simulation(request.train_id, request.line_id)
    except SimulationValidationError as exc:
        detail = str(exc)
        if detail in {"Train not found", "Line not found"}:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
    except CalcServiceUnavailable as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        )
