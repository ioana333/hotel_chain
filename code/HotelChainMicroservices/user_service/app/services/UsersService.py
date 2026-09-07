from common.exporters import ExporterFactory, keep_fields
from common.config import get_settings
from ..domain.DAOContracts.IUserDAO import IUserDAO
from ..domain.User import User

class UsersService:
    def __init__(self, repository: IUserDAO):
        self.repository = repository

    def list(self, **filters) -> list[User]:
        return self.repository.list(**filters)

    def get(self, id: int):
        return self.repository.get(id)

    def create(self, item: User) -> User:
        return self.repository.create(item)

    def update(self, item: User) -> bool:
        return self.repository.update(item)

    def delete(self, id: int) -> bool:
        return self.repository.delete(id)

    def export(self, fmt: str, **filters) -> str:
        rows = keep_fields([item.to_dict() for item in self.list(**filters)], ['id', 'username', 'role', 'full_name', 'email', 'phone'])
        path = get_settings().export_path(f'users.{fmt}')
        return ExporterFactory.create(fmt).export(rows, path)

