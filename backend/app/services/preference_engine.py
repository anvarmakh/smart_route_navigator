def score_full_stop(
    fuel_price: float,
    brand: str,
    preferred_brands: list[str],
    fuel_level: float,
    fuel_capacity: float,
    weather_condition: str,
    driver_time_left: float,
    preferences: dict[str, str]  # HOS_time_left, fuel_price, weather_safety приоритеты
) -> int:
    """
    Общая оценка остановки по всем критериям: бренд, уровень топлива, цена, погода, HOS
    """
    score = 0

    # Бренд
    if brand in preferred_brands:
        score += 50
    else:
        score -= 20

    # Критический уровень топлива
    if fuel_level < 0.1 * fuel_capacity:
        score += 100

    # Цена топлива
    fuel_priority = preferences.get("fuel_price", "mid")
    if fuel_priority == "high":
        score -= fuel_price * 30
    elif fuel_priority == "mid":
        score -= fuel_price * 20
    elif fuel_priority == "low":
        score -= fuel_price * 10

    # Погода
    weather_priority = preferences.get("weather_safety", "mid")
    if weather_condition in ["Snow", "Storm"]:
        if weather_priority == "high":
            score -= 80
        elif weather_priority == "mid":
            score -= 40
        elif weather_priority == "low":
            score -= 10

    # Время по HOS
    hos_priority = preferences.get("HOS_time_left", "mid")
    if hos_priority == "high":
        if driver_time_left < 2:
            score -= 100
        elif driver_time_left < 4:
            score -= 50
    elif hos_priority == "mid":
        if driver_time_left < 2:
            score -= 40
    elif hos_priority == "low":
        if driver_time_left < 1:
            score -= 10

    return int(score)
