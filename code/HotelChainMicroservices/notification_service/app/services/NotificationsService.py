from common.exporters import ExporterFactory, keep_fields
from common.config import get_settings
from ..domain.DAOContracts.INotificationDAO import INotificationDAO
from ..domain.Notification import Notification

class NotificationsService:
    def __init__(self, repository: INotificationDAO):
        self.repository = repository

    def list(self, **filters) -> list[Notification]:
        return self.repository.list(**filters)

    def get(self, id: int):
        return self.repository.get(id)

    def create(self, item: Notification) -> Notification:
        return self.repository.create(item)

    def update(self, item: Notification) -> bool:
        return self.repository.update(item)

    def delete(self, id: int) -> bool:
        return self.repository.delete(id)

    def export(self, fmt: str, **filters) -> str:
        rows = keep_fields([item.to_dict() for item in self.list(**filters)], ['user_id', 'channel', 'recipient', 'message'])
        path = get_settings().export_path(f'notifications.{fmt}')
        return ExporterFactory.create(fmt).export(rows, path)

