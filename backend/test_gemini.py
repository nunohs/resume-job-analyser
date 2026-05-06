import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ClientError

load_dotenv(Path(__file__).with_name(".env"))

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found. Check your backend/.env file.")

client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Say hello in one short sentence.",
    )
except ClientError as exc:
    if exc.code == 429:
        raise SystemExit(
            "Gemini API quota/rate limit reached for this API key.\n"
            "Check your Google AI Studio quota/billing, wait for the retry window, "
            "or try a different Gemini model/key."
        ) from exc

    raise SystemExit(f"Gemini API request failed: {exc.code} {exc.status}. {exc.message}") from exc

print(response.text)
