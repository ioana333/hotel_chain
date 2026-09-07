from fastapi import FastAPI
from .infrastructure.database import Base, engine, migrate_reservations_schema
from .infrastructure.TableEntities.ReservationEntity import ReservationEntity
from .controllers.ReservationController import router

Base.metadata.create_all(bind=engine)
migrate_reservations_schema()
app = FastAPI(title='ReservationService', version='1.0.0')
app.include_router(router)

@app.get('/health')
def health():
    return {'service': 'ReservationService', 'status': 'ok'}
