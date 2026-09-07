from common.exporters import ExporterFactory, keep_fields
from common.config import get_settings
from datetime import date
from common.statistics import StatisticsContext, ReservationsByMonthStrategy, ReservationsByStatusStrategy
from ..domain.DAOContracts.IReservationDAO import IReservationDAO
from ..domain.Reservation import Reservation

class ReservationsService:
    def __init__(self, repository: IReservationDAO):
        self.repository = repository

    def list(self, **filters) -> list[Reservation]:
        return self.repository.list(**filters)

    def get(self, id: int):
        return self.repository.get(id)

    def create(self, item: Reservation) -> Reservation:
        self._validate_dates(item)
        if self.repository.has_overlap(item.room_id, item.start_date, item.end_date):
            raise ValueError('Camera este deja rezervata in intervalul de check-in/check-out selectat.')
        return self.repository.create(item)

    def update(self, item: Reservation) -> bool:
        self._validate_dates(item)
        exclude_id = item.id.value if item.id else None
        if self.repository.has_overlap(item.room_id, item.start_date, item.end_date, exclude_id=exclude_id):
            raise ValueError('Camera este deja rezervata in intervalul de check-in/check-out selectat.')
        return self.repository.update(item)

    def delete(self, id: int) -> bool:
        return self.repository.delete(id)

    def export(self, fmt: str, output_path: str | None = None, **filters) -> str:
        rows = keep_fields([item.to_dict() for item in self.list(**filters)], ['hotel_id', 'room_id', 'client_name', 'client_email', 'client_phone', 'start_date', 'end_date', 'status', 'total_price'])
        path = output_path or get_settings().export_path(f'reservations.{fmt}')
        return ExporterFactory.create(fmt).export(rows, path)

    def statistics(self, criterion: str) -> dict:
        rows = [item.to_dict() for item in self.list()]
        if criterion == 'month':
            return StatisticsContext(ReservationsByMonthStrategy()).calculate(rows)
        if criterion == 'status':
            return StatisticsContext(ReservationsByStatusStrategy()).calculate(rows)
        raise ValueError('Criteriu: month, status')

    def _validate_dates(self, item: Reservation) -> None:
        try:
            check_in = date.fromisoformat(item.start_date)
            check_out = date.fromisoformat(item.end_date)
        except Exception as exc:
            raise ValueError('Datele trebuie sa fie in format YYYY-MM-DD.') from exc
        if check_out <= check_in:
            raise ValueError('Check-out trebuie sa fie dupa check-in.')
