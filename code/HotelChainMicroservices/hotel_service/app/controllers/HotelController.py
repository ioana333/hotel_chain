from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..infrastructure.database import get_db
from ..infrastructure.HotelDAO import HotelDAO, item_from_payload
from ..services.HotelsService import HotelsService
from ..schemas import HotelCreate, HotelUpdate, HotelOut

router = APIRouter(prefix='/api/hotels', tags=['HotelService'])

class HotelController:
    def __init__(self, repository: HotelDAO):
        self.service = HotelsService(repository)

def service_factory(db: Session) -> HotelsService:
    return HotelsService(HotelDAO(db))

def payload(model) -> dict:
    return model.model_dump() if hasattr(model, 'model_dump') else model.dict()

@router.get('', response_model=list[HotelOut])
def GetAll(location: str | None = None, db: Session = Depends(get_db)):
    filters = {'location': location}
    filters = {key: value for key, value in filters.items() if value is not None}
    return [item.to_dict() for item in service_factory(db).list(**filters)]

@router.get('/export/{fmt}')
def Export(fmt: str, location: str | None = None, db: Session = Depends(get_db)):
    filters = {'location': location}
    filters = {key: value for key, value in filters.items() if value is not None}
    return {'path': service_factory(db).export(fmt, **filters)}


@router.get('/{id}', response_model=HotelOut)
def GetById(id: int, db: Session = Depends(get_db)):
    item = service_factory(db).get(id)
    if item is None:
        raise HTTPException(status_code=404, detail='Hotel not found')
    return item.to_dict()

@router.post('', response_model=HotelOut, status_code=201)
def Create(item: HotelCreate, db: Session = Depends(get_db)):
    created = service_factory(db).create(item_from_payload(payload(item)))
    return created.to_dict()

@router.put('/{id}', response_model=HotelOut)
def Update(id: int, item: HotelUpdate, db: Session = Depends(get_db)):
    service = service_factory(db)
    ok = service.update(item_from_payload(payload(item), id=id))
    if not ok:
        raise HTTPException(status_code=404, detail='Hotel not found')
    return service.get(id).to_dict()

@router.delete('/{id}')
def Delete(id: int, db: Session = Depends(get_db)):
    ok = service_factory(db).delete(id)
    if not ok:
        raise HTTPException(status_code=404, detail='Hotel not found')
    return {'deleted': True}
