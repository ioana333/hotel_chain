from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..infrastructure.database import get_db
from ..infrastructure.UserDAO import UserDAO, item_from_payload
from ..services.UsersService import UsersService
from ..schemas import UserCreate, UserUpdate, UserOut

router = APIRouter(prefix='/api/users', tags=['UserService'])

class UserController:
    def __init__(self, repository: UserDAO):
        self.service = UsersService(repository)

def service_factory(db: Session) -> UsersService:
    return UsersService(UserDAO(db))

def payload(model) -> dict:
    return model.model_dump() if hasattr(model, 'model_dump') else model.dict()

def notify_auth_change(user: dict) -> None:
    try:
        import requests
        requests.post('http://127.0.0.1:8006/api/notifications/send-auth-change', json=user, timeout=1)
    except Exception as exc:
        print(
            f"[SIMULARE NOTIFICARE] NotificationService indisponibil pentru user_id={user.get('id')}. "
            f"S-ar trimite email/SMS/WhatsApp la modificarea datelor de autentificare. Detaliu: {exc}",
            flush=True,
        )

@router.get('', response_model=list[UserOut])
def GetAll(role: str | None = None, username: str | None = None, db: Session = Depends(get_db)):
    filters = {'role': role, 'username': username}
    filters = {key: value for key, value in filters.items() if value is not None}
    return [item.to_dict() for item in service_factory(db).list(**filters)]

@router.get('/export/{fmt}')
def Export(fmt: str, role: str | None = None, username: str | None = None, db: Session = Depends(get_db)):
    filters = {'role': role, 'username': username}
    filters = {key: value for key, value in filters.items() if value is not None}
    return {'path': service_factory(db).export(fmt, **filters)}


@router.post('/login')
def Login(payload: dict, db: Session = Depends(get_db)):
    username = payload.get('username', '')
    password = payload.get('password', '')
    users = service_factory(db).list(username=username)
    for user in users:
        if user.password == password and user.is_active:
            return {'authenticated': True, 'user': user.to_dict()}
    raise HTTPException(status_code=401, detail='Username sau parolă greșită')

@router.put('/{id}/credentials', response_model=UserOut)
def UpdateCredentials(id: int, payload: dict, db: Session = Depends(get_db)):
    service = service_factory(db)
    current = service.get(id)
    if current is None:
        raise HTTPException(status_code=404, detail='User not found')
    data = current.to_dict()
    data.update(payload)
    ok = service.update(item_from_payload(data, id=id))
    if not ok:
        raise HTTPException(status_code=404, detail='User not found')
    updated = service.get(id)
    notify_auth_change(updated.to_dict())
    return updated.to_dict()

@router.get('/{id}', response_model=UserOut)
def GetById(id: int, db: Session = Depends(get_db)):
    item = service_factory(db).get(id)
    if item is None:
        raise HTTPException(status_code=404, detail='User not found')
    return item.to_dict()

@router.post('', response_model=UserOut, status_code=201)
def Create(item: UserCreate, db: Session = Depends(get_db)):
    created = service_factory(db).create(item_from_payload(payload(item)))
    return created.to_dict()

@router.put('/{id}', response_model=UserOut)
def Update(id: int, item: UserUpdate, db: Session = Depends(get_db)):
    service = service_factory(db)
    before = service.get(id)
    if before is None:
        raise HTTPException(status_code=404, detail='User not found')
    ok = service.update(item_from_payload(payload(item), id=id))
    if not ok:
        raise HTTPException(status_code=404, detail='User not found')
    updated = service.get(id)
    watched_fields = ('username', 'password', 'email', 'phone')
    if any(getattr(before, field) != getattr(updated, field) for field in watched_fields):
        notify_auth_change(updated.to_dict())
    return updated.to_dict()

@router.delete('/{id}')
def Delete(id: int, db: Session = Depends(get_db)):
    ok = service_factory(db).delete(id)
    if not ok:
        raise HTTPException(status_code=404, detail='User not found')
    return {'deleted': True}
