# Получение погодных условий вдоль маршрута через провайдер
from app.providers.openweather_provider import get_weather_data

def get_weather_along_route(coordinates: list[tuple[float, float]]):
    """
    Возвращает список погодных условий по точкам вдоль маршрута.
    - координаты — список точек (lat, lon)
    - использует провайдер OpenWeather
    """
    forecasts = [get_weather_data(lat, lon) for lat, lon in coordinates]
    return forecasts