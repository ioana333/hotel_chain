from sqlalchemy import Column, Integer, String, Float, Boolean
from ..database import Base
from ...domain.Notification import Notification
from ...domain.NotificationID import NotificationID

class NotificationEntity(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    channel = Column(String(500), nullable=False)
    recipient = Column(String(500), nullable=False)
    message = Column(String(500), nullable=False)
    status = Column(String(500), nullable=False)
    created_at = Column(String(500), nullable=False)

    def __init__(self, item: Notification | None = None, **kwargs):
        if item is not None:
            self.user_id = item.user_id
            self.channel = item.channel
            self.recipient = item.recipient
            self.message = item.message
            self.status = item.status
            self.created_at = item.created_at
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_domain(self) -> Notification:
        return Notification(id=NotificationID(self.id), user_id=self.user_id, channel=self.channel, recipient=self.recipient, message=self.message, status=self.status, created_at=self.created_at)

    def update_from_domain(self, item: Notification) -> None:
        self.user_id = item.user_id
        self.channel = item.channel
        self.recipient = item.recipient
        self.message = item.message
        self.status = item.status
        self.created_at = item.created_at
