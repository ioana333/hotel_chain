from __future__ import annotations
from abc import ABC, abstractmethod
from collections import Counter, defaultdict
from datetime import datetime

class StatisticsStrategy(ABC):
    @abstractmethod
    def calculate(self, rows: list[dict]) -> dict:
        raise NotImplementedError

class RoomsByAvailabilityStrategy(StatisticsStrategy):
    def calculate(self, rows: list[dict]) -> dict:
        counter = Counter('available' if row.get('is_available') else 'reserved' for row in rows)
        return dict(counter)

class RoomsByPositionStrategy(StatisticsStrategy):
    def calculate(self, rows: list[dict]) -> dict:
        return dict(Counter(row.get('position', 'unknown') for row in rows))

class AveragePriceByHotelStrategy(StatisticsStrategy):
    def calculate(self, rows: list[dict]) -> dict:
        values = defaultdict(list)
        for row in rows:
            values[str(row.get('hotel_id'))].append(float(row.get('price_per_night') or 0))
        return {hotel: round(sum(prices) / len(prices), 2) for hotel, prices in values.items() if prices}

class ReservationsByMonthStrategy(StatisticsStrategy):
    def calculate(self, rows: list[dict]) -> dict:
        counter = Counter()
        for row in rows:
            date_text = row.get('start_date') or ''
            try:
                key = datetime.fromisoformat(date_text).strftime('%Y-%m')
            except Exception:
                key = 'unknown'
            counter[key] += 1
        return dict(counter)

class ReservationsByStatusStrategy(StatisticsStrategy):
    def calculate(self, rows: list[dict]) -> dict:
        return dict(Counter(row.get('status', 'unknown') or 'unknown' for row in rows))

class StatisticsContext:
    """Strategy: obiectul context folosește algoritmul primit, fără să-l cunoască în detaliu."""
    def __init__(self, strategy: StatisticsStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: StatisticsStrategy) -> None:
        self.strategy = strategy

    def calculate(self, rows: list[dict]) -> dict:
        return self.strategy.calculate(rows)
