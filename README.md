# AI Resume + Job Match Analyser

A full-stack web app that analyses a user's resume against a job description and provides an AI-powered match score, strengths, gaps, and improvement suggestions.

## MVP Scope

The AI Resume + Job Match Analyser is a simple full-stack web app that helps users compare their resume against a specific job description.

The MVP flow is:

1. User uploads a resume PDF.
2. User pastes a job description.
3. User clicks an analyse button.
4. The app extracts text from the resume.
5. The app compares the resume against the job description using an LLM.
6. The app returns:
   - A match score
   - Missing keywords or skills
   - Resume rewrite suggestions
   - A simple cover letter draft

## What This App Will Not Do

To keep the MVP focused, this version will not include:

- User accounts or login
- Saving analysis history
- Multiple resume versions
- LinkedIn scraping
- Job board scraping
- Comparing one resume against multiple jobs
- Automatic job applications
- Payment features

The goal is to keep the project focused on one clear flow:

```txt
Resume PDF + Job Description → AI Analysis → Job Match Report

## Tech Stack

### Frontend
- React
- Vite

### Backend
- Python
- FastAPI
- Uvicorn
- pdfplumber
- Gemini API
- python-dotenv

## Project Structure

```txt
resume-job-analyser/
├── frontend/
├── backend/
└── README.md

