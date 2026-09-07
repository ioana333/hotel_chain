from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import requests
from ..infrastructure.database import get_db
from ..infrastructure.ReviewDAO import ReviewDAO, item_from_payload
from ..services.ReviewsService import ReviewsService
from ..schemas import ReviewCreate, ReviewUpdate, ReviewOut

router = APIRouter(prefix='/api/reviews', tags=['ReviewService'])

class ReviewController:
    def __init__(self, repository: ReviewDAO):
        self.service = ReviewsService(repository)

def service_factory(db: Session) -> ReviewsService:
    return ReviewsService(ReviewDAO(db))

def payload(model) -> dict:
    return model.model_dump() if hasattr(model, 'model_dump') else model.dict()


def normalize(value) -> str:
    return str(value or '').strip().lower()


def get_client_identity(client_id: int) -> dict:
    try:
        response = requests.get(f'http://127.0.0.1:8005/api/users/{client_id}', timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception:
        return {}


def client_has_reservation(room_id: int, client_id: int) -> bool:
    """Verifică prin REST dacă utilizatorul logat are o rezervare pentru camera respectivă.
    ReviewService nu accesează direct baza ReservationService, ci comunică prin API, ca microserviciile să rămână separate.
    """
    try:
        response = requests.get(
            'http://127.0.0.1:8003/api/reservations',
            params={'room_id': room_id},
            timeout=5,
        )
        response.raise_for_status()
    except Exception:
        raise HTTPException(status_code=503, detail='ReservationService nu este disponibil. Pornește toate microserviciile înainte de a adăuga un review.')
    reservations = response.json()
    user = get_client_identity(client_id)
    user_email = normalize(user.get('email'))
    user_name = normalize(user.get('full_name') or user.get('username'))
    for reservation in reservations:
        if int(reservation.get('client_id') or 0) == client_id:
            return True
        if user_email and normalize(reservation.get('client_email')) == user_email:
            return True
        if user_name and normalize(reservation.get('client_name')) == user_name:
            return True
    return False

@router.get('', response_model=list[ReviewOut])
def GetAll(room_id: int | None = None, client_id: int | None = None, db: Session = Depends(get_db)):
    filters = {'room_id': room_id, 'client_id': client_id}
    filters = {key: value for key, value in filters.items() if value is not None}
    return [item.to_dict() for item in service_factory(db).list(**filters)]

@router.get('/export/{fmt}')
def Export(fmt: str, room_id: int | None = None, client_id: int | None = None, db: Session = Depends(get_db)):
    filters = {'room_id': room_id, 'client_id': client_id}
    filters = {key: value for key, value in filters.items() if value is not None}
    return {'path': service_factory(db).export(fmt, **filters)}


@router.get('/{id}', response_model=ReviewOut)
def GetById(id: int, db: Session = Depends(get_db)):
    item = service_factory(db).get(id)
    if item is None:
        raise HTTPException(status_code=404, detail='Review not found')
    return item.to_dict()

@router.post('', response_model=ReviewOut, status_code=201)
def Create(item: ReviewCreate, db: Session = Depends(get_db)):
    data = payload(item)
    room_id = int(data.get('room_id') or 0)
    client_id = int(data.get('client_id') or 0)
    if not client_has_reservation(room_id, client_id):
        raise HTTPException(status_code=400, detail='Nu poți lăsa review deoarece nu ai rezervat această cameră cu acest cont de client.')
    created = service_factory(db).create(item_from_payload(data))
    return created.to_dict()

@router.put('/{id}', response_model=ReviewOut)
def Update(id: int, item: ReviewUpdate, db: Session = Depends(get_db)):
    service = service_factory(db)
    ok = service.update(item_from_payload(payload(item), id=id))
    if not ok:
        raise HTTPException(status_code=404, detail='Review not found')
    return service.get(id).to_dict()

@router.delete('/{id}')
def Delete(id: int, db: Session = Depends(get_db)):
    ok = service_factory(db).delete(id)
    if not ok:
        raise HTTPException(status_code=404, detail='Review not found')
    return {'deleted': True}
