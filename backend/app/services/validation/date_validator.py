from datetime import datetime, date
from typing import Optional, Tuple
import re
from dateutil import parser

class DateValidator:
    
    SUPPORTED_FORMATS = [
        "%Y-%m-%d",      # 2024-01-15
        "%d-%m-%Y",      # 15-01-2024
        "%m/%d/%Y",      # 01/15/2024
        "%d/%m/%Y",      # 15/01/2024
        "%Y/%m/%d",      # 2024/01/15
        "%d.%m.%Y",      # 15.01.2024
        "%Y.%m.%d",      # 2024.01.15
    ]
    
    TIME_FORMATS = [
        "%H:%M",         # 14:30
        "%H:%M:%S",      # 14:30:45
        "%I:%M %p",      # 02:30 PM
        "%I:%M:%S %p",   # 02:30:45 PM
    ]
    
    @classmethod
    def parse_date(cls, date_str: str) -> Optional[date]:
        """Parse date string to date object"""
        if not date_str or str(date_str).strip() == "":
            return None
        
        date_str = str(date_str).strip()
        
        # Try each format
        for fmt in cls.SUPPORTED_FORMATS:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        
        # Try intelligent parsing
        try:
            return parser.parse(date_str).date()
        except:
            return None
    
    @classmethod
    def validate_date(cls, date_str: str, allow_future: bool = False) -> Tuple[bool, str, Optional[date]]:
        """
        Validate date string
        Returns: (is_valid, error_message, parsed_date)
        """
        if not date_str or str(date_str).strip() == "":
            return False, "Date is empty", None
        
        parsed = cls.parse_date(date_str)
        
        if parsed is None:
            return False, "Invalid date format", None
        
        # Check if future date
        if not allow_future and parsed > date.today():
            return False, "Future date not allowed", parsed
        
        # Check reasonable date range (e.g., after 1900)
        if parsed.year < 1900:
            return False, "Date too old (before 1900)", parsed
        
        return True, "", parsed
    
    @classmethod
    def parse_time(cls, time_str: str) -> Optional[datetime.time]:
        """Parse time string to time object"""
        if not time_str or str(time_str).strip() == "":
            return None
        
        time_str = str(time_str).strip()
        
        for fmt in cls.TIME_FORMATS:
            try:
                return datetime.strptime(time_str, fmt).time()
            except ValueError:
                continue
        
        return None
    
    @classmethod
    def validate_time(cls, time_str: str) -> Tuple[bool, str, Optional[datetime.time]]:
        """
        Validate time string
        Returns: (is_valid, error_message, parsed_time)
        """
        if not time_str or str(time_str).strip() == "":
            return False, "Time is empty", None
        
        parsed = cls.parse_time(time_str)
        
        if parsed is None:
            return False, "Invalid time format", None
        
        return True, "", parsed
    
    @staticmethod
    def standardize_date(dt: date, format: str = "%Y-%m-%d") -> str:
        """Convert date to standard format"""
        return dt.strftime(format)