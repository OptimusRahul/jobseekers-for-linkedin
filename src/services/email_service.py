"""Email generation orchestration service."""
from typing import Dict

from src.services import user_service, openai_service, vector_service
from typing import Dict, Any

from src.services.user_service import get_user_by_username
from src.services.vector_service import get_resume_by_user_id
from src.services.openai_service import generate_email

def generate_email(username: str, job_description: str) -> Dict[str, Any]:
    """
    Generate email for a user based on job description.
    
    Args:
        username: User's username
        job_description: Job description text
        
    Returns:
        Dictionary with subject and body
        
    Raises:
        ValueError: If user or resume not found
    """
    # Get user
    user = get_user_by_username(username)
    if not user:
        raise ValueError(f"User with username {username} not found")
    
    # Extract user_id while user object is still bound to session
    user_id = str(user.id)
    
    # Step 2: Get user's resume from PostgreSQL
    resume_data = get_resume_by_user_id(user_id)
    if not resume_data or not resume_data.get("resume_text"):
        raise ValueError(f"Resume not found for user: {username}")
    
    resume_text = resume_data["resume_text"]
    
    # Step 3: Generate email using OpenAI
    email_result = openai_service.generate_email(
        resume_text=resume_text,
        job_description=job_description
    )
    
    return email_result
