# Модель подписки, включающая план и статус
# ✅ models/subscription.py — модель подписки пользователя
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    active = Column(Boolean, default=True)
    features = Column(String, default="")  # например: "routing,fuel,analytics"

    user = relationship("User", back_populates="subscription")


