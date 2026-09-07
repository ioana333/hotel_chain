from pydantic import BaseModel

class RoomDTO(BaseModel):
    id: int | None = None
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
