from pydantic import BaseModel

class ReservationCreate(BaseModel):
    hotel_id: int = 1
    room_id: int = 1
    client_id: int = 1
    client_name: str = ''
    client_email: str = ''
    client_phone: str = ''
    start_date: str = ''
    end_date: str = ''
    status: str = 'reserved'
    total_price: float = 0.0

class ReservationUpdate(ReservationCreate):
    pass

class ReservationOut(BaseModel):
    id: int
    hotel_id: int
    room_id: int
    client_id: int
    client_name: str
    client_email: str
    client_phone: str
    start_date: str
    end_date: str
    status: str
    total_price: float
