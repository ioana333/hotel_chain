from abc import ABC, abstractmethod
from typing import Optional
from ..Reservation import Reservation

class IReservationDAO(ABC):
    @abstractmethod
    def list(self, **filters) -> list[Reservation]: raise NotImplementedError
    @abstractmethod
    def get(self, id: int) -> Optional[Reservation]: raise NotImplementedError
    @abstractmethod
    def create(self, item: Reservation) -> Reservation: raise NotImplementedError
    @abstractmethod
    def update(self, item: Reservation) -> bool: raise NotImplementedError
    @abstractmethod
    def delete(self, id: int) -> bool: raise NotImplementedError
