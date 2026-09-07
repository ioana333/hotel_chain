from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str = ''
    password: str = ''
    role: str = 'client'
    full_name: str = ''
    email: str = ''
    phone: str = ''
    is_active: bool = True

class UserUpdate(UserCreate):
    pass

class UserOut(BaseModel):
    id: int
    username: str
    password: str
    role: str
    full_name: str
    email: str
    phone: str
    is_active: bool
