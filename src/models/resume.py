"""Resume database model with vector embeddings."""
import uuid
from datetime import datetime
from typing import List
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector

from src.config import config
from src.models.base import Base

class Resume(Base):
    """Resume model with vector embeddings for PostgreSQL."""
    __tablename__ = "resumes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, unique=True)
    resume_text = Column(Text, nullable=False)
    resume_embedding = Column(Vector(config.EMBEDDING_DIMENSIONS), nullable=False)  # type: List[float]
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Resume(id={self.id}, user_id={self.user_id})>"
