from model.api_client import HotelAPIClient
from .commands import Command


class MainVM:
    def __init__(self):
        self.api = HotelAPIClient()
        self.current_user = None
        self.load_hotels_command = Command(self.load_hotels)
        self.load_rooms_command = Command(self.load_rooms)
        self.login_command = Command(lambda: None)

    def load_hotels(self):
        return self.api.get('hotel')

    def load_rooms(self, **filters):
        return self.api.get('room', **filters)

    def load_reviews(self, room_id=None):
        params = {'room_id': room_id} if room_id else {}
        return self.api.get('review', **params)

    def load_reservations(self, **filters):
        return self.api.get('reservation', **filters)

    def client_has_reservation(self, room_id: int, client_id: int) -> bool:
        rows = self.load_reservations(room_id=room_id, client_id=client_id)
        return len(rows) > 0

    def login(self, username, password):
        result = self.api.post('user', 'login', {'username': username, 'password': password})
        self.current_user = result['user']
        return self.current_user

    def create_room(self, data):
        return self.api.post('room', data=data)

    def update_room(self, room_id, data):
        return self.api.put('room', str(room_id), data=data)

    def delete_room(self, room_id):
        return self.api.delete('room', str(room_id))

    def reserve_room(self, data):
        return self.api.post('reservation', data=data)

    def add_review(self, data):
        return self.api.post('review', data=data)

    def load_users(self, role=None, username=None):
        return self.api.get('user', role=role, username=username)

    def create_user(self, data):
        return self.api.post('user', data=data)

    def update_user(self, user_id, data):
        return self.api.put('user', str(user_id), data=data)

    def delete_user(self, user_id):
        return self.api.delete('user', str(user_id))

    def update_user_credentials(self, user_id, data):
        return self.api.put('user', f'{user_id}/credentials', data=data)

    def export(self, service, fmt, output_path=None):
        return self.api.get(service, f'export/{fmt}', output_path=output_path)

    def stats(self, service, criterion):
        return self.api.get(service, f'statistics/{criterion}')
