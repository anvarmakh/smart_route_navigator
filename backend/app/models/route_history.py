from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base, engine

class RouteHistory(Base):
    __tablename__ = "route_history"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    origin = Column(String, nullable=False)          # адрес отправления
    destination = Column(String, nullable=False)     # адрес назначения

    distance = Column(Float)                         # расстояние в милях
    estimated_time = Column(Float)                   # ETA (в часах)

    fuel_data = Column(JSON, nullable=True)          # JSON с данными о заправках
    weather_data = Column(JSON, nullable=True)       # JSON с погодными данными

    created_at = Column(DateTime, default=datetime.utcnow)

    # 🔗 связь с пользователем
    user = relationship("User", back_populates="routes")


# ⛏️ Автоматическое создание таблицы (только при прямом запуске файла)
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("✅ route_history table created.")