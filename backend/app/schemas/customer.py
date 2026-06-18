from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime

class CustomerBase(BaseModel):
    customer_id: str
    full_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    city: Optional[str] = None
    signup_date: Optional[date] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerEnriched(CustomerBase):
    first_name: Optional[str] = None
    email_domain: Optional[str] = None
    is_gmail: bool = False
    signup_month: Optional[str] = None
    signup_day: Optional[str] = None

class Customer(CustomerEnriched):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class VIPCustomer(BaseModel):
    customer_id: str
    full_name: str
    email: str
    phone_number: Optional[str]
    city: str
    signup_date: date
    created_at: datetime
    
    class Config:
        from_attributes = True