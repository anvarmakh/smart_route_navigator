# Объединяет все источники данных в маршрут
from app.providers.osrm_routing_provider import OSRMRoutingProvider

engine = OSRMRoutingProvider()

def generate_route(origin, destination, height, weight):
    """Вызывает провайдер маршрутов и возвращает результат"""
    return engine.get_route(origin, destination, height, weight)