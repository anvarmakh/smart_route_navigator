# Интерфейс для геокодера (адрес → координаты)
from abc import ABC, abstractmethod

class GeocodingProvider(ABC):
    @abstractmethod
    def geocode(self, address: str):
        pass

