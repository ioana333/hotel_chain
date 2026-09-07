from typing import Optional
from sqlalchemy.orm import Session
from .TableEntities.HotelEntity import HotelEntity
from ..domain.Hotel import Hotel
from ..domain.HotelID import HotelID
from ..domain.DAOContracts.IHotelDAO import IHotelDAO

class HotelDAO(IHotelDAO):
    def __init__(self, db_context: Session):
        self.db_context = db_context

    def list(self, **filters) -> list[Hotel]:
        query = self.db_context.query(HotelEntity)
        if filters.get('location') is not None:
            query = query.filter(HotelEntity.location == filters.get('location'))
        return [entity.to_domain() for entity in query.order_by(HotelEntity.id).all()]

    def get(self, id: int) -> Optional[Hotel]:
        entity = self.db_context.query(HotelEntity).filter(HotelEntity.id == id).first()
        return entity.to_domain() if entity else None

    def create(self, item: Hotel) -> Hotel:
        entity = HotelEntity(item)
        self.db_context.add(entity)
        self.db_context.commit()
        self.db_context.refresh(entity)
        return entity.to_domain()

    def update(self, item: Hotel) -> bool:
        item_id = item.id.value if item.id else None
        entity = self.db_context.query(HotelEntity).filter(HotelEntity.id == item_id).first()
        if entity is None:
            return False
        entity.update_from_domain(item)
        self.db_context.commit()
        return True

    def delete(self, id: int) -> bool:
        entity = self.db_context.query(HotelEntity).filter(HotelEntity.id == id).first()
        if entity is None:
            return False
        self.db_context.delete(entity)
        self.db_context.commit()
        return True

def item_from_payload(data: dict, id: int | None = None) -> Hotel:
    def pick(*names, default=None):
        for name in names:
            if name in data and data[name] is not None:
                return data[name]
        return default
    item_id = id if id is not None else pick('id', 'Id', default=None)
    return Hotel(
        id=HotelID(int(item_id)) if item_id is not None else None,
        name=str(pick('name', 'Name', default='')),
        location=str(pick('location', 'Location', default='')),
        address=str(pick('address', 'Address', default='')),
        stars=int(pick('stars', 'Stars', default=3)),
        description=str(pick('description', 'Description', default=''))
    )
