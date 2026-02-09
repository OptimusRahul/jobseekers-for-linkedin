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
        hr_contacts: List of dictionaries with expanded HR contact data.
                     Keys match HRContactData schema (snake_case).
        
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
                # Map fields from dictionary
                # Use .get() for optional fields
                name = contact_data.get("name")
                title = contact_data.get("title")
                company = contact_data.get("company")
                profile_url = contact_data.get("profile_url")
                post_url = contact_data.get("post_url")
                email = contact_data.get("email")
                job_link = contact_data.get("job_link")
                post_preview = contact_data.get("post_preview")
                matched_keywords = contact_data.get("matched_keywords", [])
                extracted_at = contact_data.get("extracted_at")
                
                # Basic validation: we need at least a name or an email or a post preview
                if not any([name, email, post_preview]):
                    failed_contacts.append({"index": idx, "error": "Contact must have at least a name, email, or post preview"})
                    continue
                
                # Create HR contact with user_id
                hr_contact = HRContact(
                    user_id=user_uuid,
                    name=name,
                    title=title,
                    company=company,
                    profile_url=profile_url,
                    post_url=post_url,
                    email=email,
                    job_link=job_link,
                    post_preview=post_preview,
                    job_description=post_preview, # Sync for compatibility
                    matched_keywords=matched_keywords,
                    extracted_at=extracted_at
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
            db.rollback()
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
