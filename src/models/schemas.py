"""Pydantic schemas for request/response validation."""
from typing import Optional, List
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

class CreateHRContactRequest(BaseModel):
    """Request schema for creating HR contact."""
    email: str = Field(..., description="HR contact email address")
    phone: Optional[str] = Field(None, description="HR contact phone number (optional)")
    job_description: str = Field(..., description="Job description text")

class CreateHRContactResponse(BaseModel):
    """Response schema for HR contact creation."""
    hr_id: str = Field(..., description="Generated HR contact ID")

class HRContactData(BaseModel):
    """Schema for individual HR contact data in bulk creation."""
    email: str = Field(..., description="HR contact email address")
    phone: Optional[str] = Field(None, description="HR contact phone number (optional)")
    job_description: str = Field(..., description="Job description text")

class BulkCreateHRContactsRequest(BaseModel):
    """Request schema for bulk HR contact creation."""
    user_id: str = Field(..., description="User ID who owns these HR contacts")
    hr_contacts: List[HRContactData] = Field(..., description="List of HR contacts to create")

class BulkCreateHRContactsResponse(BaseModel):
    """Response schema for bulk HR contact creation."""
    created_count: int = Field(..., description="Number of successfully created contacts")
    hr_ids: List[str] = Field(..., description="List of created HR contact IDs")
    failed_count: int = Field(..., description="Number of failed contacts")
    failed_contacts: List[dict] = Field(..., description="List of failed contacts with error details")
