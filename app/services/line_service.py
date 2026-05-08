from typing import Optional, Dict, Any, List
from ..repositories.line_repository import LineRepository
from ..schemas.line import LineCreate, LineResponse

class LineService:
    def __init__(self):
        self.repository = LineRepository()

    async def create_line(self, line_data: LineCreate) -> LineResponse:
        existing = await self.repository.get_by_name(line_data.name)
        if existing:
            raise ValueError(f"Line with name '{line_data.name}' already exists")
        data = line_data.dict()
        line = await self.repository.create(data)
        return LineResponse(**line)

    async def get_line(self, line_id: str) -> Optional[LineResponse]:
        line = await self.repository.get_by_id(line_id)
        if line:
            return LineResponse(**line)
        return None

    async def get_all_lines(self) -> List[LineResponse]:
        lines = await self.repository.get_all()
        return [LineResponse(**line) for line in lines]

    async def update_line(self, line_id: str, line_data: LineCreate) -> Optional[LineResponse]:
        if await self.repository.name_exists(line_data.name, line_id):
            raise ValueError(f"Line with name '{line_data.name}' already exists")
        line = await self.repository.update(line_id, line_data.dict())
        if line:
            return LineResponse(**line)
        return None

    async def delete_line(self, line_id: str) -> bool:
        return await self.repository.delete(line_id)