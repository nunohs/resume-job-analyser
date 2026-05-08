# Resume Job Analyser

An AI-powered tool that compares your resume against a job description and gives you actionable feedback — instantly.

**Live demo:** https://resume-job-analyser-pi.vercel.app

## What it does (MVP Scope)

Upload your resume as a PDF, paste a job description, and get back:

- **Match score** — a 0–100 rating of how well your resume fits the role
- **Missing keywords** — skills, tools, and qualifications from the job description that are absent or weak in your resume
- **Resume rewrite suggestions** — specific bullet point rewrites with an explanation of why each change helps
- **Cover letter draft** — a tailored cover letter you can copy and adapt

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | React 19, Vite |
| Backend | FastAPI (Python) |
| AI | Google Gemini (`gemini-3.1-flash-lite-preview`) |
| PDF parsing | pdfplumber |
| Deployment | Vercel (frontend) |

## Project structure

```
resume-job-analyser/
├── frontend/          # React + Vite app
│   └── src/
│       ├── App.jsx    # Main UI and analysis results
│       └── config.js  # API base URL config
└── backend/           # FastAPI app
    ├── main.py        # API endpoints
    ├── parser.py      # PDF text extraction
    ├── prompts.py     # Gemini prompt builder
    └── requirements.txt
```

## What This App Will Not Do (Outside of scope)
To keep the MVP focused, this version will not include:

- User accounts or login
- Saving analysis history
- Multiple resume versions
- LinkedIn scraping
- Job board scraping
- Comparing one resume against multiple jobs
- Automatic job applications
- Payment features
  
##Screenshots
<img width="1889" height="940" alt="jobanalyzerscreenshot1" src="https://github.com/user-attachments/assets/73be79cc-3718-4dbb-8529-09d00022d448" />
<img width="1888" height="943" alt="jobanalyzerscreenshot2" src="https://github.com/user-attachments/assets/0bf180d1-1bb5-4adc-a66d-81e0f7617ed3" />

## Running locally

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

Create a `.env` file in `backend/`:

```
GEMINI_API_KEY=your_key_here
```

Start the server:

```bash
uvicorn main:app --reload
```

The API runs at `http://127.0.0.1:8000`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The app runs at `http://localhost:5173`.

To point the frontend at a different backend URL, set `VITE_API_BASE_URL` in a `.env` file inside `frontend/`:

```
VITE_API_BASE_URL=https://your-backend-url.com
```

## API

### `POST /analyse`

Accepts `multipart/form-data`:

| Field | Type | Description |
|---|---|---|
| `resume` | File (PDF) | The candidate's resume |
| `job_description` | string | The job description text |

Returns:

```json
{
  "match_score": 72,
  "missing_keywords": ["TypeScript", "CI/CD", "Agile"],
  "suggested_resume_rewrites": [
    {
      "original_issue": "...",
      "suggested_rewrite": "...",
      "reason": "..."
    }
  ],
  "cover_letter_draft": "Dear Hiring Manager, ..."
}
```

## Built by

Hadi Nuno Handrison

