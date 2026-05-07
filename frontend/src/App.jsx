import { useState } from "react";
import "./App.css";
import API_BASE_URL from "./config";

function App() {
  const [jobDescription, setJobDescription] = useState("");
  const [resumeFile, setResumeFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const isFormReady = jobDescription.trim() !== "" && resumeFile !== null;

  const handleAnalyse = async () => {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const formData = new FormData();

      formData.append("resume", resumeFile);
      formData.append("job_description", jobDescription);

      const response = await fetch(`${API_BASE_URL}/analyse`, {
        method: "POST",
        body: formData,
      });
      const data = await response.json();

      console.log("API response:", data);

      if (!response.ok) {
        throw new Error(data.detail || "Something went wrong.");
      }

      setResult(data);
    } catch (err) {
      console.error(err);
      setError(err.message || "Failed to analyse resume. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const getScoreClass = (score) => {
    if (score >= 75) return "score-green";
    if (score >= 50) return "score-yellow";
    return "score-red";
  };

  const handleStartOver = () => {
    setJobDescription("");
    setResumeFile(null);
    setResult(null);
    setError("");
  };

  const handleCopyCoverLetter = async () => {
    if (!result?.cover_letter_draft) return;

    try {
      await navigator.clipboard.writeText(result.cover_letter_draft);
      alert("Cover letter copied!");
    } catch {
      alert("Could not copy cover letter.");
    }
  };
  
 return (
  <main className="app-container">
    <section className="hero-section">
      <p className="eyebrow">AI Resume Match Analyser</p>
      <h1>Check how well your resume matches a job description</h1>
      <p className="hero-text">
        Upload your resume PDF, paste a job description, and get a structured
        analysis powered by Gemini.
      </p>
    </section>

    {!result ? (
      <section className="input-card">
        <div className="form-grid">
          <div className="form-section">
            <label htmlFor="jobDescription">Job Description</label>
            <textarea
              id="jobDescription"
              placeholder="Paste the job description here..."
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
            />
          </div>

          <div className="form-section">
            <label htmlFor="resume">Resume PDF</label>

            <div className="upload-box">
              <input
                id="resume"
                type="file"
                accept="application/pdf"
                onChange={(e) => setResumeFile(e.target.files[0])}
              />

              {resumeFile ? (
                <p className="file-name">{resumeFile.name}</p>
              ) : (
                <p className="upload-help">Choose a PDF resume to analyse.</p>
              )}
            </div>
          </div>
        </div>

        <button
          className="analyse-button"
          onClick={handleAnalyse}
          disabled={!isFormReady || loading}
        >
          {loading ? "Analysing..." : "Analyse"}
        </button>

        {loading && (
          <p className="loading-message">
            Gemini is analysing your resume. This may take a few seconds.
          </p>
        )}

        {error && <p className="error-message">{error}</p>}
      </section>
    ) : (
      <section className="results-card">
        <div className="results-header">
          <div>
            <p className="eyebrow">Analysis Result</p>
            <h2>Resume Match Score</h2>
          </div>

          <div className={`score-circle ${getScoreClass(result.match_score)}`}>
            {result.match_score}
          </div>
        </div>

        <div className="result-section">
          <h3>Missing Keywords</h3>

          <div className="keyword-list">
            {result.missing_keywords?.length > 0 ? (
              result.missing_keywords.map((keyword, index) => (
                <span className="keyword-chip" key={index}>
                  {keyword}
                </span>
              ))
            ) : (
              <p>No major missing keywords found.</p>
            )}
          </div>
        </div>

        <div className="result-section">
          <h3>Suggested Resume Rewrites</h3>

          <div className="rewrite-list">
            {result.suggested_resume_rewrites?.map((item, index) => (
              <div className="rewrite-card" key={index}>
                <p>
                  <strong>Issue:</strong> {item.original_issue}
                </p>
                <p>
                  <strong>Suggested rewrite:</strong> {item.suggested_rewrite}
                </p>
                <p>
                  <strong>Why it helps:</strong> {item.reason}
                </p>
              </div>
            ))}
          </div>
        </div>

        <div className="result-section">
          <div className="cover-letter-header">
            <h3>Cover Letter Draft</h3>
            <button className="copy-button" onClick={handleCopyCoverLetter}>
              Copy
            </button>
          </div>

          <textarea
            className="cover-letter-box"
            value={result.cover_letter_draft}
            readOnly
          />
        </div>

        <button className="start-over-button" onClick={handleStartOver}>
          Start Over
        </button>
      </section>
    )}

    <footer>Built by Hadi Nuno Handrison</footer>
  </main>
);
}

export default App;