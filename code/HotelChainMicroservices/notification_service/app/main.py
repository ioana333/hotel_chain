from fastapi import FastAPI
from .infrastructure.database import Base, engine
from .infrastructure.TableEntities.NotificationEntity import NotificationEntity
from .controllers.NotificationController import router

Base.metadata.create_all(bind=engine)
app = FastAPI(title='NotificationService', version='1.0.0')
app.include_router(router)

@app.get('/health')
def health():
    return {'service': 'NotificationService', 'status': 'ok'}
