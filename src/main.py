"""FastAPI application entry point."""
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional
import uuid
import logging
import traceback

from src.config import config
from src.services import (
    register_user as register_user_service, 
    get_user_by_phone, 
    get_user_by_id, 
    create_embedding, 
    generate_email as generate_email_service, 
    store_resume_embedding, 
    get_resume_by_user_id, 
    search_similar_resume
)
from src.models.schemas import RegisterRequest, RegisterResponse, UploadResumeResponse, GenerateEmailRequest, GenerateEmailResponse
from src.utils.file_parser import parse_resume_file, validate_file_size, get_supported_extensions

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Validate configuration on startup
config.validate()

app = FastAPI(
    title="Job Email Generator API",
    description="Generate personalized job application emails using AI",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    """Run startup checks."""
    logger.info("=" * 60)
    logger.info("Starting Job Email Generator API...")
    logger.info("=" * 60)
    
    # Check database connection
    from .lib.postgres import check_database_connection, check_pgvector_extension
    
    if check_database_connection():
        logger.info("Database: Connected to PostgreSQL")
        check_pgvector_extension()
    else:
        logger.error("Database: Connection failed - API may not work properly")
    
    logger.info("=" * 60)
    logger.info("API Ready: http://localhost:8000")
    logger.info("API Docs: http://localhost:8000/docs")
    logger.info("=" * 60)

@app.get("/")
def read_root():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Job Email Generator API"}

@app.get("/health")
def health_check():
    """Detailed health check including database status."""
    from .lib.postgres import check_database_connection, check_pgvector_extension
    
    db_connected = check_database_connection()
    pgvector_enabled = check_pgvector_extension() if db_connected else False
    
    status = "healthy" if db_connected and pgvector_enabled else "degraded"
    
    return {
        "status": status,
        "database": {
            "connected": db_connected,
            "pgvector_enabled": pgvector_enabled
        },
        "api_version": "1.0.0"
    }

@app.post("/register", response_model=RegisterResponse)
def register(request: RegisterRequest):
    """Register a new user with phone number."""
    try:
        user_id = register_user_service(
            phone_number=request.phone_number,
            name=request.name,
            email=request.email
        )
        return RegisterResponse(user_id=user_id)
    except ValueError as e:
        logger.warning(f"Registration validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Registration failed: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@app.post("/upload-resume", response_model=UploadResumeResponse)
async def upload_resume(
    user_id: str = Form(..., description="User ID from registration"),
    file: UploadFile = File(..., description="Resume file (PDF, DOCX, or TXT)")
):
    """
    Upload resume file and generate embeddings.
    
    Accepts: PDF, DOCX, DOC, TXT files (max 10MB)
    """
    try:
        # Validate user exists
        try:
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid user_id format")
        
        user = get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Read file content
        file_content = await file.read()
        file_size = len(file_content)
        
        # Validate file size (10MB limit)
        try:
            validate_file_size(file_size, max_size_mb=10)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
        # Validate file extension
        supported_extensions = get_supported_extensions()
        if not any(file.filename.lower().endswith(ext) for ext in supported_extensions):
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format. Supported: {', '.join(supported_extensions)}"
            )
        
        # Parse resume file
        try:
            resume_text = parse_resume_file(file_content, file.filename)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
        # Generate embedding for resume
        embedding = create_embedding(resume_text)
        
        # Store in PostgreSQL with pgvector
        store_resume_embedding(
            user_id=user_id,
            resume_text=resume_text,
            embedding=embedding
        )
        
        return UploadResumeResponse(
            message="success",
            user_id=user_id,
            filename=file.filename,
            extracted_length=len(resume_text)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Resume upload failed: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Resume upload failed: {str(e)}")

@app.post("/gen-email", response_model=GenerateEmailResponse)
def generate_email(request: GenerateEmailRequest):
    """Generate personalized job application email."""
    try:
        result = generate_email_service(
            phone_number=request.phone_number,
            job_description=request.job_description
        )
        return GenerateEmailResponse(subject=result["subject"], body=result["body"])
    except ValueError as e:
        logger.warning(f"Email generation validation error: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Email generation failed: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Email generation failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
