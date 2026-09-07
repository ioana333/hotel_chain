from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..infrastructure.database import get_db
from ..infrastructure.NotificationDAO import NotificationDAO, item_from_payload
from ..services.NotificationsService import NotificationsService
from ..schemas import NotificationCreate, NotificationUpdate, NotificationOut

router = APIRouter(prefix='/api/notifications', tags=['NotificationService'])

class NotificationController:
    def __init__(self, repository: NotificationDAO):
        self.service = NotificationsService(repository)

def service_factory(db: Session) -> NotificationsService:
    return NotificationsService(NotificationDAO(db))

def payload(model) -> dict:
    return model.model_dump() if hasattr(model, 'model_dump') else model.dict()

@router.get('', response_model=list[NotificationOut])
def GetAll(user_id: int | None = None, channel: str | None = None, db: Session = Depends(get_db)):
    filters = {'user_id': user_id, 'channel': channel}
    filters = {key: value for key, value in filters.items() if value is not None}
    return [item.to_dict() for item in service_factory(db).list(**filters)]

@router.get('/export/{fmt}')
def Export(fmt: str, user_id: int | None = None, channel: str | None = None, db: Session = Depends(get_db)):
    filters = {'user_id': user_id, 'channel': channel}
    filters = {key: value for key, value in filters.items() if value is not None}
    return {'path': service_factory(db).export(fmt, **filters)}


@router.post('/send-auth-change')
def SendAuthChange(user: dict, db: Session = Depends(get_db)):
    from common.notifications import Subject, EmailObserver, SMSObserver, WhatsAppAdapter
    subject = Subject()
    subject.attach(EmailObserver())
    subject.attach(SMSObserver())
    # cerința cere cel puțin 2 variante; păstrăm și WhatsApp ca opțiune suplimentară prin Adapter
    subject.attach(WhatsAppAdapter())
    sent = subject.notify(user, 'modificare informații autentificare')
    service = service_factory(db)
    saved = []
    for notification in sent:
        item = item_from_payload({
            'user_id': user.get('id', 0) or 0,
            'channel': notification['channel'],
            'recipient': notification['to'],
            'message': notification['message'],
            'status': notification.get('status', 'sent'),
            'created_at': notification['sent_at'],
        })
        saved_item = service.create(item).to_dict()
        prefix = "[EMAIL REAL]" if saved_item['channel'] == 'email' and saved_item['status'] == 'sent' else "[SIMULARE NOTIFICARE]"
        print(
            f"{prefix} user_id={saved_item['user_id']} "
            f"canal={saved_item['channel']} catre={saved_item['recipient']} "
            f"status={saved_item['status']} "
            f"mesaj={saved_item['message']}",
            flush=True,
        )
        saved.append(saved_item)
    return {'sent': saved}

@router.get('/{id}', response_model=NotificationOut)
def GetById(id: int, db: Session = Depends(get_db)):
    item = service_factory(db).get(id)
    if item is None:
        raise HTTPException(status_code=404, detail='Notification not found')
    return item.to_dict()

@router.post('', response_model=NotificationOut, status_code=201)
def Create(item: NotificationCreate, db: Session = Depends(get_db)):
    created = service_factory(db).create(item_from_payload(payload(item)))
    return created.to_dict()

@router.put('/{id}', response_model=NotificationOut)
def Update(id: int, item: NotificationUpdate, db: Session = Depends(get_db)):
    service = service_factory(db)
    ok = service.update(item_from_payload(payload(item), id=id))
    if not ok:
        raise HTTPException(status_code=404, detail='Notification not found')
    return service.get(id).to_dict()

@router.delete('/{id}')
def Delete(id: int, db: Session = Depends(get_db)):
    ok = service_factory(db).delete(id)
    if not ok:
        raise HTTPException(status_code=404, detail='Notification not found')
    return {'deleted': True}
