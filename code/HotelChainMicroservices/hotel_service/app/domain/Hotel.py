from .HotelID import HotelID

class Hotel:
    def __init__(self, id: HotelID | None = None, name: str = '', location: str = '', address: str = '', stars: int = 3, description: str = ''):
        self.id = id
        self.name = name
        self.location = location
        self.address = address
        self.stars = stars
        self.description = description

    def to_dict(self) -> dict:
        return {'id': self.id.value if self.id else None, 'name': self.name, 'location': self.location, 'address': self.address, 'stars': self.stars, 'description': self.description}
