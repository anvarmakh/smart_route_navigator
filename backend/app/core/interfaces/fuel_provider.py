# Интерфейс поставщика информации о топливе
from abc import ABC, abstractmethod

class FuelProvider(ABC):
    @abstractmethod
    def get_prices(self, lat: float, lon: float):
        pass
