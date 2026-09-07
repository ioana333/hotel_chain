from sqlalchemy.orm import Session

# Importurile creează tabelele prin Base.metadata.create_all în main la rulare, dar aici le creăm direct.
from hotel_service.app.infrastructure.database import Base as HotelBase, engine as hotel_engine, SessionLocal as HotelSession
from hotel_service.app.infrastructure.TableEntities.HotelEntity import HotelEntity
from room_service.app.infrastructure.database import Base as RoomBase, engine as room_engine, SessionLocal as RoomSession
from room_service.app.infrastructure.TableEntities.RoomEntity import RoomEntity
from user_service.app.infrastructure.database import Base as UserBase, engine as user_engine, SessionLocal as UserSession
from user_service.app.infrastructure.TableEntities.UserEntity import UserEntity
from reservation_service.app.infrastructure.database import Base as ReservationBase, engine as reservation_engine, SessionLocal as ReservationSession
from reservation_service.app.infrastructure.TableEntities.ReservationEntity import ReservationEntity
from review_service.app.infrastructure.database import Base as ReviewBase, engine as review_engine, SessionLocal as ReviewSession
from review_service.app.infrastructure.TableEntities.ReviewEntity import ReviewEntity
from notification_service.app.infrastructure.database import Base as NotificationBase, engine as notification_engine, SessionLocal as NotificationSession
from notification_service.app.infrastructure.TableEntities.NotificationEntity import NotificationEntity


def reset_and_seed():
    pairs = [
        (HotelBase, hotel_engine, HotelSession, HotelEntity),
        (RoomBase, room_engine, RoomSession, RoomEntity),
        (UserBase, user_engine, UserSession, UserEntity),
        (ReservationBase, reservation_engine, ReservationSession, ReservationEntity),
        (ReviewBase, review_engine, ReviewSession, ReviewEntity),
        (NotificationBase, notification_engine, NotificationSession, NotificationEntity),
    ]
    for base, engine, session_cls, _ in pairs:
        base.metadata.drop_all(bind=engine)
        base.metadata.create_all(bind=engine)

    db: Session = HotelSession()
    db.add_all([
        HotelEntity(name='Hotel Central', location='Cluj-Napoca', address='', stars=0, description=''),
        HotelEntity(name='Hotel Transilvania', location='Brașov', address='', stars=0, description=''),
        HotelEntity(name='Hotel Riviera', location='Constanța', address='', stars=0, description=''),
    ])
    db.commit(); db.close()

    db = RoomSession()
    db.add_all([
        RoomEntity(hotel_id=1, room_number='101', location='Cluj-Napoca', floor=1, room_type='', price_per_night=210, position='street view', facilities='wifi,tv,ac', image_urls='', is_available=True, max_guests=1),
        RoomEntity(hotel_id=1, room_number='102', location='Cluj-Napoca', floor=1, room_type='', price_per_night=320, position='garden view', facilities='wifi,tv,ac,minibar', image_urls='', is_available=True, max_guests=1),
        RoomEntity(hotel_id=1, room_number='203', location='Cluj-Napoca', floor=1, room_type='', price_per_night=550, position='city view', facilities='wifi,tv,ac,minibar,jacuzzi', image_urls='', is_available=False, max_guests=1),
        RoomEntity(hotel_id=2, room_number='11', location='Brașov', floor=1, room_type='', price_per_night=360, position='mountain view', facilities='wifi,tv,parking', image_urls='', is_available=True, max_guests=1),
        RoomEntity(hotel_id=3, room_number='501', location='Constanța', floor=1, room_type='', price_per_night=690, position='sea view', facilities='wifi,tv,ac,balcony', image_urls='', is_available=True, max_guests=1),
    ])
    db.commit(); db.close()

    db = UserSession()
    db.add_all([
        UserEntity(username='client', password='client', role='client', full_name='Client Demo', email='client@example.com', phone='0700000001', is_active=True),
        UserEntity(username='angajat', password='angajat', role='employee', full_name='Angajat Demo', email='angajat@example.com', phone='0700000002', is_active=True),
        UserEntity(username='manager', password='manager', role='manager', full_name='Manager Demo', email='manager@example.com', phone='0700000003', is_active=True),
        UserEntity(username='admin', password='admin', role='admin', full_name='Administrator Demo', email='admin@example.com', phone='0700000004', is_active=True),
    ])
    db.commit(); db.close()

    db = ReservationSession()
    db.add_all([
        ReservationEntity(hotel_id=1, room_id=3, client_id=1, client_name='Client Demo', client_email='client@example.com', client_phone='+40700111222', start_date='2026-05-20', end_date='2026-05-22', status='reserved', total_price=0),
    ])
    db.commit(); db.close()

    db = ReviewSession()
    db.add_all([
        ReviewEntity(room_id=3, client_id=1, client_name='Client Demo', rating=5, comment='Cameră curată și personal amabil.', created_at=''),
        ReviewEntity(room_id=3, client_id=1, client_name='Client Demo', rating=4, comment='Foarte bine, mic dejun bun.', created_at=''),
    ])
    db.commit(); db.close()

    db = NotificationSession()
    # Nu adăugăm notificări demonstrative care nu apar în cerință.
    # Tabelul se completează când administratorul modifică informații de autentificare.
    db.commit(); db.close()
    print('Bazele SQLite au fost inițializate cu date demo.')

if __name__ == '__main__':
    reset_and_seed()
