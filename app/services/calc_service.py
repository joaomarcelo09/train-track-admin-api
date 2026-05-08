from typing import Any, Dict

import httpx

from ..core.config import settings


class CalcServiceUnavailable(Exception):
    pass


class CalcServiceClient:
    def __init__(self, base_url: str = None, transport: httpx.AsyncBaseTransport = None):
        self.base_url = (base_url or settings.calc_service_url).rstrip("/")
        self.transport = transport

    async def run_simulation(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient(
                base_url=self.base_url,
                timeout=10.0,
                transport=self.transport,
            ) as client:
                response = await client.post("/simulation/run", json=payload)
                response.raise_for_status()
                return response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise CalcServiceUnavailable("Calc service unavailable") from exc
