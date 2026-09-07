from sqlalchemy import Column, Integer, String, Float, Boolean
from ..database import Base
from ...domain.Reservation import Reservation
from ...domain.ReservationID import ReservationID

class ReservationEntity(Base):
    __tablename__ = 'reservations'
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, nullable=False, default=1)
    room_id = Column(Integer, nullable=False)
    client_id = Column(Integer, nullable=False)
    client_name = Column(String(500), nullable=False)
    client_email = Column(String(500), nullable=False)
    client_phone = Column(String(100), nullable=False, default='')
    start_date = Column(String(500), nullable=False)
    end_date = Column(String(500), nullable=False)
    status = Column(String(500), nullable=False)
    total_price = Column(Float, nullable=False)

    def __init__(self, item: Reservation | None = None, **kwargs):
        if item is not None:
            self.hotel_id = item.hotel_id
            self.room_id = item.room_id
            self.client_id = item.client_id
            self.client_name = item.client_name
            self.client_email = item.client_email
            self.client_phone = item.client_phone
            self.start_date = item.start_date
            self.end_date = item.end_date
            self.status = item.status
            self.total_price = item.total_price
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_domain(self) -> Reservation:
        return Reservation(id=ReservationID(self.id), hotel_id=getattr(self, 'hotel_id', 1) or 1, room_id=self.room_id, client_id=self.client_id, client_name=self.client_name, client_email=self.client_email, client_phone=getattr(self, 'client_phone', '') or '', start_date=self.start_date, end_date=self.end_date, status=self.status, total_price=self.total_price)

    def update_from_domain(self, item: Reservation) -> None:
        self.hotel_id = item.hotel_id
        self.room_id = item.room_id
        self.client_id = item.client_id
        self.client_name = item.client_name
        self.client_email = item.client_email
        self.client_phone = item.client_phone
        self.start_date = item.start_date
        self.end_date = item.end_date
        self.status = item.status
        self.total_price = item.total_price
