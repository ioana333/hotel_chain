from pydantic import BaseModel

class HotelDTO(BaseModel):
    id: int | None = None
    name: str
    location: str
    address: str
    stars: int
    description: str
