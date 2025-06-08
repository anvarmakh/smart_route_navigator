# ✅ subscription.py — асинхронная версия проверки доступа по подписке
from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.subscription_service import check_user_plan_async
from app.services.auth_service import get_current_user

from pydantic import BaseModel
from sqlalchemy.future import select
from app.models.subscription import Subscription


router = APIRouter()

@router.get("/api/v1/subscription/check-access")
async def check_access(
    feature: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Проверка доступа пользователя к функционалу согласно его подписке
    """
    has_access = await check_user_plan_async(db, current_user, feature)
    if not has_access:
        raise HTTPException(status_code=403, detail="Недостаточный уровень подписки")
    return {"access": True}


# Добавление или обновление подписки 

class SubscriptionUpdate(BaseModel):
    active: bool
    features: str  # пример: "routing,fuel,analytics"

@router.post("/api/v1/subscription")
async def update_subscription(
    data: SubscriptionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    result = await db.execute(
        select(Subscription).where(Subscription.user_id == current_user.id)
    )
    subscription = result.scalars().first()

    if subscription:
        subscription.active = data.active
        subscription.features = data.features
    else:
        subscription = Subscription(
            user_id=current_user.id,
            active=data.active,
            features=data.features
        )
        db.add(subscription)

    await db.commit()
    return {"message": "Подписка обновлена"}


@router.get("/api/v1/subscription")
async def get_subscription(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    result = await db.execute(
        select(Subscription).where(Subscription.user_id == current_user.id)
    )
    subscription = result.scalars().first()

    if not subscription:
        raise HTTPException(status_code=404, detail="Подписка не найдена")

    return {
        "active": subscription.active,
        "features": subscription.features.split(",") if subscription.features else []
    }