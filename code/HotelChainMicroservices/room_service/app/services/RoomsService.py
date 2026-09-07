from common.exporters import ExporterFactory, keep_fields
from common.config import get_settings
from common.statistics import StatisticsContext, RoomsByAvailabilityStrategy, RoomsByPositionStrategy, AveragePriceByHotelStrategy
from ..domain.DAOContracts.IRoomDAO import IRoomDAO
from ..domain.Room import Room

class RoomsService:
    def __init__(self, repository: IRoomDAO):
        self.repository = repository

    def list(self, **filters) -> list[Room]:
        return self.repository.list(**filters)

    def get(self, id: int):
        return self.repository.get(id)

    def create(self, item: Room) -> Room:
        return self.repository.create(item)

    def update(self, item: Room) -> bool:
        return self.repository.update(item)

    def delete(self, id: int) -> bool:
        return self.repository.delete(id)

    def export(self, fmt: str, **filters) -> str:
        rows = keep_fields([item.to_dict() for item in self.list(**filters)], ['id', 'hotel_id', 'room_number', 'location', 'price_per_night', 'position', 'facilities', 'is_available'])
        path = get_settings().export_path(f'rooms.{fmt}')
        return ExporterFactory.create(fmt).export(rows, path)

    def statistics(self, criterion: str) -> dict:
        rows = [item.to_dict() for item in self.list()]
        if criterion == 'availability':
            return StatisticsContext(RoomsByAvailabilityStrategy()).calculate(rows)
        if criterion == 'position':
            return StatisticsContext(RoomsByPositionStrategy()).calculate(rows)
        if criterion == 'average-price-hotel':
            return StatisticsContext(AveragePriceByHotelStrategy()).calculate(rows)
        raise ValueError('Criterii: availability, position, average-price-hotel')

