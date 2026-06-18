from sqlalchemy import Column, Integer, String, DateTime, Boolean, Date, Index
from sqlalchemy.sql import func
from ..core.database import Base

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    first_name = Column(String)
    email = Column(String, index=True, nullable=False)
    email_domain = Column(String)
    is_gmail = Column(Boolean, default=False)
    phone_number = Column(String)
    city = Column(String, index=True)
    signup_date = Column(Date, index=True)
    signup_month = Column(String)
    signup_day = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        Index('idx_customer_email', 'email'),
        Index('idx_customer_city', 'city'),
        Index('idx_customer_signup_date', 'signup_date'),
    )

class VIPCustomer(Base):
    __tablename__ = "vip_customers"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String, index=True, nullable=False)
    full_name = Column(String)
    email = Column(String)
    phone_number = Column(String)
    city = Column(String)
    signup_date = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())