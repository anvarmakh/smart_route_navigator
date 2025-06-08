# ✅ async_database.py — подключение к PostgreSQL через async SQLAlchemy
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# 📊 Загрузка .env
load_dotenv()

# 📂 URL подключения к PostgreSQL (asyncpg)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:password@localhost:5432/smart_route")

# 🚀 Создаём асинхронный движок
engine = create_async_engine(DATABASE_URL, echo=True)

# 🔧 Сессии ORM
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 🔄 Base для моделей
Base = declarative_base()

# 🧲 Утилита для получения session в endpoint
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
