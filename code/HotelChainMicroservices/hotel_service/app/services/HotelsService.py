from common.exporters import ExporterFactory, keep_fields
from common.config import get_settings
from ..domain.DAOContracts.IHotelDAO import IHotelDAO
from ..domain.Hotel import Hotel

class HotelsService:
    def __init__(self, repository: IHotelDAO):
        self.repository = repository

    def list(self, **filters) -> list[Hotel]:
        return self.repository.list(**filters)

    def get(self, id: int):
        return self.repository.get(id)

    def create(self, item: Hotel) -> Hotel:
        return self.repository.create(item)

    def update(self, item: Hotel) -> bool:
        return self.repository.update(item)

    def delete(self, id: int) -> bool:
        return self.repository.delete(id)

    def export(self, fmt: str, **filters) -> str:
        rows = keep_fields([item.to_dict() for item in self.list(**filters)], ['id', 'name', 'location'])
        path = get_settings().export_path(f'hotels.{fmt}')
        return ExporterFactory.create(fmt).export(rows, path)

