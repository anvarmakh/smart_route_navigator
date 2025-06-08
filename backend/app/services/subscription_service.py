# Проверка наличия доступа к функциональности на основе подписки

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.subscription import Subscription


ACTIVE_PLANS = {
    "basic": ["route"],
    "premium": ["route", "fuel", "weather"]
}


# 📌 Проверка, есть ли у пользователя активная подписка, покрывающая нужную фичу
async def check_user_plan_async(db: AsyncSession, user, feature: str) -> bool:
    result = await db.execute(
        select(Subscription).where(Subscription.user_id == user.id)
    )
    subscription = result.scalars().first()
    
    if not subscription or not subscription.active:
        return False

    # Допустим, подписка хранит список разрешённых фич в виде строки: "routing,fuel,analytics"
    if feature not in (subscription.features or "").split(","):
        return False

    return True