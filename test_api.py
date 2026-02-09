"""Test script for Job Email Generator API."""
import requests
import json
import os
from pathlib import Path

BASE_URL = "http://localhost:8000"

# Test data
# Test data
test_username = "johndoe123"
test_user_id = None  # Will be set after registration

test_resume = """
John Doe
Software Engineer

EXPERIENCE:
- 5+ years of Python development experience
- Built RESTful APIs using FastAPI and Flask
- Experienced with PostgreSQL and MongoDB databases
- Implemented microservices architecture for scalable applications
- Led a team of 3 developers on a major project that increased system performance by 40%

SKILLS:
- Python, JavaScript, SQL
- FastAPI, Django, React
- Docker, Kubernetes, AWS
- PostgreSQL, Redis, pgvector

EDUCATION:
- Bachelor's in Computer Science, XYZ University
"""

test_job_description = """
Backend Engineer Position

We're looking for an experienced Backend Engineer to join our team.

Requirements:
- 3+ years of Python development
- Experience with FastAPI or similar frameworks
- Strong knowledge of SQL databases
- Experience with cloud platforms (AWS/GCP)
- Ability to work in an agile team environment

Responsibilities:
- Design and implement RESTful APIs
- Optimize database queries and system performance
- Collaborate with frontend team on API contracts
- Write clean, maintainable code with proper documentation
"""

def test_health_check():
    """Test health check endpoint."""
    print("\n1. Testing health check...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200

def test_register():
    """Test user registration."""
    global test_user_id
    print("\n2. Testing user registration...")
    response = requests.post(
        f"{BASE_URL}/register",
        json={
            "username": test_username
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 400 and "already exists" in response.json().get("detail", ""):
        print("User already exists, continuing with existing user...")
        # For existing users, we'll need to get the user_id from a previous run
        # In a real test, you'd query the user by phone or use a known ID
        print("Note: Please use the user_id from previous registration for file upload test")
        return True
    
    assert response.status_code == 200
    assert "user_id" in response.json()
    test_user_id = response.json()["user_id"]
    print(f"User ID: {test_user_id}")
    return True

def test_upload_resume():
    """Test resume upload with file."""
    global test_user_id
    print("\n3. Testing resume upload...")
    
    if not test_user_id:
        print("Warning: user_id not available from registration, using sample resume.txt file test")
        # For this test, we'll use the sample_resume.txt file
        print("Skipping file upload test - please provide user_id manually or register first")
        return
    
    # Check if sample_resume.txt exists
    resume_file_path = Path("sample_resume.txt")
    if not resume_file_path.exists():
        print(f"Creating temporary resume file for testing...")
        with open("temp_resume.txt", "w") as f:
            f.write(test_resume)
        resume_file_path = Path("temp_resume.txt")
    
    # Upload file
    with open(resume_file_path, "rb") as f:
        files = {"file": (resume_file_path.name, f, "text/plain")}
        data = {"user_id": test_user_id}
        response = requests.post(
            f"{BASE_URL}/upload-resume",
            files=files,
            data=data
        )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Clean up temp file if created
    if Path("temp_resume.txt").exists():
        os.remove("temp_resume.txt")
    
    assert response.status_code == 200
    result = response.json()
    assert result["message"] == "success"
    assert "filename" in result
    assert "extracted_length" in result
    print(f"✓ Uploaded {result['filename']} ({result['extracted_length']} chars extracted)")

def test_generate_email():
    """Test email generation."""
    print("\n4. Testing email generation...")
    response = requests.post(
        f"{BASE_URL}/gen-email",
        json={
            "username": test_username,
            "job_description": test_job_description
        }
    )
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nGenerated Email:")
        print(f"Subject: {result['subject']}")
        print(f"\nBody:\n{result['body']}")
        
        # Validate response
        assert "subject" in result
        assert "body" in result
        assert len(result["subject"]) > 0
        assert len(result["body"]) > 0
        print("\n✓ Email generation successful!")
    else:
        print(f"Error: {response.json()}")
        raise Exception(f"Email generation failed with status {response.status_code}")

def run_all_tests():
    """Run all tests in sequence."""
    print("=" * 60)
    print("Starting API Tests...")
    print("=" * 60)
    
    try:
        test_health_check()
        test_register()
        test_upload_resume()
        test_generate_email()
        
        print("\n" + "=" * 60)
        print("✓ All tests passed successfully!")
        print("=" * 60)
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"✗ Test failed: {str(e)}")
        print("=" * 60)
        raise

if __name__ == "__main__":
    run_all_tests()
