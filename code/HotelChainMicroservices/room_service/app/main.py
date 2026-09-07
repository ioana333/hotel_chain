from fastapi import FastAPI
from .infrastructure.database import Base, engine
from .infrastructure.TableEntities.RoomEntity import RoomEntity
from .controllers.RoomController import router

Base.metadata.create_all(bind=engine)
app = FastAPI(title='RoomService', version='1.0.0')
app.include_router(router)

@app.get('/health')
def health():
    return {'service': 'RoomService', 'status': 'ok'}
