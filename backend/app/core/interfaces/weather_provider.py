# Интерфейс погодного сервиса
from abc import ABC, abstractmethod

class WeatherProvider(ABC):
    @abstractmethod
    def get_weather(self, lat: float, lon: float):
        pass
