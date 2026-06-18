from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from ..core.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    log_id = Column(String, unique=True, index=True)
    action = Column(String, nullable=False)
    user_id = Column(Integer)
    details = Column(JSON)
    ip_address = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())