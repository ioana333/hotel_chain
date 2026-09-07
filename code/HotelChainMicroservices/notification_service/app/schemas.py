from pydantic import BaseModel

class NotificationCreate(BaseModel):
    user_id: int = 0
    channel: str = 'email'
    recipient: str = ''
    message: str = ''
    status: str = 'sent'
    created_at: str = ''

class NotificationUpdate(NotificationCreate):
    pass

class NotificationOut(BaseModel):
    id: int
    user_id: int
    channel: str
    recipient: str
    message: str
    status: str
    created_at: str
