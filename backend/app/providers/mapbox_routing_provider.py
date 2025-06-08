# ✅ mapbox_routing_provider.py — async Mapbox API client
# ✅ mapbox_routing_provider.py — async версия с поддержкой параметров
import httpx
import os

class MapboxRoutingProvider:

    @staticmethod
    async def get_route_async(
        origin: str,
        destination: str,
        height: float,
        weight: int,
        preferences: dict = None,
        driver_time_left: float = None,
        weather_condition: list = None
    ):
        """
        Получает маршрут от Mapbox и дополняет данными из preferences, погоды и HOS.
        """
        api_key = os.getenv("MAPBOX_API_KEY")
        base_url = "https://api.mapbox.com/directions/v5/mapbox/driving"
        url = f"{base_url}/{origin};{destination}"

        params = {
            "access_token": api_key,
            "geometries": "geojson",
            "overview": "full",
            "annotations": "duration,distance",
            # дополнительные параметры в query не вставляем, но можно обработать логикой ниже
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            route_data = response.json()

        # 🔧 Пример базового анализа/обогащения
        enriched_route = {
            "route": route_data,
            "fuel": [],
            "weather": weather_condition or [],
            "driver_constraints": {
                "time_left": driver_time_left
            },
            "preferences_used": preferences or {}
        }

        return enriched_route
