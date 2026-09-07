from typing import Optional
from sqlalchemy.orm import Session
from .TableEntities.NotificationEntity import NotificationEntity
from ..domain.Notification import Notification
from ..domain.NotificationID import NotificationID
from ..domain.DAOContracts.INotificationDAO import INotificationDAO

class NotificationDAO(INotificationDAO):
    def __init__(self, db_context: Session):
        self.db_context = db_context

    def list(self, **filters) -> list[Notification]:
        query = self.db_context.query(NotificationEntity)
        if filters.get('user_id') is not None:
            query = query.filter(NotificationEntity.user_id == filters.get('user_id'))
        if filters.get('channel') is not None:
            query = query.filter(NotificationEntity.channel == filters.get('channel'))
        return [entity.to_domain() for entity in query.order_by(NotificationEntity.id).all()]

    def get(self, id: int) -> Optional[Notification]:
        entity = self.db_context.query(NotificationEntity).filter(NotificationEntity.id == id).first()
        return entity.to_domain() if entity else None

    def create(self, item: Notification) -> Notification:
        entity = NotificationEntity(item)
        self.db_context.add(entity)
        self.db_context.commit()
        self.db_context.refresh(entity)
        return entity.to_domain()

    def update(self, item: Notification) -> bool:
        item_id = item.id.value if item.id else None
        entity = self.db_context.query(NotificationEntity).filter(NotificationEntity.id == item_id).first()
        if entity is None:
            return False
        entity.update_from_domain(item)
        self.db_context.commit()
        return True

    def delete(self, id: int) -> bool:
        entity = self.db_context.query(NotificationEntity).filter(NotificationEntity.id == id).first()
        if entity is None:
            return False
        self.db_context.delete(entity)
        self.db_context.commit()
        return True

def item_from_payload(data: dict, id: int | None = None) -> Notification:
    def pick(*names, default=None):
        for name in names:
            if name in data and data[name] is not None:
                return data[name]
        return default
    item_id = id if id is not None else pick('id', 'Id', default=None)
    return Notification(
        id=NotificationID(int(item_id)) if item_id is not None else None,
        user_id=int(pick('user_id', 'UserId', default=0)),
        channel=str(pick('channel', 'Channel', default='email')),
        recipient=str(pick('recipient', 'Recipient', default='')),
        message=str(pick('message', 'Message', default='')),
        status=str(pick('status', 'Status', default='sent')),
        created_at=str(pick('created_at', 'CreatedAt', default=''))
    )
