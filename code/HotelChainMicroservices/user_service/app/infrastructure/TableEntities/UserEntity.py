from sqlalchemy import Column, Integer, String, Float, Boolean
from ..database import Base
from ...domain.User import User
from ...domain.UserID import UserID

class UserEntity(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(500), nullable=False)
    password = Column(String(500), nullable=False)
    role = Column(String(500), nullable=False)
    full_name = Column(String(500), nullable=False)
    email = Column(String(500), nullable=False)
    phone = Column(String(500), nullable=False)
    is_active = Column(Boolean, nullable=False)

    def __init__(self, item: User | None = None, **kwargs):
        if item is not None:
            self.username = item.username
            self.password = item.password
            self.role = item.role
            self.full_name = item.full_name
            self.email = item.email
            self.phone = item.phone
            self.is_active = item.is_active
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_domain(self) -> User:
        return User(id=UserID(self.id), username=self.username, password=self.password, role=self.role, full_name=self.full_name, email=self.email, phone=self.phone, is_active=self.is_active)

    def update_from_domain(self, item: User) -> None:
        self.username = item.username
        self.password = item.password
        self.role = item.role
        self.full_name = item.full_name
        self.email = item.email
        self.phone = item.phone
        self.is_active = item.is_active
