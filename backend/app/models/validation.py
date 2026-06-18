from sqlalchemy import Column, Integer, String, DateTime, Float, JSON
from sqlalchemy.sql import func
from ..core.database import Base

class ValidationReport(Base):
    __tablename__ = "validation_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(String, unique=True, index=True)
    file_name = Column(String)
    file_type = Column(String)  # customer, transaction
    total_records = Column(Integer)
    valid_records = Column(Integer)
    invalid_records = Column(Integer)
    success_rate = Column(Float)
    errors = Column(JSON)  # Store error details
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UploadedFile(Base):
    __tablename__ = "uploaded_files"
    
    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(String, unique=True, index=True)
    file_name = Column(String)
    file_type = Column(String)
    file_path = Column(String)
    row_count = Column(Integer)
    uploaded_by = Column(Integer)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

class PhoneValidationRule(Base):
    __tablename__ = "phone_validation_rules"
    
    id = Column(Integer, primary_key=True, index=True)
    country_code = Column(String, unique=True, nullable=False)
    country_name = Column(String)
    min_digits = Column(Integer)
    max_digits = Column(Integer)
    pattern = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())