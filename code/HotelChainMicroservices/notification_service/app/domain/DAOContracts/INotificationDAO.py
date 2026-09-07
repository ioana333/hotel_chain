from abc import ABC, abstractmethod
from typing import Optional
from ..Notification import Notification

class INotificationDAO(ABC):
    @abstractmethod
    def list(self, **filters) -> list[Notification]: raise NotImplementedError
    @abstractmethod
    def get(self, id: int) -> Optional[Notification]: raise NotImplementedError
    @abstractmethod
    def create(self, item: Notification) -> Notification: raise NotImplementedError
    @abstractmethod
    def update(self, item: Notification) -> bool: raise NotImplementedError
    @abstractmethod
    def delete(self, id: int) -> bool: raise NotImplementedError
