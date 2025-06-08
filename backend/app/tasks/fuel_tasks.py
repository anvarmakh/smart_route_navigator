# Фоновая задача обновления цен на топливо
from celery import shared_task
from app.services.fuel import get_nearby_fuel_prices

@shared_task
def update_fuel_prices(location: tuple[float, float]):
    """
    Асинхронно обновляет цены на топливо по указанным координатам
    """
    prices = get_nearby_fuel_prices(location)
    # Сохраняем в БД или кэш (реализация зависит от архитектуры хранилища)
    print(f"Fuel prices at {location}: {prices}")
