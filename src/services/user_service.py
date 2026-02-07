"""User service for registration and user management."""
from typing import Optional
from sqlalchemy.exc import IntegrityError

from src.lib.postgres import get_db   
from src.models.user import User
from src.utils.validators import validate_phone_number, normalize_phone_number

def register_user(phone_number: str, name: str, email: str) -> str:
    """
    Register a new user.
    
    Args:
        phone_number: User's phone number
        name: User's name
        email: User's email
        
    Returns:
        User ID as string
        
    Raises:
        ValueError: If phone number is invalid or user already exists
    """
    # Validate phone number
    if not validate_phone_number(phone_number):
        raise ValueError("Invalid phone number format. Use format: +1234567890")
    
    # Normalize phone number
    normalized_phone = normalize_phone_number(phone_number)
    
    # Create user
    with get_db() as db:
        # Check if user already exists
        existing_user = db.query(User).filter(User.phone_number == normalized_phone).first()
        if existing_user:
            raise ValueError("User with this phone number already exists")
        
        # Create new user
        user = User(
            phone_number=normalized_phone,
            name=name,
            email=email
        )
        
        try:
            db.add(user)
            db.commit()
            db.refresh(user)
            return str(user.id)
        except IntegrityError:
            raise ValueError("User with this phone number already exists")

def get_user_by_phone(phone_number: str) -> Optional[User]:
    """
    Get user by phone number.
    
    Args:
        phone_number: User's phone number
        
    Returns:
        User object or None if not found
    """
    # Normalize phone number
    normalized_phone = normalize_phone_number(phone_number)
    
    with get_db() as db:
        return db.query(User).filter(User.phone_number == normalized_phone).first()

def get_user_by_id(user_id: str) -> Optional[User]:
    """
    Get user by ID.
    
    Args:
        user_id: User's UUID
        
    Returns:
        User object or None if not found
    """
    with get_db() as db:
        return db.query(User).filter(User.id == user_id).first()
