# Заглушка для погоды через OpenWeather
from app.core.interfaces.weather_provider import WeatherProvider

class OpenWeatherProvider(WeatherProvider):
    def get_weather(self, lat, lon):
        return {"temp": 15, "condition": "Cloudy"}

