from typing import List, Dict, Set
import pandas as pd
from ...schemas.validation import ValidationError
from .email_validator import EmailValidator
from .phone_validator import PhoneValidator
from .date_validator import DateValidator

class CustomerValidator:
    
    REQUIRED_FIELDS = ['customer_id', 'full_name', 'email', 'phone_number', 'city', 'signup_date']
    
    def __init__(self, db):
        self.db = db
        self.phone_validator = PhoneValidator(db)
        self.errors: List[ValidationError] = []
        self.valid_rows: Set[int] = set()
        self.invalid_rows: Set[int] = set()
    
    def validate_dataframe(self, df: pd.DataFrame) -> tuple[pd.DataFrame, List[ValidationError]]:
        """Validate entire customer dataframe"""
        self.errors = []
        self.valid_rows = set()
        self.invalid_rows = set()
        
        # Check required columns
        missing_cols = [col for col in self.REQUIRED_FIELDS if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")
        
        customer_ids_seen = set()
        emails_seen = set()
        
        for idx, row in df.iterrows():
            row_number = idx + 2  # +2 for header and 0-indexing
            row_valid = True
            
            # 1. Check missing values
            for field in self.REQUIRED_FIELDS:
                if pd.isna(row[field]) or str(row[field]).strip() == "":
                    self.errors.append(ValidationError(
                        row_number=row_number,
                        column_name=field,
                        error_type="MISSING_VALUE",
                        error_description=f"{field} is missing or empty",
                        suggested_fix=f"Provide a valid {field}",
                        current_value=""
                    ))
                    row_valid = False
            
            # 2. Validate customer_id duplicates
            customer_id = str(row['customer_id']).strip() if not pd.isna(row['customer_id']) else ""
            if customer_id:
                if customer_id in customer_ids_seen:
                    self.errors.append(ValidationError(
                        row_number=row_number,
                        column_name="customer_id",
                        error_type="DUPLICATE",
                        error_description=f"Duplicate customer_id: {customer_id}",
                        suggested_fix="Use unique customer_id",
                        current_value=customer_id
                    ))
                    row_valid = False
                else:
                    customer_ids_seen.add(customer_id)
            
            # 3. Validate email
            email = str(row['email']).strip() if not pd.isna(row['email']) else ""
            if email:
                is_valid, error_msg = EmailValidator.is_valid_email(email)
                if not is_valid:
                    self.errors.append(ValidationError(
                        row_number=row_number,
                        column_name="email",
                        error_type="INVALID_FORMAT",
                        error_description=error_msg,
                        suggested_fix="Use format: user@example.com",
                        current_value=email
                    ))
                    row_valid = False
                
                # Check duplicate emails
                if email in emails_seen:
                    self.errors.append(ValidationError(
                        row_number=row_number,
                        column_name="email",
                        error_type="DUPLICATE",
                        error_description=f"Duplicate email: {email}",
                        suggested_fix="Use unique email",
                        current_value=email
                    ))
                    row_valid = False
                else:
                    emails_seen.add(email)
            
            # 4. Validate phone number
            phone = str(row['phone_number']).strip() if not pd.isna(row['phone_number']) else ""
            if phone:
                is_valid, error_msg = self.phone_validator.validate_phone(phone, "IN")
                if not is_valid:
                    self.errors.append(ValidationError(
                        row_number=row_number,
                        column_name="phone_number",
                        error_type="INVALID_FORMAT",
                        error_description=error_msg,
                        suggested_fix="Use 10-digit Indian phone number",
                        current_value=phone
                    ))
                    row_valid = False
            
            # 5. Validate signup_date
            signup_date = str(row['signup_date']).strip() if not pd.isna(row['signup_date']) else ""
            if signup_date:
                is_valid, error_msg, parsed_date = DateValidator.validate_date(signup_date, allow_future=False)
                if not is_valid:
                    self.errors.append(ValidationError(
                        row_number=row_number,
                        column_name="signup_date",
                        error_type="INVALID_DATE",
                        error_description=error_msg,
                        suggested_fix="Use format: YYYY-MM-DD",
                        current_value=signup_date
                    ))
                    row_valid = False
            
            # 6. Validate city
            city = str(row['city']).strip() if not pd.isna(row['city']) else ""
            if city and len(city) < 2:
                self.errors.append(ValidationError(
                    row_number=row_number,
                    column_name="city",
                    error_type="INVALID_VALUE",
                    error_description="City name too short",
                    suggested_fix="Provide valid city name",
                    current_value=city
                ))
                row_valid = False
            
            # 7. Check invalid characters in name
            full_name = str(row['full_name']).strip() if not pd.isna(row['full_name']) else ""
            if full_name and not all(c.isalpha() or c.isspace() or c in ".-'" for c in full_name):
                self.errors.append(ValidationError(
                    row_number=row_number,
                    column_name="full_name",
                    error_type="INVALID_CHARACTERS",
                    error_description="Name contains invalid characters",
                    suggested_fix="Use only letters, spaces, hyphens, and apostrophes",
                    current_value=full_name
                ))
                row_valid = False
            
            if row_valid:
                self.valid_rows.add(row_number)
            else:
                self.invalid_rows.add(row_number)
        
        return df, self.errors
    
    def get_validation_summary(self, total_records: int) -> Dict:
        """Get validation summary"""
        valid_count = len(self.valid_rows)
        invalid_count = len(self.invalid_rows)
        
        error_distribution = {}
        for error in self.errors:
            error_distribution[error.error_type] = error_distribution.get(error.error_type, 0) + 1
        
        return {
            "total_records": total_records,
            "valid_records": valid_count,
            "invalid_records": invalid_count,
            "success_rate": round((valid_count / total_records * 100) if total_records > 0 else 0, 2),
            "error_distribution": error_distribution
        }