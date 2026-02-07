FROM python:3.9-slim

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install python deps (cache friendly)
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

EXPOSE 8000

# Run migrations + start FastAPI
CMD sh -c "alembic upgrade head && python -m uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}"
