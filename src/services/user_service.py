"""User service for registration and user management."""
from typing import Optional
from sqlalchemy.exc import IntegrityError

from src.lib.postgres import get_db   
from src.models.user import User
from src.models.user import User

def register_user(username: str) -> str:
    """
    Register a new user.
    
    Args:
        username: User's username
        
    Returns:
        User ID as string
        
    Raises:
        ValueError: If user already exists
    """
    with get_db() as db:
        # Check if user already exists
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            raise ValueError("User with this username already exists")
        
        # Create new user
        user = User(
            username=username
        )
        
        try:
            db.add(user)
            db.commit()
            db.refresh(user)
            return str(user.id)
        except IntegrityError:
            raise ValueError("User with this username already exists")

def get_user_by_username(username: str) -> Optional[User]:
    """
    Get user by username.
    
    Args:
        username: User's username
        
    Returns:
        User object or None if not found
    """
    with get_db() as db:
        user = db.query(User).filter(User.username == username).first()
        if user:
            db.expunge(user)
        return user

def get_user_by_id(user_id: str) -> Optional[User]:
    """
    Get user by ID.
    
    Args:
        user_id: User's UUID
        
    Returns:
        User object or None if not found
    """
    with get_db() as db:
        try:
            uuid_obj = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
            user = db.query(User).filter(User.id == uuid_obj).first()
            if user:
                db.expunge(user)
            return user
        except (ValueError, AttributeError):
            return None
