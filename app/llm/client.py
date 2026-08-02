from google import genai
from google.genai import types

from app.config.settings import settings
from app.models.email_summary import EmailSummary


class GeminiClient:
    """Gemini API client."""

    def __init__(self) -> None:
        self._client = genai.Client(
            api_key=settings.gemini_api_key,
        )

    def analyze_email(
        self,
        prompt: str,
    ) -> EmailSummary:
        response = self._client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=EmailSummary,
            ),
        )

        if response.parsed is None:
            raise RuntimeError("Gemini returned an empty structured response.")

        return response.parsed
