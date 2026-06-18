from typing import List, Dict, Set
import pandas as pd
from ...schemas.validation import ValidationError
from .email_validator import EmailValidator
from .phone_validator import PhoneValidator
from .date_validator import DateValidator

class TransactionValidator:
    
    REQUIRED_FIELDS = [
        'order_id', 'customer_id', 'customer_name', 'customer_email',
        'customer_phone', 'country', 'city', 'product_id', 'product_name',
        'quantity', 'unit_price', 'total_amount', 'payment_mode',
        'transaction_date', 'transaction_time'
    ]
    
    ALLOWED_PAYMENT_MODES = [
        'UPI', 'Credit Card', 'Debit Card', 'Net Banking', 'PayPal', 'Cash'
    ]
    
    def __init__(self, db):
        self.db = db
        self.phone_validator = PhoneValidator(db)
        self.errors: List[ValidationError] = []
        self.valid_rows: Set[int] = set()
        self.invalid_rows: Set[int] = set()
    
    def validate_dataframe(self, df: pd.DataFrame) -> tuple[pd.DataFrame, List[ValidationError]]:
        """Validate entire transaction dataframe"""
        self.errors = []
        self.valid_rows = set()
        self.invalid_rows = set()
        
        # Check required columns
        missing_cols = [col for col in self.REQUIRED_FIELDS if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")
        
        order_ids_seen = set()
        
        for idx, row in df.iterrows():
            row_number = idx + 2
            row_valid = True
            
            # 1. Check missing values
            for field in self.REQUIRED_FIELDS:
                if pd.isna(row[field]) or str(row[field]).strip() == "":
                    self.errors.append(ValidationError(
                        row_number=row_number,
                        column_name=field,
                        error_type="MISSING_VALUE",
                        error_description=f"{field} is missing",
                        suggested_fix=f"Provide {field}",
                        current_value=""
                    ))
                    row_valid = False
            
            # 2. Duplicate order_id
            order_id = str(row['order_id']).strip() if not pd.isna(row['order_id']) else ""
            if order_id:
                if order_id in order_ids_seen:
                    self.errors.append(ValidationError(
                        row_number=row_number,
                        column_name="order_id",
                        error_type="DUPLICATE",
                        error_description=f"Duplicate order_id: {order_id}",
                        suggested_fix="Use unique order_id",
                        current_value=order_id
                    ))
                    row_valid = False
                else:
                    order_ids_seen.add(order_id)
            
            # 3. Email validation
            email = str(row['customer_email']).strip() if not pd.isna(row['customer_email']) else ""
            if email:
                is_valid, error_msg = EmailValidator.is_valid_email(email)
                if not is_valid:
                    self.errors.append(ValidationError(
                        row_number=row_number,
                        column_name="customer_email",
                        error_type="INVALID_EMAIL",
                        error_description=error_msg,
                        suggested_fix="Use format: user@example.com",
                        current_value=email
                    ))
                    row_valid = False
            
            # 4. Phone validation with country-based rules
            phone = str(row['customer_phone']).strip() if not pd.isna(row['customer_phone']) else ""
            country = str(row['country']).strip().upper() if not pd.isna(row['country']) else "IN"
            
            if phone:
                is_valid, error_msg = self.phone_validator.validate_phone(phone, country)
                if not is_valid:
                    self.errors.append(ValidationError(
                        row_number=row_number,
                        column_name="customer_phone",
                        error_type="INVALID_PHONE",
                        error_description=f"{error_msg} for {country}",
                        suggested_fix=f"Provide valid phone for {country}",
                        current_value=phone
                    ))
                    row_valid = False
            
            # 5. Date validation
            trans_date = str(row['transaction_date']).strip() if not pd.isna(row['transaction_date']) else ""
            if trans_date:
                is_valid, error_msg, parsed_date = DateValidator.validate_date(trans_date, allow_future=False)
                if not is_valid:
                    self.errors.append(ValidationError(
                        row_number=row_number,
                        column_name="transaction_date",
                        error_type="INVALID_DATE",
                        error_description=error_msg,
                        suggested_fix="Use YYYY-MM-DD format",
                        current_value=trans_date
                    ))
                    row_valid = False
            
            # 6. Time validation
            trans_time = str(row['transaction_time']).strip() if not pd.isna(row['transaction_time']) else ""
            if trans_time:
                is_valid, error_msg, parsed_time = DateValidator.validate_time(trans_time)
                if not is_valid:
                    self.errors.append(ValidationError(
                        row_number=row_number,
                        column_name="transaction_time",
                        error_type="INVALID_TIME",
                        error_description=error_msg,
                        suggested_fix="Use HH:MM or HH:MM:SS format",
                        current_value=trans_time
                    ))
                    row_valid = False
            
            # 7. Payment mode validation
            payment_mode = str(row['payment_mode']).strip() if not pd.isna(row['payment_mode']) else ""
            if payment_mode and payment_mode not in self.ALLOWED_PAYMENT_MODES:
                self.errors.append(ValidationError(
                    row_number=row_number,
                    column_name="payment_mode",
                    error_type="INVALID_PAYMENT_MODE",
                    error_description=f"Unsupported payment mode: {payment_mode}",
                    suggested_fix=f"Use one of: {', '.join(self.ALLOWED_PAYMENT_MODES)}",
                    current_value=payment_mode
                ))
                row_valid = False
            
            # 8. Numeric validations
            try:
                quantity = int(row['quantity']) if not pd.isna(row['quantity']) else None
                if quantity is not None and quantity <= 0:
                    self.errors.append(ValidationError(
                        row_number=row_number,
                        column_name="quantity",
                        error_type="NEGATIVE_VALUE",
                        error_description="Quantity must be positive",
                        suggested_fix="Use positive integer",
                        current_value=str(quantity)
                    ))
                    row_valid = False
            except (ValueError, TypeError):
                self.errors.append(ValidationError(
                    row_number=row_number,
                    column_name="quantity",
                    error_type="INVALID_TYPE",
                    error_description="Quantity must be integer",
                    suggested_fix="Use integer value",
                    current_value=str(row['quantity'])
                ))
                row_valid = False
            
            try:
                unit_price = float(row['unit_price']) if not pd.isna(row['unit_price']) else None
                if unit_price is not None and unit_price < 0:
                    self.errors.append(ValidationError(
                        row_number=row_number,
                        column_name="unit_price",
                        error_type="NEGATIVE_PRICE",
                        error_description="Price cannot be negative",
                        suggested_fix="Use positive value",
                        current_value=str(unit_price)
                    ))
                    row_valid = False
            except (ValueError, TypeError):
                self.errors.append(ValidationError(
                    row_number=row_number,
                    column_name="unit_price",
                    error_type="INVALID_TYPE",
                    error_description="Unit price must be number",
                    suggested_fix="Use numeric value",
                    current_value=str(row['unit_price'])
                ))
                row_valid = False
            
            try:
                total_amount = float(row['total_amount']) if not pd.isna(row['total_amount']) else None
                if total_amount is not None and total_amount < 0:
                    self.errors.append(ValidationError(
                        row_number=row_number,
                        column_name="total_amount",
                        error_type="NEGATIVE_AMOUNT",
                        error_description="Total amount cannot be negative",
                        suggested_fix="Use positive value",
                        current_value=str(total_amount)
                    ))
                    row_valid = False
                
                # Validate total calculation
                if quantity and unit_price and total_amount:
                    expected_total = round(quantity * unit_price, 2)
                    if abs(total_amount - expected_total) > 0.01:
                        self.errors.append(ValidationError(
                            row_number=row_number,
                            column_name="total_amount",
                            error_type="INCORRECT_CALCULATION",
                            error_description=f"Total mismatch: {total_amount} != {quantity} × {unit_price}",
                            suggested_fix=f"Should be {expected_total}",
                            current_value=str(total_amount)
                        ))
                        row_valid = False
            except (ValueError, TypeError):
                self.errors.append(ValidationError(
                    row_number=row_number,
                    column_name="total_amount",
                    error_type="INVALID_TYPE",
                    error_description="Total amount must be number",
                    suggested_fix="Use numeric value",
                    current_value=str(row['total_amount'])
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