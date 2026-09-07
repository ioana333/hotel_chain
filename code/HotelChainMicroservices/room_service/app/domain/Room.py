from .RoomID import RoomID

class Room:
    def __init__(self, id: RoomID | None = None, hotel_id: int = 1, room_number: str = '', location: str = '', floor: int = 1, room_type: str = 'Single', price_per_night: float = 0.0, position: str = '', facilities: str = '', image_urls: str = '', is_available: bool = True, max_guests: int = 1):
        self.id = id
        self.hotel_id = hotel_id
        self.room_number = room_number
        self.location = location
        self.floor = floor
        self.room_type = room_type
        self.price_per_night = price_per_night
        self.position = position
        self.facilities = facilities
        self.image_urls = image_urls
        self.is_available = is_available
        self.max_guests = max_guests

    def to_dict(self) -> dict:
        return {'id': self.id.value if self.id else None, 'hotel_id': self.hotel_id, 'room_number': self.room_number, 'location': self.location, 'floor': self.floor, 'room_type': self.room_type, 'price_per_night': self.price_per_night, 'position': self.position, 'facilities': self.facilities, 'image_urls': self.image_urls, 'is_available': self.is_available, 'max_guests': self.max_guests}
