# Этот модуль обрабатывает POST-запросы для построения маршрутов с учётом ограничений
# ✅ routing.py — async endpoint для построения маршрута
from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.route_service import build_route
from app.services.auth_service import get_current_user

router = APIRouter()

@router.post("/api/v1/route-info")
async def route_info(
    origin: str = Query(..., description="Начальная точка"),
    destination: str = Query(..., description="Конечная точка"),
    height: float = Query(..., description="Высота трака в метрах"),
    weight: int = Query(..., description="Вес трака в кг"),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Построение маршрута с учётом ограничений по высоте и весу.
    """
    return await build_route(origin, destination, height, weight, db, current_user.id)
