from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod
import uuid

class BaseRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def update(self, id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        pass