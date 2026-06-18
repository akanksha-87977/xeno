import re
import phonenumbers
from typing import Optional, Dict
from sqlalchemy.orm import Session
from ...models.validation import PhoneValidationRule

class PhoneValidator:
    
    def __init__(self, db: Session):
        self.db = db
        self.rules = self._load_rules()
    
    def _load_rules(self) -> Dict[str, PhoneValidationRule]:
        """Load phone validation rules from database"""
        rules = self.db.query(PhoneValidationRule).all()
        return {rule.country_code: rule for rule in rules}
    
    @staticmethod
    def clean_phone(phone: str) -> str:
        """Remove all non-digit characters"""
        if not phone:
            return ""
        return re.sub(r'\D', '', str(phone))
    
    def validate_phone(self, phone: str, country_code: str = "IN") -> tuple[bool, str]:
        """Validate phone number based on country rules"""
        if not phone or phone.strip() == "":
            return False, "Phone number is empty"
        
        cleaned = self.clean_phone(phone)
        
        if not cleaned:
            return False, "Phone number contains no digits"
        
        # Get country rule
        rule = self.rules.get(country_code)
        
        if not rule:
            return False, f"No validation rule for country {country_code}"
        
        # Check length
        phone_length = len(cleaned)
        
        if phone_length < rule.min_digits:
            return False, f"Phone number too short (min {rule.min_digits} digits)"
        
        if phone_length > rule.max_digits:
            return False, f"Phone number too long (max {rule.max_digits} digits)"
        
        # Pattern validation if exists
        if rule.pattern and not re.match(rule.pattern, cleaned):
            return False, f"Phone number doesn't match country pattern"
        
        return True, ""
    
    @staticmethod
    def validate_with_phonenumbers(phone: str, country_code: str = "IN") -> tuple[bool, str]:
        """Validate using phonenumbers library"""
        try:
            parsed = phonenumbers.parse(phone, country_code)
            if phonenumbers.is_valid_number(parsed):
                return True, ""
            else:
                return False, "Invalid phone number"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def format_phone(phone: str, country_code: str = "IN") -> str:
        """Format phone number to standard format"""
        try:
            parsed = phonenumbers.parse(phone, country_code)
            return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        except:
            return PhoneValidator.clean_phone(phone)