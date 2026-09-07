from sqlalchemy import Column, Integer, String, Float, Boolean
from ..database import Base
from ...domain.Room import Room
from ...domain.RoomID import RoomID

class RoomEntity(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, nullable=False)
    room_number = Column(String(500), nullable=False)
    location = Column(String(500), nullable=False)
    floor = Column(Integer, nullable=False)
    room_type = Column(String(500), nullable=False)
    price_per_night = Column(Float, nullable=False)
    position = Column(String(500), nullable=False)
    facilities = Column(String(500), nullable=False)
    image_urls = Column(String(500), nullable=False)
    is_available = Column(Boolean, nullable=False)
    max_guests = Column(Integer, nullable=False)

    def __init__(self, item: Room | None = None, **kwargs):
        if item is not None:
            self.hotel_id = item.hotel_id
            self.room_number = item.room_number
            self.location = item.location
            self.floor = item.floor
            self.room_type = item.room_type
            self.price_per_night = item.price_per_night
            self.position = item.position
            self.facilities = item.facilities
            self.image_urls = item.image_urls
            self.is_available = item.is_available
            self.max_guests = item.max_guests
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_domain(self) -> Room:
        return Room(id=RoomID(self.id), hotel_id=self.hotel_id, room_number=self.room_number, location=self.location, floor=self.floor, room_type=self.room_type, price_per_night=self.price_per_night, position=self.position, facilities=self.facilities, image_urls=self.image_urls, is_available=self.is_available, max_guests=self.max_guests)

    def update_from_domain(self, item: Room) -> None:
        self.hotel_id = item.hotel_id
        self.room_number = item.room_number
        self.location = item.location
        self.floor = item.floor
        self.room_type = item.room_type
        self.price_per_night = item.price_per_night
        self.position = item.position
        self.facilities = item.facilities
        self.image_urls = item.image_urls
        self.is_available = item.is_available
        self.max_guests = item.max_guests
