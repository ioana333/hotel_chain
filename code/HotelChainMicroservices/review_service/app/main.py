from fastapi import FastAPI
from .infrastructure.database import Base, engine
from .infrastructure.TableEntities.ReviewEntity import ReviewEntity
from .controllers.ReviewController import router

Base.metadata.create_all(bind=engine)
app = FastAPI(title='ReviewService', version='1.0.0')
app.include_router(router)

@app.get('/health')
def health():
    return {'service': 'ReviewService', 'status': 'ok'}
