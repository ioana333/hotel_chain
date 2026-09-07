from .ReviewID import ReviewID

class Review:
    def __init__(self, id: ReviewID | None = None, room_id: int = 1, client_id: int = 1, client_name: str = '', rating: int = 5, comment: str = '', created_at: str = ''):
        self.id = id
        self.room_id = room_id
        self.client_id = client_id
        self.client_name = client_name
        self.rating = rating
        self.comment = comment
        self.created_at = created_at

    def to_dict(self) -> dict:
        return {'id': self.id.value if self.id else None, 'room_id': self.room_id, 'client_id': self.client_id, 'client_name': self.client_name, 'rating': self.rating, 'comment': self.comment, 'created_at': self.created_at}
