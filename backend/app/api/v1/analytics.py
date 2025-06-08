# ✅ route_analytics.py — асинхронная версия оригинального анализа маршрутов
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.route_history import RouteHistory
from app.models.fuel_entry import FuelEntry
from app.database import get_db, engine, Base
from app.services.auth_service import get_current_user
import statistics
from collections import Counter

# 🔧 Создаём все таблицы (только для девелопа)
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# 📌 Вызов инициализации при импорте (например, из main.py)
import asyncio
asyncio.get_event_loop().run_until_complete(init_models())


router = APIRouter()


@router.get("/api/v1/analytics/")
async def route_analytics(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    result = await db.execute(
        select(RouteHistory).where(RouteHistory.user_id == current_user.id)
    )
    history = result.scalars().all()

    if not history:
        return {"message": "Нет данных"}

    fuel_prices = []
    weather_tags = []
    route_pairs = []

    for h in history:
        if h.fuel_data:
            fuel_prices.extend(h.fuel_data)
        if h.weather_data:
            weather_tags.extend(h.weather_data)
        route_pairs.append((h.origin, h.destination))

    return {
        "avg_fuel_price": round(statistics.mean(fuel_prices), 2) if fuel_prices else 0,
        "popular_routes": Counter(route_pairs).most_common(3),
        "bad_weather_count": weather_tags.count("bad")
    }

# 📊 GET /api/v1/analytics/fuel-usage — пример эндпоинта анализа расхода топлива
@router.get("/api/v1/analytics/fuel-usage")
async def fuel_usage(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    result = await db.execute(
        select(FuelEntry).where(FuelEntry.user_id == current_user.id)
    )
    entries = result.scalars().all()

    total_gallons = sum(e.gallons for e in entries)
    total_miles = sum(e.miles for e in entries)
    avg_mpg = total_miles / total_gallons if total_gallons > 0 else 0

    return {
        "total_gallons": total_gallons,
        "total_miles": total_miles,
        "average_mpg": round(avg_mpg, 2)
    }
