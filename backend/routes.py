import base64
import os
import tempfile

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from ai_core.gemini_generator import (
    GeminiConfigurationError,
    GeminiDocumentGenerator,
    GeminiGenerationError,
)

from document_utils.exporters import (
    format_docx,
    format_pdf,
    format_txt,
)

from document_utils.formatting import sanitize_text

from backend.schemas import (
    DocumentRequest,
    ExportRequest,
    GenerateResponse,
)


router = APIRouter()


def _generator():
    try:
        return GeminiDocumentGenerator()

    except GeminiConfigurationError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc


def _generate(
    request: DocumentRequest,
) -> str:

    generator = _generator()

    try:
        result = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            effective_date=request.effective_date,
            jurisdiction=request.jurisdiction,
            special_instructions=request.special_instructions,
        )

        return sanitize_text(result)

    except GeminiGenerationError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc


@router.post(
    "/generate",
    response_model=GenerateResponse,
)
def generate_document(
    request: DocumentRequest,
):

    content = _generate(request)

    return GenerateResponse(
        document_type=request.document_type,
        content=content,
    )


@router.post(
    "/generate/export",
)
def generate_and_export(
    request: ExportRequest,
):

    content = _generate(request)

    if request.format == "txt":

        data = format_txt(content)

        media_type = "text/plain; charset=utf-8"

        filename = "legalease_document.txt"

    elif request.format == "docx":

        data = format_docx(
            content,
            request.document_type,
            request.company_name,
            request.footer_text,
            request.logo_base64,
        )

        media_type = (
            "application/"
            "vnd.openxmlformats-officedocument."
            "wordprocessingml.document"
        )

        filename = "legalease_document.docx"

    else:

        logo_path = None
        temporary_file = None
        logo_bytes = None

        if request.logo_base64:

            try:
                encoded = request.logo_base64.split(
                    ",",
                    1,
                )[-1]

                logo_bytes = base64.b64decode(
                    encoded,
                )

            except Exception:
                logo_bytes = None

        if logo_bytes:

            temporary_file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".png",
            )

            temporary_file.write(
                logo_bytes,
            )

            temporary_file.close()

            logo_path = temporary_file.name

        try:

            data = format_pdf(
                content,
                request.document_type,
                request.company_name,
                request.footer_text,
                logo_path,
            )

        finally:

            if (
                temporary_file
                and os.path.exists(
                    temporary_file.name,
                )
            ):
                os.unlink(
                    temporary_file.name,
                )

        media_type = "application/pdf"

        filename = "legalease_document.pdf"

    return Response(
        content=data,
        media_type=media_type,
        headers={
            "Content-Disposition":
            f'attachment; filename="{filename}"'
        },
    )