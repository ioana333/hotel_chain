from pydantic import BaseModel

class RoomCreate(BaseModel):
    hotel_id: int = 1
    room_number: str = ''
    location: str = ''
    floor: int = 1
    room_type: str = 'Single'
    price_per_night: float = 0.0
    position: str = ''
    facilities: str = ''
    image_urls: str = ''
    is_available: bool = True
    max_guests: int = 1

class RoomUpdate(RoomCreate):
    pass

class RoomOut(BaseModel):
    id: int
    hotel_id: int
    room_number: str
    location: str
    floor: int
    room_type: str
    price_per_night: float
    position: str
    facilities: str
    image_urls: str
    is_available: bool
    max_guests: int
