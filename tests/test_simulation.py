from types import SimpleNamespace

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient, MockTransport, Request, Response

from app.auth.jwt_handler import get_current_user
from app.api.simulation import get_simulation_service
from app.main import app
from app.services.calc_service import CalcServiceClient, CalcServiceUnavailable
from app.services.simulation_service import SimulationService, SimulationValidationError


@pytest_asyncio.fixture
async def app_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


def authenticate_requests():
    async def fake_current_user():
        return {"id": "user-id", "email": "test@example.com"}

    app.dependency_overrides[get_current_user] = fake_current_user


def build_simulation_service(train=None, line=None, tracks=None, calc_result=None, calc_error=None):
    service = SimulationService.__new__(SimulationService)
    captured = {}

    class FakeTrainService:
        async def get_train(self, train_id):
            captured["train_id"] = train_id
            return train

    class FakeLineService:
        async def get_line(self, line_id):
            captured["line_id"] = line_id
            return line

    class FakeTrackService:
        async def get_tracks_by_line(self, line_id):
            captured["tracks_line_id"] = line_id
            return tracks or []

    class FakeCalcClient:
        async def run_simulation(self, payload):
            captured["payload"] = payload
            if calc_error:
                raise calc_error
            return calc_result

    service.train_service = FakeTrainService()
    service.line_service = FakeLineService()
    service.track_service = FakeTrackService()
    service.calc_client = FakeCalcClient()
    return service, captured


@pytest.mark.asyncio
async def test_simulation_service_sends_payload_and_returns_result():
    calc_result = {
        "total_energy": 12000,
        "points": [
            {
                "track_index": 0,
                "distance": 500,
                "electricity_usage": 120,
                "track": {"length": 500, "bending": 5, "elevation": 100},
            }
        ],
    }
    service, captured = build_simulation_service(
        train=SimpleNamespace(id="train-id", weight=2000, train_cars=12),
        line=SimpleNamespace(id="line-id", name="North Route"),
        tracks=[
            SimpleNamespace(id="track-2", length=700, bending=7, elevation=110, route_order=1),
            SimpleNamespace(id="track-1", length=500, bending=5, elevation=100, route_order=0),
        ],
        calc_result=calc_result,
    )

    result = await service.run_simulation("train-id", "line-id")

    assert result.total_energy == 12000
    assert captured["payload"] == {
        "train": {"weight": 2000, "train_cars": 12},
        "line": {"id": "line-id", "name": "North Route", "total_length": 1200},
        "tracks": [
            {"length": 500, "bending": 5, "elevation": 100},
            {"length": 700, "bending": 7, "elevation": 110},
        ],
    }


@pytest.mark.asyncio
async def test_simulation_service_validates_train_exists():
    service, _ = build_simulation_service(train=None)

    with pytest.raises(SimulationValidationError, match="Train not found"):
        await service.run_simulation("missing-train", "line-id")


@pytest.mark.asyncio
async def test_simulation_service_validates_line_exists():
    service, _ = build_simulation_service(
        train=SimpleNamespace(id="train-id", weight=2000, train_cars=12),
        line=None,
    )

    with pytest.raises(SimulationValidationError, match="Line not found"):
        await service.run_simulation("train-id", "missing-line")


@pytest.mark.asyncio
async def test_simulation_service_rejects_line_without_tracks():
    service, _ = build_simulation_service(
        train=SimpleNamespace(id="train-id", weight=2000, train_cars=12),
        line=SimpleNamespace(id="line-id", name="North Route"),
        tracks=[],
    )

    with pytest.raises(SimulationValidationError, match="Line has no tracks"):
        await service.run_simulation("train-id", "line-id")


@pytest.mark.asyncio
async def test_run_simulation_endpoint_returns_result(app_client: AsyncClient):
    authenticate_requests()

    class FakeSimulationService:
        async def run_simulation(self, train_id, line_id):
            assert train_id == "train-id"
            assert line_id == "line-id"
            return {
                "total_energy": 12000,
                "points": [
                    {
                        "track_index": 0,
                        "distance": 500,
                        "electricity_usage": 120,
                        "track": {"length": 500, "bending": 5, "elevation": 100},
                    }
                ],
            }

    app.dependency_overrides[get_simulation_service] = lambda: FakeSimulationService()

    response = await app_client.post(
        "/simulation/run",
        json={"train_id": "train-id", "line_id": "line-id"},
        headers={"Authorization": "Bearer token"},
    )

    assert response.status_code == 200
    assert response.json()["total_energy"] == 12000


@pytest.mark.asyncio
async def test_run_simulation_endpoint_requires_authentication(app_client: AsyncClient):
    response = await app_client.post(
        "/simulation/run",
        json={"train_id": "train-id", "line_id": "line-id"},
    )

    assert response.status_code in (401, 403)


@pytest.mark.asyncio
async def test_run_simulation_endpoint_rejects_invalid_payload(app_client: AsyncClient):
    authenticate_requests()
    app.dependency_overrides[get_simulation_service] = lambda: object()

    response = await app_client.post(
        "/simulation/run",
        json={"train_id": "train-id"},
        headers={"Authorization": "Bearer token"},
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_run_simulation_endpoint_handles_line_without_tracks(app_client: AsyncClient):
    authenticate_requests()

    class FakeSimulationService:
        async def run_simulation(self, train_id, line_id):
            raise SimulationValidationError("Line has no tracks")

    app.dependency_overrides[get_simulation_service] = lambda: FakeSimulationService()

    response = await app_client.post(
        "/simulation/run",
        json={"train_id": "train-id", "line_id": "line-id"},
        headers={"Authorization": "Bearer token"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Line has no tracks"


@pytest.mark.asyncio
async def test_run_simulation_endpoint_handles_calc_service_unavailable(app_client: AsyncClient):
    authenticate_requests()

    class FakeSimulationService:
        async def run_simulation(self, train_id, line_id):
            raise CalcServiceUnavailable("Calc service unavailable")

    app.dependency_overrides[get_simulation_service] = lambda: FakeSimulationService()

    response = await app_client.post(
        "/simulation/run",
        json={"train_id": "train-id", "line_id": "line-id"},
        headers={"Authorization": "Bearer token"},
    )

    assert response.status_code == 503
    assert response.json()["detail"] == "Calc service unavailable"


@pytest.mark.asyncio
async def test_calc_service_client_posts_to_calc_service():
    captured = {}

    async def handler(request: Request) -> Response:
        captured["path"] = request.url.path
        captured["payload"] = request.read().decode()
        return Response(
            200,
            json={
                "total_energy": 12000,
                "points": [
                    {
                        "track_index": 0,
                        "distance": 500,
                        "electricity_usage": 120,
                        "track": {"length": 500, "bending": 5, "elevation": 100},
                    }
                ],
            },
        )

    calc_client = CalcServiceClient(
        base_url="http://calc.test",
        transport=MockTransport(handler),
    )
    payload = {
        "train": {"weight": 2000, "train_cars": 12},
        "line": {"id": "line-id", "name": "North Route", "total_length": 500},
        "tracks": [{"length": 500, "bending": 5, "elevation": 100}],
    }

    result = await calc_client.run_simulation(payload)

    assert captured["path"] == "/simulation/run"
    assert result["total_energy"] == 12000


@pytest.mark.asyncio
async def test_calc_service_client_raises_when_unavailable():
    async def handler(request: Request) -> Response:
        return Response(503)

    calc_client = CalcServiceClient(
        base_url="http://calc.test",
        transport=MockTransport(handler),
    )

    with pytest.raises(CalcServiceUnavailable):
        await calc_client.run_simulation({"train": {}, "line": {}, "tracks": []})
