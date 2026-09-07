from sqlalchemy import Column, Integer, String, Float, Boolean
from ..database import Base
from ...domain.Hotel import Hotel
from ...domain.HotelID import HotelID

class HotelEntity(Base):
    __tablename__ = 'hotels'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(500), nullable=False)
    location = Column(String(500), nullable=False)
    address = Column(String(500), nullable=False)
    stars = Column(Integer, nullable=False)
    description = Column(String(500), nullable=False)

    def __init__(self, item: Hotel | None = None, **kwargs):
        if item is not None:
            self.name = item.name
            self.location = item.location
            self.address = item.address
            self.stars = item.stars
            self.description = item.description
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_domain(self) -> Hotel:
        return Hotel(id=HotelID(self.id), name=self.name, location=self.location, address=self.address, stars=self.stars, description=self.description)

    def update_from_domain(self, item: Hotel) -> None:
        self.name = item.name
        self.location = item.location
        self.address = item.address
        self.stars = item.stars
        self.description = item.description
