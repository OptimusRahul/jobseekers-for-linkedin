"""HR contact service for storing HR information."""
from typing import Optional
from sqlalchemy.exc import IntegrityError
import uuid

from src.lib.postgres import get_db
from src.models.hr import HRContact

def create_hr_contacts(user_id: str, hr_contacts: list) -> dict:
    """
    Create one or more HR contact entries for a specific user.
    
    Args:
        user_id: User's UUID
        hr_contacts: List of dictionaries with keys: email, job_description, phone (optional)
                    Example: [{"email": "hr@company.com", "job_description": "...", "phone": "+123"}]
        
    Returns:
        Dictionary with created_count, list of hr_ids, failed_count, and failed_contacts
        
    Raises:
        ValueError: If validation fails
    """
    if not hr_contacts or not isinstance(hr_contacts, list):
        raise ValueError("hr_contacts must be a non-empty list")
    
    # Validate user_id
    try:
        user_uuid = uuid.UUID(user_id)
    except (ValueError, AttributeError):
        raise ValueError("Invalid user_id format")
    
    created_ids = []
    failed_contacts = []
    
    with get_db() as db:
        for idx, contact_data in enumerate(hr_contacts):
            try:
                # Validate required fields
                email = contact_data.get("email")
                job_description = contact_data.get("job_description")
                phone = contact_data.get("phone")
                
                if not email or "@" not in email:
                    failed_contacts.append({"index": idx, "error": "Invalid email address"})
                    continue
                
                if not job_description or len(job_description.strip()) == 0:
                    failed_contacts.append({"index": idx, "error": "Job description cannot be empty"})
                    continue
                
                # Create HR contact with user_id
                hr_contact = HRContact(
                    user_id=user_uuid,
                    email=email,
                    phone=phone,
                    job_description=job_description
                )
                
                db.add(hr_contact)
                db.flush()  # Get the ID without committing yet
                created_ids.append(str(hr_contact.id))
                
            except Exception as e:
                failed_contacts.append({"index": idx, "error": str(e)})
        
        # Commit all at once
        try:
            db.commit()
        except IntegrityError as e:
            raise ValueError(f"Failed to create HR contacts: {str(e)}")
    
    return {
        "created_count": len(created_ids),
        "hr_ids": created_ids,
        "failed_count": len(failed_contacts),
        "failed_contacts": failed_contacts
    }

def get_hr_contact_by_id(user_id: str, hr_id: str) -> Optional[HRContact]:
    """
    Get HR contact by ID for a specific user.
    
    Args:
        user_id: User's UUID
        hr_id: HR contact UUID
        
    Returns:
        HRContact object or None if not found or doesn't belong to user
    """
    with get_db() as db:
        return db.query(HRContact).filter(
            HRContact.id == hr_id,
            HRContact.user_id == user_id
        ).first()

def get_all_hr_contacts(user_id: str, limit: int = 100) -> list:
    """
    Get all HR contacts for a specific user.
    
    Args:
        user_id: User's UUID
        limit: Maximum number of contacts to return
        
    Returns:
        List of HRContact objects belonging to the user
    """
    with get_db() as db:
        return db.query(HRContact).filter(
            HRContact.user_id == user_id
        ).limit(limit).all()
