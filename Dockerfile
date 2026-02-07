# Use Python 3.9 to match Render environment
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies (added gcc for some Python packages)
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

# Expose port
EXPOSE 8000

# Run migrations then start the app (Railway will provide $PORT)
CMD ["sh", "-c", "alembic upgrade head && cd src && python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]