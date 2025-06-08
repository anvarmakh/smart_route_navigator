# Реализация маршрутизатора на базе OSRM

import requests
from app.core.interfaces.routing_provider import RoutingProvider

class OSRMRoutingProvider(RoutingProvider):
    def __init__(self, osrm_url="http://localhost:5000"):
        self.osrm_url = osrm_url

    def geocode(self, location):
        # Используем Nominatim для преобразования адреса в координаты
        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": location, "format": "json", "limit": 1}
        response = requests.get(url, params=params, headers={"User-Agent": "SmartRouteBot"})
        response.raise_for_status()
        data = response.json()
        if not data:
            raise ValueError(f"Не удалось найти координаты для {location}")
        return float(data[0]["lon"]), float(data[0]["lat"])

    def get_route(self, origin, destination, height, weight):
        lon1, lat1 = self.geocode(origin)
        lon2, lat2 = self.geocode(destination)

        url = f"{self.osrm_url}/route/v1/driving/{lon1},{lat1};{lon2},{lat2}"
        params = {
            "overview": "full",
            "geometries": "geojson"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if not data.get("routes"):
            raise ValueError("Маршрут не найден")

        route = data["routes"][0]
        return {
            "route": route["geometry"]["coordinates"],
            "distance_miles": route["distance"] / 1609.34,
            "eta_hours": route["duration"] / 3600
        }
