from fastapi import FastAPI
from .infrastructure.database import Base, engine
from .infrastructure.TableEntities.UserEntity import UserEntity
from .controllers.UserController import router

Base.metadata.create_all(bind=engine)
app = FastAPI(title='UserService', version='1.0.0')
app.include_router(router)

@app.get('/health')
def health():
    return {'service': 'UserService', 'status': 'ok'}
