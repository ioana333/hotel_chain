from pydantic import BaseModel

class ReviewCreate(BaseModel):
    room_id: int = 1
    client_id: int = 1
    client_name: str = ''
    rating: int = 5
    comment: str = ''
    created_at: str = ''

class ReviewUpdate(ReviewCreate):
    pass

class ReviewOut(BaseModel):
    id: int
    room_id: int
    client_id: int
    client_name: str
    rating: int
    comment: str
    created_at: str
