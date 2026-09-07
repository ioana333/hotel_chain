from abc import ABC, abstractmethod
from typing import Optional
from ..Review import Review

class IReviewDAO(ABC):
    @abstractmethod
    def list(self, **filters) -> list[Review]: raise NotImplementedError
    @abstractmethod
    def get(self, id: int) -> Optional[Review]: raise NotImplementedError
    @abstractmethod
    def create(self, item: Review) -> Review: raise NotImplementedError
    @abstractmethod
    def update(self, item: Review) -> bool: raise NotImplementedError
    @abstractmethod
    def delete(self, id: int) -> bool: raise NotImplementedError
