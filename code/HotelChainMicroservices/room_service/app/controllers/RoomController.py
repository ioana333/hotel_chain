from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..infrastructure.database import get_db
from ..infrastructure.RoomDAO import RoomDAO, item_from_payload
from ..services.RoomsService import RoomsService
from ..schemas import RoomCreate, RoomUpdate, RoomOut

router = APIRouter(prefix='/api/rooms', tags=['RoomService'])

class RoomController:
    def __init__(self, repository: RoomDAO):
        self.service = RoomsService(repository)

def service_factory(db: Session) -> RoomsService:
    return RoomsService(RoomDAO(db))

def payload(model) -> dict:
    return model.model_dump() if hasattr(model, 'model_dump') else model.dict()

@router.get('', response_model=list[RoomOut])
def GetAll(hotel_id: int | None = None, location: str | None = None, is_available: bool | None = None, price_max: float | None = None, position: str | None = None, facilities: str | None = None, check_in: str | None = None, check_out: str | None = None, db: Session = Depends(get_db)):
    filters = {'hotel_id': hotel_id, 'location': location, 'is_available': is_available, 'price_max': price_max, 'position': position, 'facilities': facilities, 'check_in': check_in, 'check_out': check_out}
    filters = {key: value for key, value in filters.items() if value is not None}
    return [item.to_dict() for item in service_factory(db).list(**filters)]

@router.get('/export/{fmt}')
def Export(fmt: str, hotel_id: int | None = None, location: str | None = None, is_available: bool | None = None, price_max: float | None = None, position: str | None = None, facilities: str | None = None, db: Session = Depends(get_db)):
    filters = {'hotel_id': hotel_id, 'location': location, 'is_available': is_available, 'price_max': price_max, 'position': position, 'facilities': facilities}
    filters = {key: value for key, value in filters.items() if value is not None}
    return {'path': service_factory(db).export(fmt, **filters)}


@router.get('/statistics/{criterion}')
def Statistics(criterion: str, db: Session = Depends(get_db)):
    try:
        return service_factory(db).statistics(criterion)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@router.get('/{id}', response_model=RoomOut)
def GetById(id: int, db: Session = Depends(get_db)):
    item = service_factory(db).get(id)
    if item is None:
        raise HTTPException(status_code=404, detail='Room not found')
    return item.to_dict()

@router.post('', response_model=RoomOut, status_code=201)
def Create(item: RoomCreate, db: Session = Depends(get_db)):
    created = service_factory(db).create(item_from_payload(payload(item)))
    return created.to_dict()

@router.put('/{id}', response_model=RoomOut)
def Update(id: int, item: RoomUpdate, db: Session = Depends(get_db)):
    service = service_factory(db)
    ok = service.update(item_from_payload(payload(item), id=id))
    if not ok:
        raise HTTPException(status_code=404, detail='Room not found')
    return service.get(id).to_dict()

@router.delete('/{id}')
def Delete(id: int, db: Session = Depends(get_db)):
    ok = service_factory(db).delete(id)
    if not ok:
        raise HTTPException(status_code=404, detail='Room not found')
    return {'deleted': True}
