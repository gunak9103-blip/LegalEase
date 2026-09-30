import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import base64
import html
import os
import tempfile
from datetime import date

import requests
import streamlit as st
from dotenv import load_dotenv

from document_utils.exporters import (
    format_docx,
    format_pdf,
    format_txt,
)

from document_utils.formatting import (
    format_html_preview,
    sanitize_text,
    terms_to_list,
)


load_dotenv()


st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000",
).rstrip("/")


APP_NAME = os.getenv(
    "APP_NAME",
    "LegalEase",
)


DEFAULT_LOGO = os.getenv(
    "LOGO_PATH",
    "assets/logo.png",
)


def inject_css():

    st.markdown(
        """
<style>

.hero {
    padding: 1.4rem;
    border-radius: 16px;
    background: linear-gradient(
        135deg,
        #111827,
        #1f2937
    );
    color: white;
    margin-bottom: 1rem;
}

.hero h1 {
    margin: 0;
    font-size: 2.1rem;
}

.hero p {
    margin-top: .4rem;
    opacity: .85;
}

.legal-preview {
    background: #111827;
    color: #f9fafb;
    padding: 1.4rem;
    border-radius: 14px;
    max-height: 650px;
    overflow-y: auto;
    border: 1px solid #374151;
    line-height: 1.65;
}

.legal-preview h3 {
    margin-top: 1rem;
    border-bottom: 1px solid #4b5563;
    padding-bottom: .25rem;
}

.legal-preview p {
    margin: .45rem 0;
}

.legal-preview li {
    margin: .3rem 0;
}

.spacer {
    height: .35rem;
}

.notice {
    padding: .75rem 1rem;
    border-radius: 10px;
    background: #fff7ed;
    border: 1px solid #fed7aa;
}

</style>
        """,
        unsafe_allow_html=True,
    )


def get_logo_bytes(uploaded_file):

    if uploaded_file:
        return uploaded_file.getvalue()

    path = PROJECT_ROOT / DEFAULT_LOGO

    if path.exists():
        return path.read_bytes()

    return None


def call_generate(payload: dict) -> str:

    timeout = int(
        os.getenv(
            "REQUEST_TIMEOUT_SECONDS",
            "90",
        )
    )

    response = requests.post(
        f"{BACKEND_URL}/generate",
        json=payload,
        timeout=timeout,
    )

    if response.status_code != 200:

        try:
            detail = response.json().get(
                "detail",
                response.text,
            )

        except Exception:
            detail = response.text

        raise RuntimeError(str(detail))

    return response.json()["content"]


inject_css()


hero_html = f"""
<div class="hero">
    <h1>⚖️ {html.escape(APP_NAME)}</h1>
    <p>
        AI-assisted legal document drafting,
        editable preview, and branded export.
    </p>
</div>
"""

st.markdown(
    hero_html,
    unsafe_allow_html=True,
)


with st.sidebar:

    st.header("Document settings")

    document_type = st.selectbox(
        "Document type",
        [
            "Employment Contract",
            "Non-Disclosure Agreement",
            "Lease Agreement",
            "Employment Offer Letter",
            "Service Agreement",
            "Freelance Work Contract",
            "General Agreement",
            "Custom",
        ],
    )

    if document_type == "Custom":

        document_type = st.text_input(
            "Custom document type",
            "Legal Agreement",
        )

    jurisdiction = st.text_input(
        "Jurisdiction",
        "",
    )

    effective_date = st.date_input(
        "Effective date",
        value=date.today(),
    )

    company_name = st.text_input(
        "Brand/company name",
        APP_NAME,
    )

    footer_text = st.text_input(
        "Footer",
        (
            "Generated with LegalEase. "
            "Review with a qualified legal "
            "professional before use."
        ),
    )

    logo_upload = st.file_uploader(
        "Optional logo",
        type=[
            "png",
            "jpg",
            "jpeg",
        ],
        help="Used in DOCX/PDF exports.",
    )

    st.divider()

    st.caption("FastAPI backend")

    st.code(
        BACKEND_URL,
        language="text",
    )


st.subheader("Document details")


col1, col2 = st.columns(2)


with col1:

    parties = st.text_area(
        "Parties involved",
        placeholder=(
            "Jane Doe (Service Provider), "
            "TechNova Inc. (Client)"
        ),
        height=130,
    )


with col2:

    terms = st.text_area(
        "Terms & conditions",
        placeholder=(
            "Payment within 30 days of invoice; "
            "Provider delivers work by agreed deadline; "
            "Confidentiality must be maintained; "
            "Either party may terminate with 15 days notice"
        ),
        height=130,
    )


special_instructions = st.text_area(
    "Special instructions",
    placeholder=(
        "Add drafting preferences, "
        "placeholders, or additional requirements."
    ),
    height=100,
)


if st.button(
    "✨ Generate Document",
    type="primary",
    use_container_width=True,
):

    if (
        not parties.strip()
        or not terms.strip()
    ):

        st.error(
            "Please provide both parties and terms."
        )

    else:

        payload = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "effective_date": effective_date.isoformat(),
            "jurisdiction": jurisdiction,
            "special_instructions": special_instructions,
        }

        with st.spinner(
            "Generating your document..."
        ):

            try:

                st.session_state["document"] = (
                    call_generate(payload)
                )

                st.session_state["document_type"] = (
                    document_type
                )

                st.session_state["terms"] = terms

                st.success(
                    "Document generated. "
                    "Review it carefully before use."
                )

            except Exception as exc:

                st.error(
                    f"Generation failed: {exc}"
                )


if "document" in st.session_state:

    st.divider()

    st.subheader("Editable document")

    edited = st.text_area(
        "Click into the document below to edit it.",
        value=st.session_state["document"],
        height=520,
        key="document_editor",
    )

    edited = sanitize_text(edited)

    st.session_state["document"] = edited

    st.subheader("Preview")

    st.markdown(
        format_html_preview(edited),
        unsafe_allow_html=True,
    )

    st.subheader("Download")

    logo_bytes = get_logo_bytes(logo_upload)

    logo_b64 = None

    if logo_bytes:

        logo_b64 = base64.b64encode(
            logo_bytes
        ).decode()

    txt_data = format_txt(edited)

    docx_data = format_docx(
        edited,
        st.session_state.get(
            "document_type",
            document_type,
        ),
        company_name,
        footer_text,
        logo_b64,
    )

    pdf_path = None

    if logo_bytes:

        temp = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".png",
        )

        temp.write(logo_bytes)
        temp.close()

        pdf_path = temp.name

    try:

        pdf_data = format_pdf(
            edited,
            st.session_state.get(
                "document_type",
                document_type,
            ),
            company_name,
            footer_text,
            pdf_path,
        )

    finally:

        if pdf_path:

            try:
                os.unlink(pdf_path)

            except OSError:
                pass

    d1, d2, d3 = st.columns(3)

    with d1:

        st.download_button(
            "⬇️ Download TXT",
            data=txt_data,
            file_name="legalease_document.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with d2:

        st.download_button(
            "⬇️ Download DOCX",
            data=docx_data,
            file_name="legalease_document.docx",
            mime=(
                "application/"
                "vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            use_container_width=True,
        )

    with d3:

        st.download_button(
            "⬇️ Download PDF",
            data=pdf_data,
            file_name="legalease_document.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    with st.expander(
        "Terms parsed from semicolon-separated input"
    ):

        parsed_terms = terms_to_list(
            st.session_state.get(
                "terms",
                ""
            )
        )

        for item in parsed_terms:

            st.write(
                f"• {item}"
            )


st.divider()


st.markdown(
    """
<div class="notice">
    <strong>Important:</strong>
    LegalEase generates drafts for informational
    and drafting assistance.

    AI output may contain errors or omit
    jurisdiction-specific requirements.

    Have a qualified legal professional review
    important documents before signing or relying
    on them.
</div>
    """,
    unsafe_allow_html=True,
)