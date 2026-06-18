import re
from email_validator import validate_email, EmailNotValidError

class EmailValidator:
    
    @staticmethod
    def is_valid_email(email: str) -> tuple[bool, str]:
        """Validate email format"""
        if not email or email.strip() == "":
            return False, "Email is empty"
        
        try:
            # Validate and normalize
            valid = validate_email(email, check_deliverability=False)
            return True, ""
        except EmailNotValidError as e:
            return False, str(e)
    
    @staticmethod
    def has_at_symbol(email: str) -> bool:
        """Check if email contains @"""
        return "@" in email if email else False
    
    @staticmethod
    def get_domain(email: str) -> str:
        """Extract domain from email"""
        if not email or "@" not in email:
            return ""
        return email.split("@")[1].lower()
    
    @staticmethod
    def is_gmail(email: str) -> bool:
        """Check if email is Gmail"""
        domain = EmailValidator.get_domain(email)
        return domain == "gmail.com"
    
    @staticmethod
    def validate_domain(email: str) -> tuple[bool, str]:
        """Validate email domain"""
        domain = EmailValidator.get_domain(email)
        if not domain:
            return False, "Invalid domain"
        
        # Basic domain validation
        domain_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$'
        
        if not re.match(domain_pattern, domain):
            return False, "Invalid domain format"
        
        return True, ""