# Фоновая задача обновления погодных условий
from celery import shared_task
from app.services.weather import get_weather_along_route

@shared_task
def update_weather_for_route(route_id: int, coordinates: list[tuple[float, float]]):
    """
    Асинхронно обновляет погодные данные для маршрута с заданными координатами
    """
    weather_data = get_weather_along_route(coordinates)
    # Сохраняем в БД или кэш (реализация зависит от архитектуры хранилища)
    print(f"Weather for route {route_id}: {weather_data}")

