from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import text
from common.config import get_settings

DATABASE_URL = get_settings().sqlite_url('reservations.db')
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def migrate_reservations_schema() -> None:
    with engine.begin() as connection:
        columns = {row[1] for row in connection.execute(text("PRAGMA table_info(reservations)")).fetchall()}
        if not columns:
            return
        if 'hotel_id' not in columns:
            connection.execute(text("ALTER TABLE reservations ADD COLUMN hotel_id INTEGER NOT NULL DEFAULT 1"))
        if 'client_phone' not in columns:
            connection.execute(text("ALTER TABLE reservations ADD COLUMN client_phone VARCHAR(100) NOT NULL DEFAULT ''"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
