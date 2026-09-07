from pydantic import BaseModel

class ReviewDTO(BaseModel):
    id: int | None = None
    room_id: int
    client_id: int
    client_name: str
    rating: int
    comment: str
    created_at: str
