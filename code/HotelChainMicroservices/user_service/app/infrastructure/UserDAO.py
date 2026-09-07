from typing import Optional
from sqlalchemy.orm import Session
from .TableEntities.UserEntity import UserEntity
from ..domain.User import User
from ..domain.UserID import UserID
from ..domain.DAOContracts.IUserDAO import IUserDAO

class UserDAO(IUserDAO):
    def __init__(self, db_context: Session):
        self.db_context = db_context

    def list(self, **filters) -> list[User]:
        query = self.db_context.query(UserEntity)
        if filters.get('role') is not None:
            query = query.filter(UserEntity.role == filters.get('role'))
        if filters.get('username') is not None:
            query = query.filter(UserEntity.username == filters.get('username'))
        return [entity.to_domain() for entity in query.order_by(UserEntity.id).all()]

    def get(self, id: int) -> Optional[User]:
        entity = self.db_context.query(UserEntity).filter(UserEntity.id == id).first()
        return entity.to_domain() if entity else None

    def create(self, item: User) -> User:
        entity = UserEntity(item)
        self.db_context.add(entity)
        self.db_context.commit()
        self.db_context.refresh(entity)
        return entity.to_domain()

    def update(self, item: User) -> bool:
        item_id = item.id.value if item.id else None
        entity = self.db_context.query(UserEntity).filter(UserEntity.id == item_id).first()
        if entity is None:
            return False
        entity.update_from_domain(item)
        self.db_context.commit()
        return True

    def delete(self, id: int) -> bool:
        entity = self.db_context.query(UserEntity).filter(UserEntity.id == id).first()
        if entity is None:
            return False
        self.db_context.delete(entity)
        self.db_context.commit()
        return True

def item_from_payload(data: dict, id: int | None = None) -> User:
    def pick(*names, default=None):
        for name in names:
            if name in data and data[name] is not None:
                return data[name]
        return default
    item_id = id if id is not None else pick('id', 'Id', default=None)
    return User(
        id=UserID(int(item_id)) if item_id is not None else None,
        username=str(pick('username', 'Username', default='')),
        password=str(pick('password', 'Password', default='')),
        role=str(pick('role', 'Role', default='client')),
        full_name=str(pick('full_name', 'FullName', default='')),
        email=str(pick('email', 'Email', default='')),
        phone=str(pick('phone', 'Phone', default='')),
        is_active=bool(pick('is_active', 'IsActive', default=True))
    )
