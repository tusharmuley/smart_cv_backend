import json

from google import genai

from app.ai.prompts import ANALYZE_RESUME_PROMPT
from app.core.config import settings


client = genai.Client(
    api_key=settings.GOOGLE_API_KEY
)


class GeminiService:

    @staticmethod
    def analyze_resume(
        resume_text: str,
        job_description: str,
    ):

        prompt = ANALYZE_RESUME_PROMPT.format(
            resume=resume_text,
            job_description=job_description,
        )

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        return json.loads(response.text)