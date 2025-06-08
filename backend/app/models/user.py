# Модель пользователя с ролями и подпиской
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.truck_profile import TruckProfile
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String, default="driver")
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"))
    company_id = Column(Integer, ForeignKey("companies.id"))
    truck = relationship("TruckProfile", back_populates="user", uselist=False)
    routes = relationship("RouteHistory", back_populates="user", cascade="all, delete")
    subscription = relationship("Subscription", back_populates="users", uselist=False)
    company = relationship("Company", back_populates="drivers")