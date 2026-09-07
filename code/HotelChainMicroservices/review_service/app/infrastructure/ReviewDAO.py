from typing import Optional
from sqlalchemy.orm import Session
from .TableEntities.ReviewEntity import ReviewEntity
from ..domain.Review import Review
from ..domain.ReviewID import ReviewID
from ..domain.DAOContracts.IReviewDAO import IReviewDAO

class ReviewDAO(IReviewDAO):
    def __init__(self, db_context: Session):
        self.db_context = db_context

    def list(self, **filters) -> list[Review]:
        query = self.db_context.query(ReviewEntity)
        if filters.get('room_id') is not None:
            query = query.filter(ReviewEntity.room_id == filters.get('room_id'))
        if filters.get('client_id') is not None:
            query = query.filter(ReviewEntity.client_id == filters.get('client_id'))
        return [entity.to_domain() for entity in query.order_by(ReviewEntity.id).all()]

    def get(self, id: int) -> Optional[Review]:
        entity = self.db_context.query(ReviewEntity).filter(ReviewEntity.id == id).first()
        return entity.to_domain() if entity else None

    def create(self, item: Review) -> Review:
        entity = ReviewEntity(item)
        self.db_context.add(entity)
        self.db_context.commit()
        self.db_context.refresh(entity)
        return entity.to_domain()

    def update(self, item: Review) -> bool:
        item_id = item.id.value if item.id else None
        entity = self.db_context.query(ReviewEntity).filter(ReviewEntity.id == item_id).first()
        if entity is None:
            return False
        entity.update_from_domain(item)
        self.db_context.commit()
        return True

    def delete(self, id: int) -> bool:
        entity = self.db_context.query(ReviewEntity).filter(ReviewEntity.id == id).first()
        if entity is None:
            return False
        self.db_context.delete(entity)
        self.db_context.commit()
        return True

def item_from_payload(data: dict, id: int | None = None) -> Review:
    def pick(*names, default=None):
        for name in names:
            if name in data and data[name] is not None:
                return data[name]
        return default
    item_id = id if id is not None else pick('id', 'Id', default=None)
    return Review(
        id=ReviewID(int(item_id)) if item_id is not None else None,
        room_id=int(pick('room_id', 'RoomId', default=1)),
        client_id=int(pick('client_id', 'ClientId', default=1)),
        client_name=str(pick('client_name', 'ClientName', default='')),
        rating=int(pick('rating', 'Rating', default=5)),
        comment=str(pick('comment', 'Comment', default='')),
        created_at=str(pick('created_at', 'CreatedAt', default=''))
    )
