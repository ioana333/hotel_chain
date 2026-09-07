from .ReservationID import ReservationID

class Reservation:
    def __init__(self, id: ReservationID | None = None, hotel_id: int = 1, room_id: int = 1, client_id: int = 1, client_name: str = '', client_email: str = '', client_phone: str = '', start_date: str = '', end_date: str = '', status: str = 'reserved', total_price: float = 0.0):
        self.id = id
        self.hotel_id = hotel_id
        self.room_id = room_id
        self.client_id = client_id
        self.client_name = client_name
        self.client_email = client_email
        self.client_phone = client_phone
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.total_price = total_price

    def to_dict(self) -> dict:
        return {'id': self.id.value if self.id else None, 'hotel_id': self.hotel_id, 'room_id': self.room_id, 'client_id': self.client_id, 'client_name': self.client_name, 'client_email': self.client_email, 'client_phone': self.client_phone, 'start_date': self.start_date, 'end_date': self.end_date, 'status': self.status, 'total_price': self.total_price}
