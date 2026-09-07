from pydantic import BaseModel

class UserDTO(BaseModel):
    id: int | None = None
    username: str
    password: str
    role: str
    full_name: str
    email: str
    phone: str
    is_active: bool
