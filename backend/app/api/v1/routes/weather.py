# Этот модуль возвращает погодные условия вдоль заданного маршрута
from fastapi import APIRouter
from typing import List, Tuple
from app.services.weather import get_weather_along_route_async

router = APIRouter()

@router.post("/api/v1/weather/")
async def weather_info(coords: List[Tuple[float, float]]):
    """
    Получение погодных условий вдоль маршрута
    """
    return await get_weather_along_route_async(coords)
