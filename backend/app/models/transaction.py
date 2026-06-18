from sqlalchemy import Column, Integer, String, DateTime, Float, Date, Time, ForeignKey, Index
from sqlalchemy.sql import func
from ..core.database import Base

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, unique=True, index=True, nullable=False)
    customer_id = Column(String, ForeignKey('customers.customer_id'))
    amount = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        Index('idx_order_customer', 'customer_id'),
    )

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True, nullable=False)
    order_id = Column(String, ForeignKey('orders.order_id'))
    customer_id = Column(String)
    customer_name = Column(String)
    customer_email = Column(String)
    customer_phone = Column(String)
    country = Column(String)
    city = Column(String)
    product_id = Column(String)
    product_name = Column(String)
    quantity = Column(Integer)
    unit_price = Column(Float)
    total_amount = Column(Float)
    payment_mode = Column(String)
    transaction_date = Column(Date)
    transaction_time = Column(Time)
    created_at = Column(DateTime(timezone=True), server_default=func.now())