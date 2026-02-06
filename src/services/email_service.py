"""Email generation orchestration service."""
from typing import Dict

from src.services import user_service, openai_service, vector_service

def generate_email(phone_number: str, job_description: str) -> Dict[str, str]:
    """
    Generate personalized job application email.
    
    This is the main orchestration function that:
    1. Fetches user from Postgres by phone number
    2. Generates JD embedding using OpenAI
    3. Retrieves resume from PostgreSQL (by user_id)
    4. Calls OpenAI to generate email with resume + JD
    5. Returns formatted email
    
    Args:
        phone_number: User's phone number
        job_description: Job description text
        
    Returns:
        Dictionary with 'subject' and 'body' keys
        
    Raises:
        ValueError: If user not found or resume not found
    """
    # Step 1: Get user from Postgres
    user = user_service.get_user_by_phone(phone_number)
    if not user:
        raise ValueError(f"User not found with phone number: {phone_number}")
    
    # Extract user_id while user object is still bound to session
    user_id = str(user.id)
    
    # Step 2: Get user's resume from PostgreSQL
    resume_data = vector_service.get_resume_by_user_id(user_id)
    if not resume_data or not resume_data.get("resume_text"):
        raise ValueError(f"Resume not found for user: {phone_number}")
    
    resume_text = resume_data["resume_text"]
    
    # Step 3: Generate email using OpenAI
    email_result = openai_service.generate_email(
        resume_text=resume_text,
        job_description=job_description
    )
    
    return email_result
