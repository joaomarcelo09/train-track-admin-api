from typing import Optional, Dict, Any, List
from ..repositories.train_repository import TrainRepository
from ..schemas.train import TrainCreate, TrainResponse

class TrainService:
    def __init__(self):
        self.repository = TrainRepository()

    async def create_train(self, train_data: TrainCreate) -> TrainResponse:
        data = train_data.dict()
        train = await self.repository.create(data)
        return TrainResponse(**train)

    async def get_train(self, train_id: str) -> Optional[TrainResponse]:
        train = await self.repository.get_by_id(train_id)
        if train:
            return TrainResponse(**train)
        return None

    async def get_all_trains(self) -> List[TrainResponse]:
        trains = await self.repository.get_all()
        return [TrainResponse(**train) for train in trains]

    async def update_train(self, train_id: str, train_data: TrainCreate) -> Optional[TrainResponse]:
        train = await self.repository.update(train_id, train_data.dict())
        if train:
            return TrainResponse(**train)
        return None

    async def delete_train(self, train_id: str) -> bool:
        return await self.repository.delete(train_id)