from .UserID import UserID

class User:
    def __init__(self, id: UserID | None = None, username: str = '', password: str = '', role: str = 'client', full_name: str = '', email: str = '', phone: str = '', is_active: bool = True):
        self.id = id
        self.username = username
        self.password = password
        self.role = role
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.is_active = is_active

    def to_dict(self) -> dict:
        return {'id': self.id.value if self.id else None, 'username': self.username, 'password': self.password, 'role': self.role, 'full_name': self.full_name, 'email': self.email, 'phone': self.phone, 'is_active': self.is_active}
