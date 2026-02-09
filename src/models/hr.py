"""HR contact database model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.models.base import Base

class HRContact(Base):
    """HR contact model for PostgreSQL."""
    __tablename__ = "hr_contacts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    name = Column(String, nullable=True)
    title = Column(String, nullable=True)
    company = Column(String, nullable=True)
    profile_url = Column(String, nullable=True)
    post_url = Column(String, nullable=True)
    email = Column(String, nullable=True)  # Changed to nullable=True
    job_link = Column(String, nullable=True)
    post_preview = Column(Text, nullable=True)
    matched_keywords = Column(JSON, nullable=True)
    extracted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Keep job_description for backward compatibility if needed, or remove it.
    # The user request suggests "fix the get and post endpoints" based on the new JSON.
    # I'll replace job_description with post_preview in the service layer logic.
    # But for the database, let's just add the new fields.
    job_description = Column(Text, nullable=True) 
    
    # Relationship to User
    user = relationship("User", back_populates="hr_contacts")
    
    def __repr__(self):
        return f"<HRContact(id={self.id}, user_id={self.user_id}, name={self.name}, email={self.email})>"
