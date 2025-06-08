# ✅ telemetry.py — асинхронная телеметрия
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
import redis.asyncio as redis
import os
from app.services.route_service import build_route
from app.services.auth_service import get_current_user
from app.services.alert_service import notify_all_channels_async
from geopy.distance import geodesic

router = APIRouter()

# Подключение к Redis
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True
)

# 📍 Модель для приёма координат водителя
class LocationPayload(BaseModel):
    latitude: float
    longitude: float
    timestamp: str

# 🚚 Обновление текущей координаты водителя
@router.post("/api/v1/telemetry/location")
async def update_driver_location(
    payload: LocationPayload,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = current_user.id
    location_key = f"driver:{user_id}:location"
    route_key = f"driver:{user_id}:route_destination"

    # Сохраняем координату в Redis
    await redis_client.hset(location_key, mapping={
        "lat": payload.latitude,
        "lon": payload.longitude,
        "ts": payload.timestamp
    })
    await redis_client.expire(location_key, 3600)

    # Проверяем отклонение от маршрута
    dest = await redis_client.get(route_key)
    if dest:
        try:
            dest_lat, dest_lon = map(float, dest.split(","))
            current = (payload.latitude, payload.longitude)
            distance = geodesic(current, (dest_lat, dest_lon)).miles
            if distance > 25:
                msg = f"🚨 Driver ID {user_id} отклонился от маршрута на {distance:.1f} миль."
                print(f"[ALERT] {msg}")
                await notify_all_channels_async(subject="Driver Deviation Alert", message=msg)
        except Exception as e:
            print("[WARN] Unable to check deviation:", e)

    return {"message": "Location updated"}

# 🗺️ Построение маршрута от текущей позиции
@router.post("/api/v1/telemetry/build-route")
async def build_route_from_current_location(
    destination: str,
    height: float,
    weight: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = current_user.id
    location_key = f"driver:{user_id}:location"

    # 1. Получаем текущие координаты из Redis
    location_data = await redis_client.hgetall(location_key)
    if not location_data:
        return {"error": "No location data found"}

    origin = f"{location_data['lon']},{location_data['lat']}"

    # 2. Сохраняем целевую точку в Redis
    await redis_client.set(f"driver:{user_id}:route_destination", destination)

    # 3. Получаем данные из Samsara
    from integrations.samsara_provider import get_samsara_vehicle_info_async
    samsara_data = await get_samsara_vehicle_info_async(user_id)
    fuel_level = samsara_data.get("fuel_level", 100)
    driver_time_left = samsara_data.get("driver_time_left", 11)  # в часах

    # 4. Получаем погодные условия
    from app.services.weather import get_weather_along_route_async
    origin_coords = tuple(map(float, origin.split(",")))
    dest_coords = tuple(map(float, destination.split(",")))
    weather_condition = await get_weather_along_route_async([origin_coords, dest_coords])

    # 5. Пользовательские предпочтения (можно получать из профиля или настроек)
    preferences = {
        "fuel_level": fuel_level,
        "driver_time_left": driver_time_left,
        "weather": weather_condition
    }

    # 6. Вызываем build_route с полной информацией
    route = await build_route(
        origin=origin,
        destination=destination,
        height=height,
        weight=weight,
        db=db,
        user_id=user_id,
        driver_time_left=driver_time_left,
        weather_condition=weather_condition,
        preferences=preferences
    )

    return route