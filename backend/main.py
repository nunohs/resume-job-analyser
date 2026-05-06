from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from parser import extract_text_from_pdf

app = FastAPI()

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

        return {
            "status": "received",
            "resume_filename": resume.filename,
            "resume_text_preview": resume_text[:500],
            "job_description_preview": job_description[:500]
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
