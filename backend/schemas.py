from typing import Literal

from pydantic import BaseModel, Field, field_validator


DocumentFormat = Literal["txt", "docx", "pdf"]


class DocumentRequest(BaseModel):
    document_type: str = Field(
        ...,
        min_length=2,
        max_length=120,
    )

    parties: str = Field(
        ...,
        min_length=2,
        max_length=5000,
    )

    terms: str = Field(
        ...,
        min_length=2,
        max_length=12000,
    )

    effective_date: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    jurisdiction: str = Field(
        default="",
        max_length=200,
    )

    special_instructions: str = Field(
        default="",
        max_length=5000,
    )

    @field_validator(
        "document_type",
        "parties",
        "terms",
        "effective_date",
    )
    @classmethod
    def strip_required(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("This field cannot be empty.")

        return value


class GenerateResponse(BaseModel):
    document_type: str
    content: str


class ExportRequest(DocumentRequest):
    format: DocumentFormat = "docx"

    company_name: str = Field(
        default="LegalEase",
        max_length=120,
    )

    footer_text: str = Field(
        default=(
            "Generated with LegalEase. "
            "Review with a qualified legal professional before use."
        ),
        max_length=500,
    )

    logo_base64: str | None = None