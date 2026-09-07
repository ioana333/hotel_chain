from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from email.message import EmailMessage
import os
import smtplib


class Observer(ABC):
    @abstractmethod
    def update(self, user: dict, change: str) -> dict:
        raise NotImplementedError


class Subject:
    """Observer comportamental: modificarea unui user notifica mai multi observatori."""

    def __init__(self):
        self._observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def notify(self, user: dict, change: str) -> list[dict]:
        return [observer.update(user, change) for observer in self._observers]


class EmailObserver(Observer):
    """Trimite email real prin SMTP_SSL cand credidentialele sunt configurate."""

    def update(self, user: dict, change: str) -> dict:
        recipient = user.get('email', '')
        account_details = (
            f"Username: {user.get('username', '')}\n"
            f"Parola: {user.get('password', '')}\n"
            f"Rol: {user.get('role', '')}\n"
            f"Nume: {user.get('full_name', '')}\n"
            f"Email: {user.get('email', '')}\n"
            f"Telefon: {user.get('phone', '')}"
        )
        message = f"Contul tau a fost modificat: {change}. Noile date sunt:\n{account_details}"
        result = {
            'channel': 'email',
            'to': recipient,
            'message': message,
            'sent_at': datetime.now().isoformat(timespec='seconds'),
            'status': 'sent',
        }

        sender = os.getenv('HOTELCHAIN_SMTP_EMAIL', '')
        password = os.getenv('HOTELCHAIN_SMTP_PASSWORD', '')
        host = os.getenv('HOTELCHAIN_SMTP_HOST', 'smtp.gmail.com')
        port = int(os.getenv('HOTELCHAIN_SMTP_PORT', '465'))

        if not recipient:
            result['status'] = 'failed'
            result['message'] = f"{message} Nu exista adresa email pentru utilizator."
            return result
        if not sender or not password:
            result['status'] = 'simulated'
            result['message'] = f"{message} SMTP neconfigurat; notificarea email a fost simulata."
            return result

        try:
            email = EmailMessage()
            email['Subject'] = 'HotelChain - modificare date autentificare'
            email['From'] = sender
            email['To'] = recipient
            email.set_content(
                "Buna,\n\n"
                f"Contul tau HotelChain a fost modificat: {change}.\n\n"
                "Noile date ale contului sunt:\n"
                f"{account_details}\n\n"
                "Daca nu ai solicitat aceasta modificare, contacteaza administratorul hotelului.\n\n"
                "HotelChain"
            )
            with smtplib.SMTP_SSL(host, port) as connection:
                connection.login(sender, password)
                connection.send_message(email)
        except Exception as exc:
            result['status'] = 'failed'
            result['message'] = f"{message} Trimiterea email a esuat: {exc}"

        return result


class SMSObserver(Observer):
    def update(self, user: dict, change: str) -> dict:
        return {
            'channel': 'sms',
            'to': user.get('phone', ''),
            'message': f"Date autentificare modificate: {change}",
            'sent_at': datetime.now().isoformat(timespec='seconds'),
            'status': 'simulated',
        }


class LegacyWhatsAppGateway:
    def send_text(self, number: str, text: str) -> dict:
        return {'legacy_status': 'queued', 'number': number, 'text': text}


class WhatsAppAdapter(Observer):
    """Adapter structural: adapteaza LegacyWhatsAppGateway la interfata Observer."""

    def __init__(self, gateway: LegacyWhatsAppGateway | None = None):
        self.gateway = gateway or LegacyWhatsAppGateway()

    def update(self, user: dict, change: str) -> dict:
        result = self.gateway.send_text(user.get('phone', ''), f"WhatsApp: {change}")
        return {
            'channel': 'whatsapp',
            'to': result['number'],
            'message': result['text'],
            'sent_at': datetime.now().isoformat(timespec='seconds'),
            'status': 'simulated',
        }
