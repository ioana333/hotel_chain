from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..infrastructure.database import get_db
from ..infrastructure.ReservationDAO import ReservationDAO, item_from_payload
from ..services.ReservationsService import ReservationsService
from ..schemas import ReservationCreate, ReservationUpdate, ReservationOut

router = APIRouter(prefix='/api/reservations', tags=['ReservationService'])

class ReservationController:
    def __init__(self, repository: ReservationDAO):
        self.service = ReservationsService(repository)

def service_factory(db: Session) -> ReservationsService:
    return ReservationsService(ReservationDAO(db))

def payload(model) -> dict:
    return model.model_dump() if hasattr(model, 'model_dump') else model.dict()

@router.get('', response_model=list[ReservationOut])
def GetAll(hotel_id: int | None = None, room_id: int | None = None, client_id: int | None = None, status: str | None = None, check_in: str | None = None, check_out: str | None = None, db: Session = Depends(get_db)):
    filters = {'hotel_id': hotel_id, 'room_id': room_id, 'client_id': client_id, 'status': status, 'check_in': check_in, 'check_out': check_out}
    filters = {key: value for key, value in filters.items() if value is not None}
    return [item.to_dict() for item in service_factory(db).list(**filters)]

@router.get('/export/{fmt}')
def Export(fmt: str, output_path: str | None = None, hotel_id: int | None = None, room_id: int | None = None, client_id: int | None = None, status: str | None = None, db: Session = Depends(get_db)):
    filters = {'hotel_id': hotel_id, 'room_id': room_id, 'client_id': client_id, 'status': status}
    filters = {key: value for key, value in filters.items() if value is not None}
    return {'path': service_factory(db).export(fmt, output_path=output_path, **filters)}


@router.get('/statistics/{criterion}')
def Statistics(criterion: str, db: Session = Depends(get_db)):
    try:
        return service_factory(db).statistics(criterion)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@router.get('/{id}', response_model=ReservationOut)
def GetById(id: int, db: Session = Depends(get_db)):
    item = service_factory(db).get(id)
    if item is None:
        raise HTTPException(status_code=404, detail='Reservation not found')
    return item.to_dict()

@router.post('', response_model=ReservationOut, status_code=201)
def Create(item: ReservationCreate, db: Session = Depends(get_db)):
    try:
        created = service_factory(db).create(item_from_payload(payload(item)))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return created.to_dict()

@router.put('/{id}', response_model=ReservationOut)
def Update(id: int, item: ReservationUpdate, db: Session = Depends(get_db)):
    service = service_factory(db)
    try:
        ok = service.update(item_from_payload(payload(item), id=id))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    if not ok:
        raise HTTPException(status_code=404, detail='Reservation not found')
    return service.get(id).to_dict()

@router.delete('/{id}')
def Delete(id: int, db: Session = Depends(get_db)):
    ok = service_factory(db).delete(id)
    if not ok:
        raise HTTPException(status_code=404, detail='Reservation not found')
    return {'deleted': True}
