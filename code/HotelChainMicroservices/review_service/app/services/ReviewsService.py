from common.exporters import ExporterFactory, keep_fields
from common.config import get_settings
from ..domain.DAOContracts.IReviewDAO import IReviewDAO
from ..domain.Review import Review

class ReviewsService:
    def __init__(self, repository: IReviewDAO):
        self.repository = repository

    def list(self, **filters) -> list[Review]:
        return self.repository.list(**filters)

    def get(self, id: int):
        return self.repository.get(id)

    def create(self, item: Review) -> Review:
        return self.repository.create(item)

    def update(self, item: Review) -> bool:
        return self.repository.update(item)

    def delete(self, id: int) -> bool:
        return self.repository.delete(id)

    def export(self, fmt: str, **filters) -> str:
        rows = keep_fields([item.to_dict() for item in self.list(**filters)], ['room_id', 'client_name', 'rating', 'comment'])
        path = get_settings().export_path(f'reviews.{fmt}')
        return ExporterFactory.create(fmt).export(rows, path)

