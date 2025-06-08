# ✅ history.py — асинхронная история маршрутов
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.route_history import RouteHistory
from app.database import get_db
from app.services.auth_service import get_current_user

router = APIRouter()

@router.get("/api/v1/history/")
async def get_route_history(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Возвращает историю маршрутов пользователя
    """
    result = await db.execute(
        select(RouteHistory)
        .where(RouteHistory.user_id == current_user.id)
        .order_by(RouteHistory.created_at.desc())
    )
    history = result.scalars().all()

    return [
        {
            "origin": h.origin,
            "destination": h.destination,
            "distance": h.distance,
            "estimated_time": h.estimated_time,
            "fuel_data": h.fuel_data,
            "weather_data": h.weather_data,
            "created_at": h.created_at.isoformat()
        } for h in history
    ]
