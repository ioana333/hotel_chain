from pydantic import BaseModel

class NotificationDTO(BaseModel):
    id: int | None = None
    user_id: int
    channel: str
    recipient: str
    message: str
    status: str
    created_at: str
