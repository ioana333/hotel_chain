from abc import ABC, abstractmethod
from typing import Optional
from ..Room import Room

class IRoomDAO(ABC):
    @abstractmethod
    def list(self, **filters) -> list[Room]: raise NotImplementedError
    @abstractmethod
    def get(self, id: int) -> Optional[Room]: raise NotImplementedError
    @abstractmethod
    def create(self, item: Room) -> Room: raise NotImplementedError
    @abstractmethod
    def update(self, item: Room) -> bool: raise NotImplementedError
    @abstractmethod
    def delete(self, id: int) -> bool: raise NotImplementedError
