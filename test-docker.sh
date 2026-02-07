#!/bin/bash
# Test Docker build and imports

echo "=================================="
echo "Docker Build Test Script"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Build the Docker image
echo "${YELLOW}Step 1: Building Docker image...${NC}"
if docker build -t job-email-api . ; then
    echo "${GREEN}✓ Docker build successful${NC}"
    echo ""
else
    echo "${RED}✗ Docker build failed${NC}"
    exit 1
fi

# Step 2: Test Python imports
echo "${YELLOW}Step 2: Testing Python imports...${NC}"
if docker run --rm job-email-api python -c "
import sys
print('Python version:', sys.version)
print('Python path:', sys.path)
print('')
print('Testing imports...')
from src.main import app
print('✓ src.main imported successfully')
from src.models.user import User
print('✓ src.models.user imported successfully')
from src.services.user_service import register_user
print('✓ src.services.user_service imported successfully')
from src.lib.postgres import get_db
print('✓ src.lib.postgres imported successfully')
print('')
print('All imports successful!')
" ; then
    echo "${GREEN}✓ All imports working${NC}"
    echo ""
else
    echo "${RED}✗ Import test failed${NC}"
    exit 1
fi

# Step 3: Check uvicorn can load the app
echo "${YELLOW}Step 3: Testing uvicorn app loading...${NC}"
if docker run --rm job-email-api python -c "
from uvicorn.importer import import_from_string
app = import_from_string('src.main:app')
print('✓ Uvicorn can load the app')
print(f'✓ App type: {type(app)}')
" ; then
    echo "${GREEN}✓ Uvicorn can load the app${NC}"
    echo ""
else
    echo "${RED}✗ Uvicorn app loading failed${NC}"
    exit 1
fi

# Step 4: List installed packages
echo "${YELLOW}Step 4: Installed packages:${NC}"
docker run --rm job-email-api pip list | head -20

echo ""
echo "${GREEN}=================================="
echo "All tests passed! ✓"
echo "==================================${NC}"
echo ""
echo "To run the full application with database:"
echo "  1. Add your OPENAI_API_KEY to .env file"
echo "  2. Run: docker-compose up"
echo ""
echo "To test just the API container:"
echo "  docker run -p 8000:8000 -e DATABASE_URL=<url> -e OPENAI_API_KEY=<key> job-email-api"
echo ""
