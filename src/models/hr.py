"""HR contact database model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID

from src.models.base import Base

class HRContact(Base):
    """HR contact model for PostgreSQL."""
    __tablename__ = "hr_contacts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    job_description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<HRContact(id={self.id}, email={self.email})>"
