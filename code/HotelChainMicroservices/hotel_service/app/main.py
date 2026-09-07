from fastapi import FastAPI
from .infrastructure.database import Base, engine
from .infrastructure.TableEntities.HotelEntity import HotelEntity
from .controllers.HotelController import router

Base.metadata.create_all(bind=engine)
app = FastAPI(title='HotelService', version='1.0.0')
app.include_router(router)

@app.get('/health')
def health():
    return {'service': 'HotelService', 'status': 'ok'}
