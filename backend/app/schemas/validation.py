from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class ValidationError(BaseModel):
    row_number: int
    column_name: str
    error_type: str
    error_description: str
    suggested_fix: Optional[str] = None
    current_value: Optional[str] = None

class ValidationReport(BaseModel):
    report_id: str
    file_name: str
    file_type: str
    total_records: int
    valid_records: int
    invalid_records: int
    success_rate: float
    errors: List[ValidationError]
    created_at: datetime
    
    class Config:
        from_attributes = True

class ValidationSummary(BaseModel):
    total_records: int
    valid_records: int
    invalid_records: int
    success_rate: float
    error_distribution: Dict[str, int]
    ai_insights: Optional[str] = None