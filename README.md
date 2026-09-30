# LegalEase ⚖️

LegalEase is an AI-powered legal document drafting application.

It uses:

- Streamlit for the frontend
- FastAPI for the backend
- Google Gemini for AI-assisted drafting
- python-docx for DOCX exports
- fpdf2 for PDF exports

## Features

- Legal document draft generation
- Editable document preview
- TXT export
- DOCX export
- PDF export
- Optional branding and logo
- FastAPI REST API
- Basic automated tests
- Docker support
- Render deployment configuration

## Project Structure

```text
LegalEase
│
├── ai_core/
├── assets/
├── backend/
├── document_utils/
├── frontend/
├── tests/
│
├── .env
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── Procfile
├── render.yaml
├── requirements.txt
└── README.md