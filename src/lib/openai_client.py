"""OpenAI client initialization."""
from openai import OpenAI
from src.config import config

# Initialize OpenAI client
client = OpenAI(api_key=config.OPENAI_API_KEY)

def get_openai_client():
    """Get OpenAI client instance."""
    return client
