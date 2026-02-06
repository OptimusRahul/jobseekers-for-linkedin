"""File parsing utilities for resume extraction."""
import io
from typing import BinaryIO
from pathlib import Path

from PyPDF2 import PdfReader
from docx import Document


def extract_text_from_pdf(file: BinaryIO) -> str:
    """
    Extract text from PDF file.
    
    Args:
        file: Binary file object
        
    Returns:
        Extracted text content
    """
    try:
        pdf_reader = PdfReader(file)
        text_parts = []
        
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)
        
        return "\n\n".join(text_parts).strip()
    except Exception as e:
        raise ValueError(f"Failed to parse PDF: {str(e)}")


def extract_text_from_docx(file: BinaryIO) -> str:
    """
    Extract text from DOCX file.
    
    Args:
        file: Binary file object
        
    Returns:
        Extracted text content
    """
    try:
        doc = Document(file)
        text_parts = []
        
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text_parts.append(paragraph.text)
        
        return "\n\n".join(text_parts).strip()
    except Exception as e:
        raise ValueError(f"Failed to parse DOCX: {str(e)}")


def extract_text_from_txt(file: BinaryIO) -> str:
    """
    Extract text from TXT file.
    
    Args:
        file: Binary file object
        
    Returns:
        Extracted text content
    """
    try:
        content = file.read()
        
        # Try UTF-8 first
        try:
            return content.decode('utf-8').strip()
        except UnicodeDecodeError:
            # Fallback to latin-1
            return content.decode('latin-1').strip()
    except Exception as e:
        raise ValueError(f"Failed to parse TXT: {str(e)}")


def parse_resume_file(file_content: bytes, filename: str) -> str:
    """
    Parse resume file and extract text content.
    
    Supports: PDF, DOCX, TXT
    
    Args:
        file_content: File content as bytes
        filename: Original filename
        
    Returns:
        Extracted text content
        
    Raises:
        ValueError: If file format is not supported or parsing fails
    """
    # Get file extension
    extension = Path(filename).suffix.lower()
    
    # Create file-like object
    file_obj = io.BytesIO(file_content)
    
    # Parse based on extension
    if extension == '.pdf':
        text = extract_text_from_pdf(file_obj)
    elif extension in ['.docx', '.doc']:
        text = extract_text_from_docx(file_obj)
    elif extension == '.txt':
        text = extract_text_from_txt(file_obj)
    else:
        raise ValueError(
            f"Unsupported file format: {extension}. "
            f"Supported formats: .pdf, .docx, .doc, .txt"
        )
    
    # Validate extracted text
    if not text or len(text.strip()) < 50:
        raise ValueError(
            "Resume appears to be empty or too short. "
            "Please ensure the file contains valid text content."
        )
    
    return text


def get_supported_extensions() -> list[str]:
    """
    Get list of supported file extensions.
    
    Returns:
        List of supported extensions (e.g., ['.pdf', '.docx', '.txt'])
    """
    return ['.pdf', '.docx', '.doc', '.txt']


def validate_file_size(file_size: int, max_size_mb: int = 10) -> None:
    """
    Validate file size.
    
    Args:
        file_size: File size in bytes
        max_size_mb: Maximum allowed size in MB
        
    Raises:
        ValueError: If file size exceeds limit
    """
    max_size_bytes = max_size_mb * 1024 * 1024
    
    if file_size > max_size_bytes:
        raise ValueError(
            f"File size ({file_size / 1024 / 1024:.2f} MB) exceeds "
            f"maximum allowed size ({max_size_mb} MB)"
        )
