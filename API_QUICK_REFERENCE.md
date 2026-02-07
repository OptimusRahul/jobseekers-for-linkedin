# API Quick Reference

Quick reference card for the Job Email Generator API.

## 🔗 Base URL

```
http://127.0.0.1:8000
```

## 📡 Endpoints

### 1️⃣ Health Check
```http
GET /
```

**Response:**
```json
{
    "status": "healthy",
    "message": "Job Email Generator API"
}
```

---

### 2️⃣ Register User
```http
POST /register
Content-Type: application/json

{
    "phone_number": "+1234567890",
    "name": "John Doe",
    "email": "john.doe@example.com"
}
```

**Response:**
```json
{
    "user_id": "uuid-here"
}
```

---

### 3️⃣ Upload Resume
```http
POST /upload-resume
Content-Type: multipart/form-data

Form Data:
- user_id: <user_id_from_registration>
- file: <resume_file.pdf|docx|txt>
```

**Supported Formats:** PDF, DOCX, DOC, TXT (max 10MB)

**Response:**
```json
{
    "message": "success",
    "user_id": "uuid-here",
    "filename": "resume.pdf",
    "extracted_length": 1245
}
```

---

### 4️⃣ Generate Email
```http
POST /gen-email
Content-Type: application/json

{
    "phone_number": "+1234567890",
    "job_description": "Job description here..."
}
```

**Response:**
```json
{
    "subject": "Application for...",
    "body": "Dear Hiring Manager,..."
}
```

---

## 📋 Workflow

```
1. Register User      → Get user_id
2. Upload Resume      → Store embeddings
3. Generate Email     → Get personalized email
```

## 🧪 Testing

### cURL Examples

**Health Check:**
```bash
curl http://127.0.0.1:8000/
```

**Register:**
```bash
curl -X POST http://127.0.0.1:8000/register \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+1234567890",
    "name": "John Doe",
    "email": "john@example.com"
  }'
```

**Upload Resume:**
```bash
curl -X POST http://127.0.0.1:8000/upload-resume \
  -F "user_id=a1b2c3d4-e5f6-7890-abcd-ef1234567890" \
  -F "file=@/path/to/resume.pdf"
```

**Generate Email:**
```bash
curl -X POST http://127.0.0.1:8000/gen-email \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+1234567890",
    "job_description": "We are hiring a Senior Backend Engineer..."
  }'
```

---

## ❌ Common Errors

| Code | Message | Solution |
|------|---------|----------|
| 400 | "Phone number already exists" | Use different phone number |
| 400 | "Invalid user_id format" | Provide valid UUID |
| 400 | "Unsupported file format" | Use PDF, DOCX, or TXT |
| 400 | "File size exceeds limit" | Use file smaller than 10MB |
| 404 | "User not found" | Register user first / Check user_id |
| 500 | "OpenAI API error" | Check OPENAI_API_KEY in .env |
| 500 | "Database error" | Run `make migrate-up` |

---

## 🔑 Required Headers

All POST requests:
```
Content-Type: application/json
```

---

## ⚡ Response Times

| Endpoint | Typical Time |
|----------|-------------|
| `/` | < 10ms |
| `/register` | 50-100ms |
| `/upload-resume` | 2-5 seconds (file parsing + OpenAI embedding) |
| `/gen-email` | 5-10 seconds (OpenAI GPT) |

---

## 🎯 Postman Collection

Import these files into Postman:
- `Job_Email_Generator.postman_collection.json`
- `Job_Email_Generator.postman_environment.json`

See [POSTMAN_GUIDE.md](POSTMAN_GUIDE.md) for details.

---

## 📚 Full Documentation

- [README.md](README.md) - Complete setup guide
- [POSTMAN_GUIDE.md](POSTMAN_GUIDE.md) - Postman usage
- API Docs: http://127.0.0.1:8000/docs (when server is running)

---

**Quick Start:**
```bash
make migrate-up && make run
```
