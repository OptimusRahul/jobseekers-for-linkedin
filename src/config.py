"""Configuration management for the application."""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration."""
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # OpenAI Models
    EMBEDDING_MODEL = "text-embedding-3-small"
    CHAT_MODEL = "gpt-4o-mini"
    
    # Vector embedding dimensions
    EMBEDDING_DIMENSIONS = 1536  # for text-embedding-3-small
    
    @classmethod
    def validate(cls):
        """Validate that all required config values are set."""
        required = [
            "DATABASE_URL",
            "OPENAI_API_KEY"
        ]
        missing = [key for key in required if not getattr(cls, key)]
        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")

config = Config()
