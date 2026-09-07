from abc import ABC, abstractmethod
from typing import Optional
from ..Hotel import Hotel

class IHotelDAO(ABC):
    @abstractmethod
    def list(self, **filters) -> list[Hotel]: raise NotImplementedError
    @abstractmethod
    def get(self, id: int) -> Optional[Hotel]: raise NotImplementedError
    @abstractmethod
    def create(self, item: Hotel) -> Hotel: raise NotImplementedError
    @abstractmethod
    def update(self, item: Hotel) -> bool: raise NotImplementedError
    @abstractmethod
    def delete(self, id: int) -> bool: raise NotImplementedError
