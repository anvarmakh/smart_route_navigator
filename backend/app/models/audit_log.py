# Лог действий пользователей
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    action = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)