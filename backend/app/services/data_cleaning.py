import pandas as pd
import re
from typing import Dict
from .validation.phone_validator import PhoneValidator
from .validation.date_validator import DateValidator

class DataCleaningService:
    
    @staticmethod
    def clean_customer_data(df: pd.DataFrame) -> tuple[pd.DataFrame, Dict]:
        """Clean customer dataframe"""
        original_count = len(df)
        changes = {
            "trimmed_whitespace": 0,
            "standardized_phones": 0,
            "standardized_dates": 0,
            "removed_duplicates": 0,
            "normalized_names": 0
        }
        
        # 1. Trim whitespace from all string columns
        for col in df.select_dtypes(include=['object']).columns:
            before = df[col].astype(str)
            df[col] = df[col].astype(str).str.strip()
            after = df[col]
            changes["trimmed_whitespace"] += (before != after).sum()
        
        # 2. Normalize capitalization for names
        if 'full_name' in df.columns:
            before = df['full_name'].copy()
            df['full_name'] = df['full_name'].str.title()
            changes["normalized_names"] = (before != df['full_name']).sum()
        
        if 'city' in df.columns:
            df['city'] = df['city'].str.title()
        
        # 3. Standardize phone numbers
        if 'phone_number' in df.columns:
            before = df['phone_number'].copy()
            df['phone_number'] = df['phone_number'].apply(
                lambda x: PhoneValidator.clean_phone(str(x)) if pd.notna(x) else x
            )
            changes["standardized_phones"] = (before != df['phone_number']).sum()
        
        # 4. Standardize dates
        if 'signup_date' in df.columns:
            before = df['signup_date'].copy()
            df['signup_date'] = df['signup_date'].apply(
                lambda x: DateValidator.standardize_date(DateValidator.parse_date(str(x)))
                if pd.notna(x) and DateValidator.parse_date(str(x)) else x
            )
            changes["standardized_dates"] = (before != df['signup_date']).sum()
        
        # 5. Remove duplicates based on customer_id
        if 'customer_id' in df.columns:
            before_count = len(df)
            df = df.drop_duplicates(subset=['customer_id'], keep='first')
            changes["removed_duplicates"] = before_count - len(df)
        
        # 6. Remove rows with all NaN
        df = df.dropna(how='all')
        
        return df, changes
    
    @staticmethod
    def clean_transaction_data(df: pd.DataFrame) -> tuple[pd.DataFrame, Dict]:
        """Clean transaction dataframe"""
        changes = {
            "trimmed_whitespace": 0,
            "standardized_phones": 0,
            "standardized_dates": 0,
            "standardized_times": 0,
            "removed_duplicates": 0,
            "normalized_payment_modes": 0,
            "fixed_calculations": 0
        }
        
        # 1. Trim whitespace
        for col in df.select_dtypes(include=['object']).columns:
            before = df[col].astype(str)
            df[col] = df[col].astype(str).str.strip()
            changes["trimmed_whitespace"] += (before != after).sum()
        
        # 2. Standardize phone numbers
        if 'customer_phone' in df.columns:
            before = df['customer_phone'].copy()
            df['customer_phone'] = df['customer_phone'].apply(
                lambda x: PhoneValidator.clean_phone(str(x)) if pd.notna(x) else x
            )
            changes["standardized_phones"] = (before != df['customer_phone']).sum()
        
        # 3. Standardize dates
        if 'transaction_date' in df.columns:
            before = df['transaction_date'].copy()
            df['transaction_date'] = df['transaction_date'].apply(
                lambda x: DateValidator.standardize_date(DateValidator.parse_date(str(x)))
                if pd.notna(x) and DateValidator.parse_date(str(x)) else x
            )
            changes["standardized_dates"] = (before != df['transaction_date']).sum()
        
        # 4. Standardize times
        if 'transaction_time' in df.columns:
            before = df['transaction_time'].copy()
            df['transaction_time'] = df['transaction_time'].apply(
                lambda x: DateValidator.parse_time(str(x)).strftime("%H:%M:%S")
                if pd.notna(x) and DateValidator.parse_time(str(x)) else x
            )
            changes["standardized_times"] = (before != df['transaction_time']).sum()
        
        # 5. Normalize payment modes
        if 'payment_mode' in df.columns:
            before = df['payment_mode'].copy()
            df['payment_mode'] = df['payment_mode'].str.title()
            changes["normalized_payment_modes"] = (before != df['payment_mode']).sum()
        
        # 6. Fix total_amount calculations
        if all(col in df.columns for col in ['quantity', 'unit_price', 'total_amount']):
            before = df['total_amount'].copy()
            df['total_amount'] = df['quantity'] * df['unit_price']
            changes["fixed_calculations"] = (before != df['total_amount']).sum()
        
        # 7. Remove duplicate order_ids
        if 'order_id' in df.columns:
            before_count = len(df)
            df = df.drop_duplicates(subset=['order_id'], keep='first')
            changes["removed_duplicates"] = before_count - len(df)
        
        return df, changes
    
    @staticmethod
    def remove_invalid_records(df: pd.DataFrame, invalid_rows: set) -> pd.DataFrame:
        """Remove invalid rows from dataframe"""
        # Convert row numbers to indices (subtract 2 for header and 0-indexing)
        invalid_indices = [row - 2 for row in invalid_rows if row >= 2]
        return df.drop(invalid_indices, errors='ignore')