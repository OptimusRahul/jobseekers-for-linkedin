"""Validation utilities."""
import re

def validate_phone_number(phone_number: str) -> bool:
    """
    Validate phone number format.
    
    Accepts formats like:
    - +1234567890
    - +1-234-567-8900
    - +1 (234) 567-8900
    
    Args:
        phone_number: Phone number string
        
    Returns:
        True if valid, False otherwise
    """
    # Remove spaces, hyphens, parentheses
    cleaned = re.sub(r'[\s\-\(\)]', '', phone_number)
    
    # Check if it starts with + and has 10-15 digits
    pattern = r'^\+\d{10,15}$'
    return bool(re.match(pattern, cleaned))

def normalize_phone_number(phone_number: str) -> str:
    """
    Normalize phone number by removing formatting.
    
    Args:
        phone_number: Phone number string
        
    Returns:
        Normalized phone number (e.g., "+1234567890")
    """
    # Remove all non-digit characters except +
    return re.sub(r'[^\d+]', '', phone_number)
