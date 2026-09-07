from typing import Optional
from datetime import date
from sqlalchemy.orm import Session
from .TableEntities.ReservationEntity import ReservationEntity
from ..domain.Reservation import Reservation
from ..domain.ReservationID import ReservationID
from ..domain.DAOContracts.IReservationDAO import IReservationDAO

class ReservationDAO(IReservationDAO):
    def __init__(self, db_context: Session):
        self.db_context = db_context

    def list(self, **filters) -> list[Reservation]:
        query = self.db_context.query(ReservationEntity)
        if filters.get('hotel_id') is not None:
            query = query.filter(ReservationEntity.hotel_id == filters.get('hotel_id'))
        if filters.get('room_id') is not None:
            query = query.filter(ReservationEntity.room_id == filters.get('room_id'))
        if filters.get('client_id') is not None:
            query = query.filter(ReservationEntity.client_id == filters.get('client_id'))
        if filters.get('status') is not None:
            query = query.filter(ReservationEntity.status == filters.get('status'))
        if filters.get('check_in') and filters.get('check_out'):
            check_in = str(filters.get('check_in'))
            check_out = str(filters.get('check_out'))
            query = query.filter(ReservationEntity.start_date < check_out, ReservationEntity.end_date > check_in)
        return [entity.to_domain() for entity in query.order_by(ReservationEntity.id).all()]

    def get(self, id: int) -> Optional[Reservation]:
        entity = self.db_context.query(ReservationEntity).filter(ReservationEntity.id == id).first()
        return entity.to_domain() if entity else None

    def create(self, item: Reservation) -> Reservation:
        entity = ReservationEntity(item)
        self.db_context.add(entity)
        self.db_context.commit()
        self.db_context.refresh(entity)
        return entity.to_domain()

    def has_overlap(self, room_id: int, check_in: str, check_out: str, exclude_id: int | None = None) -> bool:
        query = self.db_context.query(ReservationEntity).filter(
            ReservationEntity.room_id == room_id,
            ReservationEntity.status.in_(('reserved', 'confirmed', 'checked-in')),
            ReservationEntity.start_date < check_out,
            ReservationEntity.end_date > check_in,
        )
        if exclude_id is not None:
            query = query.filter(ReservationEntity.id != exclude_id)
        return self.db_context.query(query.exists()).scalar()

    def update(self, item: Reservation) -> bool:
        item_id = item.id.value if item.id else None
        entity = self.db_context.query(ReservationEntity).filter(ReservationEntity.id == item_id).first()
        if entity is None:
            return False
        entity.update_from_domain(item)
        self.db_context.commit()
        return True

    def delete(self, id: int) -> bool:
        entity = self.db_context.query(ReservationEntity).filter(ReservationEntity.id == id).first()
        if entity is None:
            return False
        self.db_context.delete(entity)
        self.db_context.commit()
        return True

def item_from_payload(data: dict, id: int | None = None) -> Reservation:
    def pick(*names, default=None):
        for name in names:
            if name in data and data[name] is not None:
                return data[name]
        return default
    item_id = id if id is not None else pick('id', 'Id', default=None)
    return Reservation(
        id=ReservationID(int(item_id)) if item_id is not None else None,
        hotel_id=int(pick('hotel_id', 'HotelId', default=1)),
        room_id=int(pick('room_id', 'RoomId', default=1)),
        client_id=int(pick('client_id', 'ClientId', default=1)),
        client_name=str(pick('client_name', 'ClientName', default='')),
        client_email=str(pick('client_email', 'ClientEmail', default='')),
        client_phone=str(pick('client_phone', 'ClientPhone', 'phone', 'Phone', default='')),
        start_date=str(pick('start_date', 'StartDate', 'check_in', 'CheckIn', default='')),
        end_date=str(pick('end_date', 'EndDate', 'check_out', 'CheckOut', default='')),
        status=str(pick('status', 'Status', default='reserved')),
        total_price=float(pick('total_price', 'TotalPrice', default=0.0))
    )
