import os
from typing import Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()


class GeminiConfigurationError(RuntimeError):
    """Raised when Gemini cannot be configured."""


class GeminiGenerationError(RuntimeError):
    """Raised when Gemini fails to generate content."""


class GeminiDocumentGenerator:
    """
    Generates structured legal-document drafts using Google Gemini.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

        self.model = model or os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash",
        )

        if not self.api_key:
            raise GeminiConfigurationError(
                "GEMINI_API_KEY is not configured. "
                "Add it to your .env file."
            )

        self.client = genai.Client(
            api_key=self.api_key
        )

    @staticmethod
    def _build_prompt(
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
        jurisdiction: str = "",
        special_instructions: str = "",
    ) -> str:

        jurisdiction_text = (
            jurisdiction
            if jurisdiction
            else "Not specified"
        )

        instructions_text = (
            special_instructions
            if special_instructions
            else "None"
        )

        prompt = f"""
You are LegalEase's legal-document drafting assistant.

Create a professional DRAFT of a {document_type}.

USER-PROVIDED FACTS

Document type:
{document_type}

Parties:
{parties}

Effective date:
{effective_date}

Jurisdiction:
{jurisdiction_text}

Terms and conditions:
{terms}

Special instructions:
{instructions_text}

OUTPUT REQUIREMENTS

1. Produce only the document draft.

2. Do not include an AI preamble.

3. Do not invent names, dates, addresses, prices,
laws, statutes, or other facts.

4. If information is missing, use a clear placeholder
such as:

[ADDRESS NOT PROVIDED]

5. Use clear headings and numbered sections.

6. Include appropriate sections such as:

- Title
- Parties
- Effective Date
- Definitions
- Purpose
- Obligations
- Payment terms where applicable
- Confidentiality where applicable
- Term and termination where applicable
- Dispute resolution where appropriate
- Governing law only when jurisdiction is supplied
- Notices where appropriate
- Entire agreement
- Amendments
- Severability
- Signature blocks

7. Preserve the user's supplied terms faithfully.

8. Do not claim that the document is legally valid,
legally enforceable, or lawyer-reviewed.

9. Use professional legal drafting language.

10. The output must be plain editable text.

11. End with signature blocks appropriate to the parties.

Return the complete document draft.
"""

        return prompt.strip()

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
        jurisdiction: str = "",
        special_instructions: str = "",
    ) -> str:

        prompt = self._build_prompt(
            document_type=document_type,
            parties=parties,
            terms=terms,
            effective_date=effective_date,
            jurisdiction=jurisdiction,
            special_instructions=special_instructions,
        )

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    max_output_tokens=8000,
                ),
            )

        except Exception as exc:
            raise GeminiGenerationError(
                f"Gemini request failed: {exc}"
            ) from exc

        text = getattr(response, "text", None)

        if not text or not text.strip():
            raise GeminiGenerationError(
                "Gemini returned an empty response."
            )

        return text.strip()