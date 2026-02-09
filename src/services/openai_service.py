"""OpenAI service for embeddings and chat completion."""
import json
from typing import List, Dict, Optional

from src.lib.openai_client import get_openai_client
from src.config import config
from src.prompts.email_prompt import create_email_prompt

def create_embedding(text: str) -> List[float]:
    """
    Create embedding for text using OpenAI.
    
    Args:
        text: Text to embed
        
    Returns:
        List of floats representing the embedding vector
    """
    client = get_openai_client()
    
    response = client.embeddings.create(
        model=config.EMBEDDING_MODEL,
        input=text
    )
    
    return response.data[0].embedding

def generate_email(
    resume_text: str, 
    job_description: str,
    hr_name: Optional[str] = None,
    hr_title: Optional[str] = None,
    company: Optional[str] = None
) -> Dict[str, str]:
    """
    Generate personalized email using OpenAI chat completion.
    
    Args:
        resume_text: Candidate's resume text
        job_description: Job description text
        hr_name: HR contact name (optional)
        hr_title: HR contact title (optional)
        company: Company name (optional)
        
    Returns:
        Dictionary with 'subject' and 'body' keys
    """
    client = get_openai_client()
    
    # Create prompt
    prompt = create_email_prompt(
        resume_text=resume_text, 
        job_description=job_description,
        hr_name=hr_name,
        hr_title=hr_title,
        company=company
    )
    
    # Call OpenAI
    response = client.chat.completions.create(
        model=config.CHAT_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.7,
        max_tokens=1000
    )
    
    # Parse response
    result = json.loads(response.choices[0].message.content)
    
    # Validate response structure
    if "subject" not in result or "body" not in result:
        raise ValueError("Invalid response format from OpenAI")
    
    return {
        "subject": result["subject"],
        "body": result["body"]
    }
