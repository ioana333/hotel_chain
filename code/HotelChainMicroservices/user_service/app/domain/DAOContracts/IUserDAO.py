from abc import ABC, abstractmethod
from typing import Optional
from ..User import User

class IUserDAO(ABC):
    @abstractmethod
    def list(self, **filters) -> list[User]: raise NotImplementedError
    @abstractmethod
    def get(self, id: int) -> Optional[User]: raise NotImplementedError
    @abstractmethod
    def create(self, item: User) -> User: raise NotImplementedError
    @abstractmethod
    def update(self, item: User) -> bool: raise NotImplementedError
    @abstractmethod
    def delete(self, id: int) -> bool: raise NotImplementedError
