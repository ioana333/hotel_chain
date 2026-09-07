from pydantic import BaseModel

class HotelCreate(BaseModel):
    name: str = ''
    location: str = ''
    address: str = ''
    stars: int = 3
    description: str = ''

class HotelUpdate(HotelCreate):
    pass

class HotelOut(BaseModel):
    id: int
    name: str
    location: str
    address: str
    stars: int
    description: str
