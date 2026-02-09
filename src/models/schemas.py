"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, Field

class RegisterRequest(BaseModel):
    """Request schema for user registration."""
    username: str = Field(..., description="User's unique username")

class RegisterResponse(BaseModel):
    """Response schema for user registration."""
    user_id: str = Field(..., description="Generated user ID")

class UploadResumeResponse(BaseModel):
    """Response schema for resume upload."""
    message: str = Field(..., description="Success message")
    user_id: str = Field(..., description="User ID")
    filename: str = Field(..., description="Original filename")
    extracted_length: int = Field(..., description="Length of extracted text")

class GenerateEmailRequest(BaseModel):
    """Request schema for email generation."""
    username: str = Field(..., description="User's username")
    job_description: str = Field(..., description="Job description text")

class GenerateEmailResponse(BaseModel):
    """Response schema for email generation."""
    subject: str = Field(..., description="Email subject line")
    body: str = Field(..., description="Email body content")
