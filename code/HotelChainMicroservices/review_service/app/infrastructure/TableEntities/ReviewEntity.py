from sqlalchemy import Column, Integer, String, Float, Boolean
from ..database import Base
from ...domain.Review import Review
from ...domain.ReviewID import ReviewID

class ReviewEntity(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, nullable=False)
    client_id = Column(Integer, nullable=False)
    client_name = Column(String(500), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String(500), nullable=False)
    created_at = Column(String(500), nullable=False)

    def __init__(self, item: Review | None = None, **kwargs):
        if item is not None:
            self.room_id = item.room_id
            self.client_id = item.client_id
            self.client_name = item.client_name
            self.rating = item.rating
            self.comment = item.comment
            self.created_at = item.created_at
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_domain(self) -> Review:
        return Review(id=ReviewID(self.id), room_id=self.room_id, client_id=self.client_id, client_name=self.client_name, rating=self.rating, comment=self.comment, created_at=self.created_at)

    def update_from_domain(self, item: Review) -> None:
        self.room_id = item.room_id
        self.client_id = item.client_id
        self.client_name = item.client_name
        self.rating = item.rating
        self.comment = item.comment
        self.created_at = item.created_at
