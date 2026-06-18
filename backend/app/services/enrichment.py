import pandas as pd
from datetime import datetime
from .validation.email_validator import EmailValidator

class CustomerEnrichmentService:
    
    @staticmethod
    def enrich_customer_data(df: pd.DataFrame) -> pd.DataFrame:
        """Enrich customer data with derived fields"""
        
        # 1. Extract first_name from full_name
        if 'full_name' in df.columns:
            df['first_name'] = df['full_name'].apply(
                lambda x: str(x).split()[0] if pd.notna(x) and str(x).strip() else ""
            )
        
        # 2. Extract email_domain
        if 'email' in df.columns:
            df['email_domain'] = df['email'].apply(
                lambda x: EmailValidator.get_domain(str(x)) if pd.notna(x) else ""
            )
        
        # 3. Check is_gmail
        if 'email' in df.columns:
            df['is_gmail'] = df['email'].apply(
                lambda x: EmailValidator.is_gmail(str(x)) if pd.notna(x) else False
            )
        
        # 4. Extract signup_month and signup_day
        if 'signup_date' in df.columns:
            df['signup_date_parsed'] = pd.to_datetime(df['signup_date'], errors='coerce')
            df['signup_month'] = df['signup_date_parsed'].dt.strftime('%B')
            df['signup_day'] = df['signup_date_parsed'].dt.strftime('%A')
            df = df.drop('signup_date_parsed', axis=1)
        
        return df