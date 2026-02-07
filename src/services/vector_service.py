"""Vector service for PostgreSQL pgvector operations."""
from typing import List, Optional, Dict
import uuid

from lib.postgres import get_db
from models.resume import Resume

def store_resume_embedding(user_id: str, resume_text: str, embedding: List[float]) -> None:
    """
    Store resume embedding in PostgreSQL with pgvector.
    
    Args:
        user_id: User's UUID
        resume_text: Resume text content
        embedding: Embedding vector (list of floats)
    """
    with get_db() as db:
        # Check if resume already exists
        existing_resume = db.query(Resume).filter(Resume.user_id == user_id).first()
        
        if existing_resume:
            # Update existing resume
            existing_resume.resume_text = resume_text
            existing_resume.resume_embedding = embedding
        else:
            # Create new resume
            resume = Resume(
                user_id=uuid.UUID(user_id),
                resume_text=resume_text,
                resume_embedding=embedding
            )
            db.add(resume)

def get_resume_by_user_id(user_id: str) -> Optional[Dict]:
    """
    Get resume by user ID.
    
    Args:
        user_id: User's UUID
        
    Returns:
        Dictionary with resume data or None if not found
    """
    with get_db() as db:
        resume = db.query(Resume).filter(Resume.user_id == user_id).first()
        
        if resume:
            return {
                "user_id": str(resume.user_id),
                "resume_text": resume.resume_text,
                "embedding": resume.resume_embedding
            }
        
        return None

def search_similar_resume(embedding: List[float], limit: int = 1) -> Optional[Dict]:
    """
    Search for similar resume using vector similarity (cosine distance).
    
    Args:
        embedding: Query embedding vector
        limit: Number of results to return
        
    Returns:
        Dictionary with user_id and resume_text, or None if not found
    """
    with get_db() as db:
        # Use pgvector's cosine distance operator (<=>)
        # Lower distance = more similar
        result = db.query(Resume).order_by(
            Resume.resume_embedding.cosine_distance(embedding)
        ).limit(limit).first()
        
        if result:
            return {
                "user_id": str(result.user_id),
                "resume_text": result.resume_text
            }
        
        return None
