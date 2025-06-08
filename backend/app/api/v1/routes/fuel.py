# ✅ fuel.py — асинхронный анализ заправок
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.fuel import rank_fuel_stops_by_brand
from app.services.auth_service import get_current_user

router = APIRouter()

@router.post("/api/v1/fuel/recommendations")
async def recommend_stops(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Возвращает отсортированные заправки на основе всех факторов
    """
    body = await request.json()

    stops = body.get("stops", [])
    preferred_brands = body.get("preferred_brands", [])
    fuel_level = body.get("fuel_level", 100)
    fuel_capacity = body.get("fuel_capacity", 300)
    preferences = body.get("preferences", {
        "fuel_price": 1.0,
        "weather": 1.0,
        "distance": 1.0
    })

    ranked = rank_fuel_stops_by_brand(
        stops, preferred_brands, fuel_level, fuel_capacity, preferences
    )
    return {"recommendations": ranked}
