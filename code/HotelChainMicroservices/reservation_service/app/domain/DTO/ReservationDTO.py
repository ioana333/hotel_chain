from pydantic import BaseModel

class ReservationDTO(BaseModel):
    id: int | None = None
    room_id: int
    client_id: int
    client_name: str
    client_email: str
    start_date: str
    end_date: str
    status: str
    total_price: float
