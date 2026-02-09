"""HR contact service for storing HR information."""
from typing import Optional
from sqlalchemy.exc import IntegrityError

from src.lib.postgres import get_db
from src.models.hr import HRContact

def create_hr_contacts(hr_contacts: list) -> dict:
    """
    Create one or more HR contact entries.
    
    Args:
        hr_contacts: List of dictionaries with keys: email, job_description, phone (optional)
                    Example: [{"email": "hr@company.com", "job_description": "...", "phone": "+123"}]
        
    Returns:
        Dictionary with created_count, list of hr_ids, failed_count, and failed_contacts
        
    Raises:
        ValueError: If validation fails
    """
    if not hr_contacts or not isinstance(hr_contacts, list):
        raise ValueError("hr_contacts must be a non-empty list")
    
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
                
                # Create HR contact
                hr_contact = HRContact(
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

def get_hr_contact_by_id(hr_id: str) -> Optional[HRContact]:
    """
    Get HR contact by ID.
    
    Args:
        hr_id: HR contact UUID
        
    Returns:
        HRContact object or None if not found
    """
    with get_db() as db:
        return db.query(HRContact).filter(HRContact.id == hr_id).first()

def get_all_hr_contacts(limit: int = 100) -> list:
    """
    Get all HR contacts.
    
    Args:
        limit: Maximum number of contacts to return
        
    Returns:
        List of HRContact objects
    """
    with get_db() as db:
        return db.query(HRContact).limit(limit).all()
