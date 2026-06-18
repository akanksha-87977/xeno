from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import pandas as pd
import uuid
from datetime import datetime

from ....core.database import get_db
from ....models.user import User
from ....models.customer import Customer
from ....models.validation import ValidationReport, UploadedFile
from ....schemas.customer import Customer as CustomerSchema
from ....schemas.validation import ValidationReport as ValidationReportSchema, ValidationSummary
from ....services.validation.customer_validator import CustomerValidator
from ....services.data_cleaning import DataCleaningService
from ....services.enrichment import CustomerEnrichmentService
from ....services.file_processor import FileProcessorService
from ....services.ai_insights import AIInsightsService
from ....api.deps import get_current_active_user

router = APIRouter()

@router.post("/validate")
def validate_customers(
    file_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Validate customer data file"""
    
    # Get uploaded file
    uploaded_file = db.query(UploadedFile).filter(
        UploadedFile.file_id == file_id
    ).first()
    
    if not uploaded_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # Read file
    try:
        df = FileProcessorService.read_file(uploaded_file.file_path)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to read file: {str(e)}"
        )
    
    # Validate
    validator = CustomerValidator(db)
    try:
        validated_df, errors = validator.validate_dataframe(df)
        summary = validator.get_validation_summary(len(df))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Validation failed: {str(e)}"
        )
    
    # Generate AI insights
    error_distribution = summary.get('error_distribution', {})
    ai_insights = AIInsightsService.generate_insights(
        total_records=summary['total_records'],
        valid_records=summary['valid_records'],
        invalid_records=summary['invalid_records'],
        errors=errors,
        error_distribution=error_distribution
    )
    
    # Save validation report
    report_id = str(uuid.uuid4())
    report = ValidationReport(
        report_id=report_id,
        file_name=uploaded_file.file_name,
        file_type="customer",
        total_records=summary['total_records'],
        valid_records=summary['valid_records'],
        invalid_records=summary['invalid_records'],
        success_rate=summary['success_rate'],
        errors=[error.dict() for error in errors]
    )
    
    db.add(report)
    db.commit()
    db.refresh(report)
    
    return {
        "report_id": report_id,
        "summary": summary,
        "errors": errors[:100],  # Return first 100 errors
        "total_errors": len(errors),
        "ai_insights": ai_insights
    }

@router.post("/clean")
def clean_customers(
    file_id: str,
    remove_invalid: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Clean customer data"""
    
    # Get uploaded file
    uploaded_file = db.query(UploadedFile).filter(
        UploadedFile.file_id == file_id
    ).first()
    
    if not uploaded_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # Read file
    df = FileProcessorService.read_file(uploaded_file.file_path)
    
    # Clean data
    cleaned_df, changes = DataCleaningService.clean_customer_data(df)
    
    # Enrich data
    enriched_df = CustomerEnrichmentService.enrich_customer_data(cleaned_df)
    
    # Save cleaned file
    cleaned_file_path = FileProcessorService.save_file(
        enriched_df,
        f"cleaned_{uploaded_file.file_name}",
        format='csv'
    )
    
    return {
        "cleaned_file_path": cleaned_file_path,
        "original_rows": len(df),
        "cleaned_rows": len(enriched_df),
        "changes": changes,
        "message": "Data cleaned and enriched successfully"
    }

@router.post("/import")
def import_customers(
    file_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Import cleaned customer data to database"""
    
    # Get uploaded file
    uploaded_file = db.query(UploadedFile).filter(
        UploadedFile.file_id == file_id
    ).first()
    
    if not uploaded_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # Read file
    df = FileProcessorService.read_file(uploaded_file.file_path)
    
    # Clean and enrich
    cleaned_df, _ = DataCleaningService.clean_customer_data(df)
    enriched_df = CustomerEnrichmentService.enrich_customer_data(cleaned_df)
    
    # Import to database
    imported_count = 0
    for _, row in enriched_df.iterrows():
        try:
            customer = Customer(
                customer_id=row['customer_id'],
                full_name=row['full_name'],
                first_name=row.get('first_name', ''),
                email=row['email'],
                email_domain=row.get('email_domain', ''),
                is_gmail=row.get('is_gmail', False),
                phone_number=row.get('phone_number', ''),
                city=row.get('city', ''),
                signup_date=pd.to_datetime(row['signup_date']).date() if pd.notna(row.get('signup_date')) else None,
                signup_month=row.get('signup_month', ''),
                signup_day=row.get('signup_day', '')
            )
            
            db.add(customer)
            imported_count += 1
        except Exception as e:
            print(f"Error importing row: {str(e)}")
            continue
    
    db.commit()
    
    return {
        "imported_count": imported_count,
        "message": f"Successfully imported {imported_count} customers"
    }

@router.get("/", response_model=List[CustomerSchema])
def get_customers(
    skip: int = 0,
    limit: int = 100,
    city: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get customers with optional filters"""
    
    query = db.query(Customer)
    
    if city:
        query = query.filter(Customer.city == city)
    
    customers = query.offset(skip).limit(limit).all()
    return customers

@router.get("/{customer_id}", response_model=CustomerSchema)
def get_customer(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get customer by ID"""
    
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    return customer