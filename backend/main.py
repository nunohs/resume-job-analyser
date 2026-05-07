import os
import json
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from google import genai
from google.genai import types
from pydantic import BaseModel
from google.genai.errors import ServerError, ClientError

from fastapi.middleware.cors import CORSMiddleware

from parser import extract_text_from_pdf
from prompts import build_analysis_prompt


load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing. Add it to your .env file.")

client = genai.Client(api_key=GEMINI_API_KEY)


class ResumeRewriteSuggestion(BaseModel):
    original_issue: str
    suggested_rewrite: str
    reason: str


class ResumeAnalysisResponse(BaseModel):
    match_score: int
    missing_keywords: List[str]
    suggested_resume_rewrites: List[ResumeRewriteSuggestion]
    cover_letter_draft: str

@app.get("/")
def read_root():
    return {"message": "Resume Job Analyser backend is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/analyse")
async def analyse_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    try:
        resume_text = extract_text_from_pdf(resume)

        prompt = build_analysis_prompt(
            resume_text=resume_text,
            job_description=job_description
        )

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ResumeAnalysisResponse,
            ),
        )

        analysis = json.loads(response.text)

        return analysis

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Gemini returned an unexpected response format. Please try again."
        )

    except ServerError as e:
        raise HTTPException(
        status_code=503,
        detail="Gemini is currently experiencing high demand. Please wait a minute and try again."
    )

    except ClientError as e:
        raise HTTPException(
            status_code=429,
            detail="Gemini API quota or request limit reached. Please check your Gemini usage or try again later."
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Something went wrong while analysing the resume: {str(e)}"
        )