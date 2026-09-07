from typing import Optional
import sqlite3
from sqlalchemy.orm import Session
from common.config import get_settings
from .TableEntities.RoomEntity import RoomEntity
from ..domain.Room import Room
from ..domain.RoomID import RoomID
from ..domain.DAOContracts.IRoomDAO import IRoomDAO

class RoomDAO(IRoomDAO):
    def __init__(self, db_context: Session):
        self.db_context = db_context

    def list(self, **filters) -> list[Room]:
        query = self.db_context.query(RoomEntity)
        if filters.get('hotel_id') is not None:
            query = query.filter(RoomEntity.hotel_id == filters.get('hotel_id'))
        if filters.get('location') is not None:
            query = query.filter(RoomEntity.location == filters.get('location'))
        has_stay_interval = bool(filters.get('check_in') and filters.get('check_out'))
        requested_availability = filters.get('is_available')
        if requested_availability is not None and not has_stay_interval:
            value = filters.get('is_available')
            if isinstance(value, str):
                value = value.lower() in ('true','1','yes','da')
            query = query.filter(RoomEntity.is_available == bool(value))
        if filters.get('price_max') is not None:
            query = query.filter(RoomEntity.price_per_night <= float(filters.get('price_max')))
        if filters.get('position') is not None:
            query = query.filter(RoomEntity.position == filters.get('position'))
        if filters.get('facilities'):
            query = query.filter(RoomEntity.facilities.ilike(f"%{filters.get('facilities')}%"))
        rooms = [entity.to_domain() for entity in query.order_by(RoomEntity.hotel_id, RoomEntity.location, RoomEntity.room_number).all()]
        if has_stay_interval:
            reserved_room_ids = self._reserved_room_ids(str(filters.get('check_in')), str(filters.get('check_out')))
            for room in rooms:
                if room.id and room.id.value in reserved_room_ids:
                    room.is_available = False
            if requested_availability is not None:
                value = requested_availability
                if isinstance(value, str):
                    value = value.lower() in ('true','1','yes','da')
                rooms = [room for room in rooms if room.is_available == bool(value)]
        return rooms

    def _reserved_room_ids(self, check_in: str, check_out: str) -> set[int]:
        db_path = get_settings().data_dir / 'reservations.db'
        if not db_path.exists():
            return set()
        with sqlite3.connect(db_path) as connection:
            rows = connection.execute(
                """
                SELECT room_id FROM reservations
                WHERE status IN ('reserved', 'confirmed', 'checked-in')
                  AND start_date < ?
                  AND end_date > ?
                """,
                (check_out, check_in),
            ).fetchall()
        return {int(row[0]) for row in rows}

    def get(self, id: int) -> Optional[Room]:
        entity = self.db_context.query(RoomEntity).filter(RoomEntity.id == id).first()
        return entity.to_domain() if entity else None

    def create(self, item: Room) -> Room:
        entity = RoomEntity(item)
        self.db_context.add(entity)
        self.db_context.commit()
        self.db_context.refresh(entity)
        return entity.to_domain()

    def update(self, item: Room) -> bool:
        item_id = item.id.value if item.id else None
        entity = self.db_context.query(RoomEntity).filter(RoomEntity.id == item_id).first()
        if entity is None:
            return False
        entity.update_from_domain(item)
        self.db_context.commit()
        return True

    def delete(self, id: int) -> bool:
        entity = self.db_context.query(RoomEntity).filter(RoomEntity.id == id).first()
        if entity is None:
            return False
        self.db_context.delete(entity)
        self.db_context.commit()
        return True

def item_from_payload(data: dict, id: int | None = None) -> Room:
    def pick(*names, default=None):
        for name in names:
            if name in data and data[name] is not None:
                return data[name]
        return default
    item_id = id if id is not None else pick('id', 'Id', default=None)
    return Room(
        id=RoomID(int(item_id)) if item_id is not None else None,
        hotel_id=int(pick('hotel_id', 'HotelId', default=1)),
        room_number=str(pick('room_number', 'RoomNumber', default='')),
        location=str(pick('location', 'Location', default='')),
        floor=int(pick('floor', 'Floor', default=1)),
        room_type=str(pick('room_type', 'RoomType', default='Single')),
        price_per_night=float(pick('price_per_night', 'PricePerNight', default=0.0)),
        position=str(pick('position', 'Position', default='')),
        facilities=str(pick('facilities', 'Facilities', default='')),
        image_urls=str(pick('image_urls', 'ImageUrls', default='')),
        is_available=bool(pick('is_available', 'IsAvailable', default=True)),
        max_guests=int(pick('max_guests', 'MaxGuests', default=1))
    )
