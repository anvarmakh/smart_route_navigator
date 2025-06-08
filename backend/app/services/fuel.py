from app.services.preference_engine import score_full_stop

def rank_fuel_stops_by_brand(
    stops: list[dict],
    preferred_brands: list[str],
    fuel_level: float,
    fuel_capacity: float,
    preferences: dict[str, str]
) -> list[dict]:
    """
    Полный скоринг остановок с учётом бренда, уровня топлива, погоды, цены и HOS
    """
    for stop in stops:
        stop["score"] = score_full_stop(
            fuel_price=stop.get("price", 0),
            brand=stop.get("brand", ""),
            preferred_brands=preferred_brands,
            fuel_level=fuel_level,
            fuel_capacity=fuel_capacity,
            weather_condition=stop.get("weather", "Clear"),
            driver_time_left=stop.get("driver_time_left", 4),
            preferences=preferences
        )
    return sorted(stops, key=lambda s: s["score"], reverse=True)

