from pydantic import BaseModel
from typing import Optional
from datetime import date, time, datetime

class TransactionBase(BaseModel):
    order_id: str
    customer_id: Optional[str] = None
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    product_id: Optional[str] = None
    product_name: Optional[str] = None
    quantity: Optional[int] = None
    unit_price: Optional[float] = None
    total_amount: Optional[float] = None
    payment_mode: Optional[str] = None
    transaction_date: Optional[date] = None
    transaction_time: Optional[time] = None

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    transaction_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True