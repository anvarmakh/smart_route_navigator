import os
import requests

SAMSARA_API_TOKEN = os.getenv("SAMSARA_API_TOKEN", "")
SAMSARA_BASE_URL = "https://api.samsara.com"

# 🔌 Получение телеметрии по user_id (заглушка, заменить при проде)
def get_samsara_vehicle_info(user_id: int) -> dict:
    """
    Возвращает телеметрию по пользователю из Samsara API.

    ⚠️ Пока это заглушка. Для реальной интеграции:
    - Привязать user_id к vehicle_id
    - Авторизоваться через OAuth2 и получить access_token
    - Вызвать GET /fleet/vehicles/{id}/locations
    - Вызвать GET /fleet/vehicles/{id}/statistics
    - Вызвать GET /fleet/drivers/{id}/hos
    """
    return {
        "fuel_level": 160.5,         # уровень топлива
        "driver_time_left": 3.2,     # оставшееся время по HOS
        "weather": "Clear"           # текущая погода (в будущем — из внешнего API)
    }