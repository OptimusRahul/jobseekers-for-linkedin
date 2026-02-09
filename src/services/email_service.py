"""Email generation orchestration service."""
from typing import Dict, Any

from src.services import openai_service, vector_service
from src.services.hr_service import get_hr_contact_by_id

def generate_email(user_id: str, hr_id: str) -> Dict[str, Any]:
    """
    Generate email for a user based on HR contact job description.
    
    Args:
        user_id: User's UUID
        hr_id: HR contact UUID
        
    Returns:
        Dictionary with subject and body
        
    Raises:
        ValueError: If HR contact or resume not found
    """
    # Step 1: Get HR contact (which includes job description)
    hr_contact = get_hr_contact_by_id(user_id=user_id, hr_id=hr_id)
    if not hr_contact:
        raise ValueError(f"HR contact with ID {hr_id} not found for user {user_id}")
    
    job_description = hr_contact.job_description
    
    # Step 2: Get user's resume from PostgreSQL
    resume_data = vector_service.get_resume_by_user_id(user_id)
    if not resume_data or not resume_data.get("resume_text"):
        raise ValueError(f"Resume not found for user: {user_id}")
    
    resume_text = resume_data["resume_text"]
    
    # Step 3: Generate email using OpenAI
    email_result = openai_service.generate_email(
        resume_text=resume_text,
        job_description=job_description,
        hr_name=hr_contact.name,
        hr_title=hr_contact.title,
        company=hr_contact.company
    )
    
    return email_result
