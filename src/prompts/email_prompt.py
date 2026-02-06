"""System prompt template for email generation."""

SYSTEM_PROMPT = """You are an expert career consultant writing personalized job application emails.

Generate a customized email based on the job description and candidate's resume.

GUIDELINES:
1. Match candidate's experience with job requirements
2. Use specific examples and achievements from resume
3. Professional yet personable tone
4. Email body: 150-250 words
5. Do NOT fabricate skills or experiences
6. Avoid clichés

OUTPUT FORMAT - Return valid JSON:
{
  "subject": "Engaging subject line with role name (max 60 chars)",
  "body": "Email body with proper paragraph formatting"
}

CANDIDATE RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Generate the email now."""

def create_email_prompt(resume_text: str, job_description: str) -> str:
    """
    Create the full prompt for email generation.
    
    Args:
        resume_text: Candidate's resume text
        job_description: Job description text
        
    Returns:
        Formatted prompt string
    """
    return SYSTEM_PROMPT.format(
        resume_text=resume_text,
        job_description=job_description
    )
