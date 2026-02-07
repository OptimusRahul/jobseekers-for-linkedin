# Docker Testing Guide

This guide will help you test the application locally using Docker before deploying to Render.

## Prerequisites

- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed (usually comes with Docker Desktop)
- OpenAI API key

## Quick Start

### 1. Set up environment variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Then edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-actual-openai-api-key
```

### 2. Build and run with Docker Compose

```bash
# Build and start all services (database + API)
docker-compose up --build

# Or run in detached mode (background)
docker-compose up -d --build
```

This will:
- Start PostgreSQL with pgvector extension
- Run database migrations automatically
- Start the FastAPI application on http://localhost:8000

### 3. Test the API

Open your browser and visit:
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### 4. Stop the services

```bash
# Stop and remove containers
docker-compose down

# Stop and remove containers + volumes (clears database)
docker-compose down -v
```

## Testing Individual Components

### Test the Build Only

```bash
# Build the Docker image
docker build -t job-email-api .

# Check if the build succeeded
docker images | grep job-email-api
```

### Test the Application Container

```bash
# Run just the API container (without database)
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_key_here \
  -e DATABASE_URL=your_db_url \
  job-email-api
```

### View Logs

```bash
# View all logs
docker-compose logs

# View API logs only
docker-compose logs web

# Follow logs in real-time
docker-compose logs -f web
```

### Access the Container Shell

```bash
# Access the running API container
docker-compose exec web bash

# Inside container, you can:
python -m pip list
python -c "import src.main; print('Import successful!')"
alembic current
```

## Production-Like Testing

To test exactly as it will run on Render (without hot-reload):

1. **Edit `docker-compose.yml`** - Comment out the volumes section under `web` service
2. **Change the command** to:
   ```yaml
   command: >
     sh -c "
       alembic upgrade head &&
       python -m uvicorn src.main:app --host 0.0.0.0 --port 8000
     "
   ```
3. **Rebuild and test**:
   ```bash
   docker-compose down
   docker-compose up --build
   ```

## Troubleshooting

### Database Connection Issues

```bash
# Check if database is ready
docker-compose exec db pg_isready -U job_email_user -d job_email_db

# Check database logs
docker-compose logs db

# Connect to database directly
docker-compose exec db psql -U job_email_user -d job_email_db
```

### Import Errors

```bash
# Check Python path inside container
docker-compose exec web python -c "import sys; print('\n'.join(sys.path))"

# Test imports
docker-compose exec web python -c "from src.main import app; print('Success!')"
```

### Port Already in Use

If port 8000 or 5432 is already in use:

```bash
# Change ports in docker-compose.yml
# For API: "8001:8000" instead of "8000:8000"
# For DB: "5433:5432" instead of "5432:5432"
```

## Testing the API Endpoints

Once running, test with curl:

```bash
# Health check
curl http://localhost:8000/health

# Register user
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+1234567890",
    "name": "Test User",
    "email": "test@example.com"
  }'

# Upload resume
curl -X POST http://localhost:8000/upload-resume \
  -F "user_id=<user_id_from_registration>" \
  -F "file=@sample_resume.txt"

# Generate email
curl -X POST http://localhost:8000/gen-email \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+1234567890",
    "job_description": "We are looking for a senior software engineer..."
  }'
```

## Cleaning Up

```bash
# Remove all containers, networks, and volumes
docker-compose down -v

# Remove the built image
docker rmi job-email-api

# Remove all unused Docker resources
docker system prune -a
```

## Next Steps

Once you've verified everything works locally:

1. The same command used in the Dockerfile CMD can be used in Render
2. Update your Render service settings to match the working configuration
3. Ensure environment variables are set correctly in Render dashboard
