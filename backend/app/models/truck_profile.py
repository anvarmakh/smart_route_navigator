# Модель для хранения данных о траке индивидуального водителя
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class TruckProfile(Base):
    __tablename__ = "truck_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    make = Column(String)        # Марка: Freightliner, Volvo и т.д.
    model = Column(String)       # Модель: Cascadia, VNL и т.п.
    year = Column(Integer)
    fuel_capacity = Column(Float)  # Объем бака в галлонах или литрах
    mpg = Column(Float)            # Средний расход (miles per gallon или km/l)

    user = relationship("User", back_populates="truck")