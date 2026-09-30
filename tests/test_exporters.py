from document_utils.exporters import (
    format_docx,
    format_pdf,
    format_txt,
)


SAMPLE_TEXT = """
SERVICE AGREEMENT

1. PARTIES

Client and Provider agree to the terms
of this Service Agreement.

2. PAYMENT

Payment shall be made within 30 days.

3. TERMINATION

Either party may terminate this agreement
with written notice.

SIGNATURES

Client: ____________________

Provider: ____________________
"""


def test_format_txt():

    result = format_txt(SAMPLE_TEXT)

    assert isinstance(result, bytes)

    assert b"SERVICE AGREEMENT" in result

    assert b"PAYMENT" in result


def test_format_docx():

    result = format_docx(
        SAMPLE_TEXT,
        "Service Agreement",
    )

    assert isinstance(result, bytes)

    assert result.startswith(
        b"PK"
    )


def test_format_pdf():

    result = format_pdf(
        SAMPLE_TEXT,
        "Service Agreement",
    )

    assert isinstance(result, bytes)

    assert result.startswith(
        b"%PDF"
    )