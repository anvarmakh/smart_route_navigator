# Middleware-функция или ручная проверка на доступ по подписке
from fastapi import Request, HTTPException

ACTIVE_PLANS = {
    "basic": ["route"],
    "premium": ["route", "fuel", "weather"]
}

async def check_subscription(request: Request, required_feature: str):
    """
    Проверка: доступен ли запрашиваемый функционал пользователю
    """
    user = request.state.user
    plan = user.get("subscription", "basic")
    if required_feature not in ACTIVE_PLANS.get(plan, []):
        raise HTTPException(status_code=403, detail="Upgrade your plan to use this feature")