from .NotificationID import NotificationID

class Notification:
    def __init__(self, id: NotificationID | None = None, user_id: int = 0, channel: str = 'email', recipient: str = '', message: str = '', status: str = 'sent', created_at: str = ''):
        self.id = id
        self.user_id = user_id
        self.channel = channel
        self.recipient = recipient
        self.message = message
        self.status = status
        self.created_at = created_at

    def to_dict(self) -> dict:
        return {'id': self.id.value if self.id else None, 'user_id': self.user_id, 'channel': self.channel, 'recipient': self.recipient, 'message': self.message, 'status': self.status, 'created_at': self.created_at}
