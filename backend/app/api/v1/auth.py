# ✅ auth.py — асинхронная авторизация с FastAPI + Async SQLAlchemy
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.future import select
from app.database import get_db
from app.services.auth_service import (
    get_current_user,
    verify_password,
    get_password_hash,
    create_access_token,
)
from app.models.user import UserCreate, User
from app.models.truck_profile import TruckProfile

router = APIRouter()

# 🔐 Логин: получение токена
@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.email == form_data.username)
    )
    user = result.scalars().first()


    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# 🆕 POST /register: регистрация нового пользователя и создание TruckProfile
@router.post("/register")
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalars().first()

    if existing_user:    
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = get_password_hash(user_data.password)
    new_user = User(email=user_data.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    hashed_password = get_password_hash(user_data.password)
    new_user = User(email=user_data.email, password=hashed_password)
    db.add(new_user)
    await db.flush()  # получаем ID пользователя

    # Создаём профиль трака по умолчанию
    truck_profile = TruckProfile(user_id=new_user.id)
    db.add(truck_profile)

    await db.commit()
    return {"message": "User created successfully"}

# 🚛 GET /api/v1/profile/truck — возвращает профиль трака для авторизованного юзера
@router.get("/api/v1/profile/truck")
async def get_truck_profile(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(TruckProfile).where(TruckProfile.user_id == current_user.id)
    )
    truck = result.scalars().first()

    if not truck:
        raise HTTPException(status_code=404, detail="Truck profile not found")

    return {
        "make": truck.make,
        "model": truck.model,
        "year": truck.year,
        "fuel_capacity": truck.fuel_capacity,
        "mpg": truck.mpg
    }