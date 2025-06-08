# Интерфейс маршрутизатора
from abc import ABC, abstractmethod

class RoutingProvider(ABC):
    @abstractmethod
    def get_route(self, origin: str, destination: str, height: float, weight: int):
        pass
