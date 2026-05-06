def build_analysis_prompt(resume_text: str, job_description: str) -> str:
    """
    Builds the prompt sent to Gemini for resume-job analysis.
    """

    return f"""
You are an expert resume analyst and career coach.

Your task is to compare the candidate's resume against the job description.

Analyse the resume carefully and return a structured JSON response with these sections:

1. match_score
- A number from 0 to 100.
- 100 means the resume is an extremely strong match.
- 0 means the resume is completely unrelated.

2. missing_keywords
- A list of important skills, tools, qualifications, or phrases from the job description that are missing or weak in the resume.

3. suggested_resume_rewrites
- A list of specific bullet point rewrite suggestions.
- Each suggestion should improve alignment with the job description.
- Keep the suggestions realistic. Do not invent fake experience.

4. cover_letter_draft
- A short, professional cover letter draft tailored to the job.

Important rules:
- Do not invent experience, employers, certifications, or technical skills that are not supported by the resume.
- If a skill is implied but not clearly stated, say it should be made clearer.
- Keep the tone professional and suitable for job applications.
- Return only valid JSON.

Resume:
\"\"\"
{resume_text}
\"\"\"

Job Description:
\"\"\"
{job_description}
\"\"\"
"""