from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import UUID

class RegisterRequest(BaseModel):
    """Request schema for user registration."""
    username: str = Field(..., description="User's unique username")

class RegisterResponse(BaseModel):
    """Response schema for user registration."""
    user_id: UUID = Field(..., description="Generated user ID")

class UploadResumeResponse(BaseModel):
    """Response schema for resume upload."""
    message: str = Field(..., description="Success message")
    user_id: UUID = Field(..., description="User ID")
    filename: str = Field(..., description="Original filename")
    extracted_length: int = Field(..., description="Length of extracted text")

class GenerateEmailRequest(BaseModel):
    """Request schema for email generation."""
    user_id: UUID = Field(..., description="User's UUID")
    hr_id: UUID = Field(..., description="HR contact UUID containing job description")

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
    hr_id: UUID = Field(..., description="Generated HR contact ID")

class HRContactData(BaseModel):
    """Schema for individual HR contact data in bulk creation."""
    name: Optional[str] = Field(None, description="HR contact name")
    title: Optional[str] = Field(None, description="HR contact title/headline")
    company: Optional[str] = Field(None, description="HR contact company")
    profile_url: Optional[str] = Field(None, alias="profileUrl", description="LinkedIn profile URL")
    post_url: Optional[str] = Field(None, alias="postUrl", description="LinkedIn post URL")
    email: Optional[str] = Field(None, description="HR contact email address")
    job_link: Optional[str] = Field(None, alias="jobLink", description="Job listing URL")
    post_preview: Optional[str] = Field(None, alias="postPreview", description="Preview text from the post")
    extracted_at: Optional[datetime] = Field(None, alias="extractedAt", description="When the data was extracted")
    matched_keywords: List[str] = Field(default_factory=list, alias="matchedKeywords", description="Keywords matched in the post")

    class Config:
        populate_by_name = True

class BulkCreateHRContactsRequest(BaseModel):
    """Request schema for bulk HR contact creation."""
    user_id: UUID = Field(..., description="User ID who owns these HR contacts")
    hr_contacts: List[HRContactData] = Field(..., description="List of HR contacts to create")

class BulkCreateHRContactsResponse(BaseModel):
    """Response schema for bulk HR contact creation."""
    created_count: int = Field(..., description="Number of successfully created contacts")
    hr_ids: List[UUID] = Field(..., description="List of created HR contact IDs")
    failed_count: int = Field(..., description="Number of failed contacts")
    failed_contacts: List[dict] = Field(..., description="List of failed contacts with error details")
