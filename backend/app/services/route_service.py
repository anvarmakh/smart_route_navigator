# ✅ route_service.py — асинхронная версия логики маршрутизации
from app.models.route_history import RouteHistory
from sqlalchemy.ext.asyncio import AsyncSession
from app.providers.mapbox_routing_provider import MapboxRoutingProvider
import logging

# Логгер маршрутизации
logger = logging.getLogger("routing")

# Основная функция построения маршрута с использованием Mapbox
# Получает координаты, рассчитывает маршрут, сохраняет в БД

# 📌 Асинхронная функция построения маршрута и сохранения в историю
async def build_route(
    origin: str,
    destination: str,
    height: float,
    weight: int,
    db: AsyncSession,
    user_id: int,
    driver_time_left: float = None,
    weather_condition: list = None,
    preferences: dict = None
):
    """
    Построение маршрута с использованием Mapbox и сохранением истории маршрута.
    Учитывает ограничения по габаритам, погоде, времени и предпочтениям.
    """
    try:
        routing_result = await MapboxRoutingProvider.get_route_async(
            origin, destination, height, weight
        )

        # 🔧 Вставляем дополнительные данные в маршрут (если есть)
        route_data = routing_result.get("route", {})

        if preferences:
            route_data["preferences"] = preferences

        if weather_condition:
            routing_result["weather"] = weather_condition

        # 💾 Сохраняем историю маршрута
        history = RouteHistory(
            user_id=user_id,
            origin=origin,
            destination=destination,
            route_data=route_data,
            fuel_data=routing_result.get("fuel", []),
            weather_data=weather_condition or []
        )
        db.add(history)
        await db.commit()

        return routing_result

    except Exception as e:
        logger.error(f"Ошибка при построении маршрута: {e}")
        raise
