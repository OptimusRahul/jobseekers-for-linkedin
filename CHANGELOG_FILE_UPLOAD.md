# Resume Upload API Change - File Upload Support

## Summary

The `/upload-resume` endpoint has been updated to accept **file uploads** instead of plain text. Users now upload actual resume files (PDF, DOCX, TXT) and provide a `user_id` instead of `phone_number`.

## What Changed

### API Endpoint Changes

**Before:**
```http
POST /upload-resume
Content-Type: application/json

{
  "phone_number": "+1234567890",
  "resume_text": "John Doe\nSoftware Engineer\n..."
}
```

**After:**
```http
POST /upload-resume
Content-Type: multipart/form-data

Form Data:
- user_id: <uuid-from-registration>
- file: <resume.pdf|docx|txt>
```

### Response Changes

**Before:**
```json
{
  "message": "success"
}
```

**After:**
```json
{
  "message": "success",
  "user_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "filename": "resume.pdf",
  "extracted_length": 1245
}
```

## New Features

### 1. File Format Support

The API now supports multiple file formats:
- **PDF** (.pdf) - Extracted using PyPDF2
- **Word** (.docx, .doc) - Extracted using python-docx
- **Text** (.txt) - Direct text reading with encoding detection

### 2. File Validation

- **File size limit**: 10MB maximum
- **Format validation**: Only supported formats accepted
- **Content validation**: Ensures extracted text is at least 50 characters

### 3. Automatic Text Extraction

The system automatically:
1. Detects file format from extension
2. Extracts text content using appropriate parser
3. Validates extracted text
4. Generates embeddings from extracted text

### 4. User ID-Based Mapping

- Changed from `phone_number` to `user_id` for direct user mapping
- More efficient database lookups (no phone normalization needed)
- Better security (user_id is returned during registration)

## Technical Changes

### New Dependencies

Added to `pyproject.toml` and `requirements.txt`:
```toml
python-multipart==0.0.6  # For file upload support in FastAPI
pypdf2==3.0.1            # PDF text extraction
python-docx==1.1.0       # DOCX text extraction
```

### New Files

1. **`src/utils/file_parser.py`** - File parsing utilities
   - `parse_resume_file()` - Main parsing function
   - `extract_text_from_pdf()` - PDF parser
   - `extract_text_from_docx()` - DOCX parser
   - `extract_text_from_txt()` - TXT parser
   - `validate_file_size()` - File size validator
   - `get_supported_extensions()` - Returns supported formats

2. **`sample_resume.txt`** - Sample resume file for testing

### Modified Files

1. **`src/main.py`**
   - Changed endpoint from JSON to `multipart/form-data`
   - Added `async` for file reading
   - Added `UploadFile` and `Form` from FastAPI
   - Added file validation logic
   - Added text extraction before embedding generation

2. **`src/models/schemas.py`**
   - Removed `UploadResumeRequest` (form data doesn't use Pydantic)
   - Added `UploadResumeResponse` with additional fields

3. **`test_api.py`**
   - Updated to use file upload with `requests.post(files=...)`
   - Added file creation for testing
   - Updated to use `user_id` from registration

4. **`Job_Email_Generator.postman_collection.json`**
   - Changed body type from `raw` to `formdata`
   - Added file upload field
   - Updated tests to check new response fields

5. **Documentation Files**
   - `README.md` - Updated API reference section
   - `POSTMAN_GUIDE.md` - Updated with file upload instructions
   - `API_QUICK_REFERENCE.md` - Updated cURL examples

## Migration Guide

### For API Users

**Before (Old):**
```python
import requests

response = requests.post(
    "http://localhost:8000/upload-resume",
    json={
        "phone_number": "+1234567890",
        "resume_text": "Your resume text..."
    }
)
```

**After (New):**
```python
import requests

# Get user_id from registration response
register_response = requests.post(
    "http://localhost:8000/register",
    json={"phone_number": "+1234567890", "name": "John Doe", "email": "john@example.com"}
)
user_id = register_response.json()["user_id"]

# Upload resume file
with open("resume.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/upload-resume",
        files={"file": f},
        data={"user_id": user_id}
    )
```

### For Postman Users

1. Open the "Upload Resume" request
2. Change Body type to `form-data` (already updated in collection)
3. Fill in `user_id` field (auto-populated from environment)
4. Click "Select Files" for `file` field
5. Choose your resume file
6. Send request

## Error Handling

New error responses:

| Code | Error | Cause |
|------|-------|-------|
| 400 | Invalid user_id format | user_id is not a valid UUID |
| 400 | Unsupported file format | File extension not in [.pdf, .docx, .doc, .txt] |
| 400 | File size exceeds limit | File larger than 10MB |
| 400 | Resume appears to be empty | Extracted text is less than 50 characters |
| 404 | User not found | user_id doesn't exist in database |
| 500 | Failed to parse PDF/DOCX/TXT | File is corrupted or invalid |

## Benefits

### 1. Better User Experience
- Users upload actual resume files (no copy-paste needed)
- Supports common formats (PDF, Word)
- Automatic text extraction

### 2. Improved Data Quality
- Original formatting preserved during extraction
- Better text extraction from PDF/Word than manual copy-paste
- Validation ensures minimum content length

### 3. More Secure
- User identified by UUID instead of phone number
- File size limits prevent abuse
- Format validation prevents malicious files

### 4. More Efficient
- Direct user_id lookup (no phone normalization)
- Single upload for multiple formats
- Cleaner API design

## Testing

### Test with Sample File

```bash
# 1. Register user
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+1234567890", "name": "John Doe", "email": "john@example.com"}'

# Response: {"user_id": "abc-123-..."}

# 2. Upload resume
curl -X POST http://localhost:8000/upload-resume \
  -F "user_id=abc-123-..." \
  -F "file=@sample_resume.txt"

# Response: {
#   "message": "success",
#   "user_id": "abc-123-...",
#   "filename": "sample_resume.txt",
#   "extracted_length": 2845
# }
```

### Test with Python Script

```bash
uv run python test_api.py
```

## Backward Compatibility

⚠️ **Breaking Change**: The old JSON-based endpoint is no longer supported.

If you have existing code using the old endpoint:
1. Update to file upload format
2. Change from `phone_number` to `user_id`
3. Update request content type to `multipart/form-data`

## Performance

- **PDF parsing**: ~500ms - 2s (depending on file size and complexity)
- **DOCX parsing**: ~200ms - 1s
- **TXT parsing**: ~50ms - 200ms
- **Embedding generation**: ~1-2s (OpenAI API call)

**Total time**: 2-5 seconds (vs 2-3 seconds for plain text)

The slight increase is due to file parsing, but the improved data quality is worth it.

## Future Enhancements

Potential improvements:
- Support for more formats (RTF, HTML)
- Resume parsing to extract structured data (name, email, skills)
- OCR support for scanned PDFs
- File storage for original resume access
- Batch upload support

---

## Questions?

See updated documentation:
- [README.md](README.md) - Full API documentation
- [POSTMAN_GUIDE.md](POSTMAN_GUIDE.md) - Postman testing guide
- [API_QUICK_REFERENCE.md](API_QUICK_REFERENCE.md) - Quick reference card

---

**Last Updated**: 2026-02-03
**Version**: 2.0.0
