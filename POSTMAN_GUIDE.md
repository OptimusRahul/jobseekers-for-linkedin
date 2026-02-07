# Postman Collection Guide

This guide explains how to use the Postman collection to test the Job Email Generator API.

## 📦 Files Included

- `Job_Email_Generator.postman_collection.json` - Complete API collection
- `Job_Email_Generator.postman_environment.json` - Environment variables (Local)

## 🚀 Quick Start

### 1. Import into Postman

**Option A: Via Postman App**
1. Open Postman Desktop App
2. Click **Import** (top left)
3. Drag and drop both JSON files
4. Click **Import**

**Option B: Via File Menu**
1. File → Import
2. Select both files:
   - `Job_Email_Generator.postman_collection.json`
   - `Job_Email_Generator.postman_environment.json`
3. Click Open

### 2. Select Environment

1. Click the environment dropdown (top right)
2. Select **"Job Email Generator - Local"**
3. Verify `base_url` is set to `http://127.0.0.1:8000`

### 3. Start the Server

```bash
# Make sure your server is running
make run

# Or
uv run uvicorn src.main:app --reload
```

### 4. Run Requests

Execute requests in this order for the complete flow:

1. **Health Check** - Verify API is running
2. **Register User** - Create a new user account
3. **Upload Resume** - Upload resume text and generate embeddings
4. **Generate Email** - Create personalized job application email

## 📋 API Endpoints

### 1. Health Check
```
GET /
```

**Description:** Verify the API is running

**Response:**
```json
{
    "status": "healthy",
    "message": "Job Email Generator API"
}
```

---

### 2. Register User
```
POST /register
```

**Description:** Register a new user with phone number, name, and email

**Request Body:**
```json
{
    "phone_number": "+1234567890",
    "name": "John Doe",
    "email": "john.doe@example.com"
}
```

**Response:**
```json
{
    "user_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

**Notes:**
- Phone number must be unique
- The `user_id` is automatically saved to environment variables

---

### 3. Upload Resume
```
POST /upload-resume
Content-Type: multipart/form-data
```

**Description:** Upload resume file. The system extracts text, generates vector embeddings using OpenAI, and stores them in PostgreSQL.

**Request (Form Data):**
- `user_id` (text): User ID from registration
- `file` (file): Resume file

**Supported Formats:**
- PDF (.pdf)
- Word (.docx, .doc)
- Text (.txt)

**Max File Size:** 10MB

**Response:**
```json
{
    "message": "success",
    "user_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "filename": "resume.pdf",
    "extracted_length": 1245
}
```

**Notes:**
- User must be registered first (use `user_id` from registration response)
- File text is automatically extracted based on format
- Resume text is converted to embeddings using OpenAI `text-embedding-3-small`
- Embeddings are stored in PostgreSQL with pgvector for similarity search

---

### 4. Generate Email
```
POST /gen-email
```

**Description:** Generate a personalized job application email based on the user's resume and job description using AI.

**Request Body:**
```json
{
    "phone_number": "+1234567890",
    "job_description": "Senior Backend Engineer\n\nWe are looking for..."
}
```

**Response:**
```json
{
    "subject": "Application for Senior Backend Engineer Position",
    "body": "Dear Hiring Manager,\n\nI am writing to express..."
}
```

**Notes:**
- User must have uploaded a resume first
- Uses OpenAI GPT-4o-mini to generate personalized content
- Matches relevant resume experience to job requirements

---

## 🧪 Testing Workflow

### Complete Flow Test

1. **Start Fresh**
   ```bash
   # Reset database if needed
   make migrate-down
   make migrate-up
   ```

2. **Run Health Check**
   - Execute "Health Check" request
   - Verify status: 200 OK
   - Confirm response has `"status": "healthy"`

3. **Register User**
   - Execute "Register User" request
   - Copy the returned `user_id`
   - It's auto-saved to environment variables

4. **Upload Resume**
   - Click on "Upload Resume" request
   - In the Body tab, ensure form-data is selected
   - The `user_id` field should auto-populate from environment
   - Click "Select Files" for the `file` field
   - Choose a resume file (PDF, DOCX, or TXT)
   - Execute the request
   - Wait ~2-5 seconds (file parsing + OpenAI embedding generation)
   - Verify response contains `"message": "success"` and `extracted_length`

5. **Generate Email**
   - Execute "Generate Email" request
   - Wait ~5-10 seconds (OpenAI GPT generation)
   - Review the generated `subject` and `body`

### Using Different Phone Numbers

To test multiple users:

1. Change `phone_number` in environment variables
2. Register new user
3. Upload resume for that user
4. Generate email for that user

---

## 🔧 Environment Variables

The environment includes:

| Variable | Default Value | Description |
|----------|---------------|-------------|
| `base_url` | `http://127.0.0.1:8000` | API base URL |
| `user_id` | (empty) | Auto-populated after registration |
| `phone_number` | `+1234567890` | Default test phone number |

### Modify Environment

1. Click the eye icon (👁️) next to environment dropdown
2. Click **Edit** on "Job Email Generator - Local"
3. Modify values as needed
4. Click **Save**

---

## 📊 Automated Tests

The collection includes automated tests for each endpoint:

### Health Check Tests
- ✅ Status code is 200
- ✅ Response has `status` field
- ✅ Status equals "healthy"

### Register User Tests
- ✅ Status code is 200
- ✅ Response contains `user_id`
- ✅ Auto-saves `user_id` to environment

### Upload Resume Tests
- ✅ Status code is 200
- ✅ Response message is "success"

### Generate Email Tests
- ✅ Status code is 200
- ✅ Response contains `subject` and `body`
- ✅ Both fields are non-empty

### View Test Results

After running a request:
1. Click **Test Results** tab (bottom)
2. See passed/failed tests
3. View execution time

---

## 🎯 Sample Data

### Sample Resume File

A sample resume file is included in the project:
- `sample_resume.txt` - Use this for testing the file upload

**To use in Postman:**
1. Select the "Upload Resume" request
2. Go to the Body tab
3. Click "Select Files" for the `file` field
4. Navigate to the project directory and select `sample_resume.txt`
5. Send the request

You can also test with your own PDF or DOCX files (max 10MB).

### Sample Job Description

```
Senior Backend Engineer

We are looking for an experienced backend engineer to join our fast-growing startup.

Responsibilities:
- Design and develop scalable RESTful APIs using Python
- Build microservices architecture
- Optimize database performance and queries
- Implement CI/CD pipelines
- Mentor junior developers
- Collaborate with frontend team

Requirements:
- 5+ years of Python development experience
- Strong knowledge of FastAPI, Django, or Flask
- Experience with PostgreSQL and Redis
- Docker and Kubernetes expertise
- AWS cloud experience
- Strong problem-solving skills

Nice to Have:
- Experience with vector databases
- Machine learning background
- Open source contributions

We Offer:
- Competitive salary ($120k-$180k)
- Remote work flexibility
- Health insurance
- Stock options
- Continuous learning budget
```

---

## 🚨 Troubleshooting

### Connection Refused

**Error:** `Could not get any response`

**Fix:**
```bash
# Make sure server is running
make run

# Verify server is listening
curl http://127.0.0.1:8000/
```

### User Not Found (404)

**Error:** `User not found` when uploading resume

**Fix:**
1. Register user first using "Register User" request
2. Make sure `phone_number` matches in both requests
3. Check environment variables

### OpenAI API Error

**Error:** `OpenAI API call failed`

**Fix:**
```bash
# Check .env file has valid OpenAI key
cat .env

# Verify key is set
OPENAI_API_KEY=sk-...
```

### Database Connection Error

**Error:** `Connection refused` or `Database error`

**Fix:**
```bash
# Run migrations
make migrate-up

# Verify PostgreSQL is running
psql -h localhost -U postgres -l

# Check DATABASE_URL in .env
```

---

## 🔄 Runner Collection

Run all requests sequentially:

1. Click **Collections** (left sidebar)
2. Click **"..."** next to "Job Email Generator API"
3. Click **Run collection**
4. Click **Run Job Email Generator API**
5. Watch tests execute automatically

---

## 📝 Tips

### Quick Testing
- Use **Cmd/Ctrl + Enter** to send requests quickly
- Enable **Auto-follow redirects** in settings
- Save responses as examples for documentation

### Environment Management
- Create separate environments for:
  - Local (`http://127.0.0.1:8000`)
  - Staging (`https://staging.yourapp.com`)
  - Production (`https://api.yourapp.com`)

### Variables Usage
- Use `{{variable}}` syntax in requests
- Reference in URL: `{{base_url}}/register`
- Reference in body: `"phone": "{{phone_number}}"`

### Debugging
- Open Postman Console (View → Show Postman Console)
- See raw request/response details
- View headers, body, and timing

---

## 📚 Additional Resources

- [Postman Documentation](https://learning.postman.com/docs/)
- [API Documentation](../README.md)
- [Project Setup](../README.md#installation)

---

## 🎉 Ready to Test!

Your Postman collection is ready. Start with:

```bash
# 1. Start server
make run

# 2. Open Postman
# 3. Select "Job Email Generator - Local" environment
# 4. Run "Health Check" request
# 5. Follow the workflow above
```

Happy testing! 🚀
