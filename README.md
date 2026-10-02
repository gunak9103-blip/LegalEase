# LegalEase ⚖️

LegalEase is an AI-powered legal document drafting application that helps users generate structured legal document drafts from user-provided information.

It combines a Streamlit frontend, FastAPI backend, and Google Gemini for AI-assisted document generation, with editable previews and branded document exports.

> **Disclaimer:** LegalEase generates AI-assisted document drafts for informational and drafting purposes. Documents should be reviewed by a qualified legal professional before use.

## 🚀 Live Demo

**Frontend:**  
https://legalease-frontend-w4gl.onrender.com

**Backend API:**  
https://legalease-backend-v2.onrender.com

**API Documentation:**  
https://legalease-backend-v2.onrender.com/docs

## ✨ Features

- AI-assisted legal document drafting with Google Gemini
- Editable document preview
- TXT export
- DOCX export
- PDF export
- Optional company branding and logo
- FastAPI REST API
- Streamlit frontend
- Automated tests with pytest
- Docker support
- Render deployment

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Streamlit | Frontend UI |
| FastAPI | Backend REST API |
| Google Gemini | AI document generation |
| Pydantic | Request validation |
| python-docx | DOCX generation |
| fpdf2 | PDF generation |
| Pillow | Logo/image handling |
| Requests | Frontend-backend communication |
| Pytest | Automated testing |
| Docker | Containerization |
| Render | Cloud deployment |
| Git/GitHub | Version control |

## 🏗️ Architecture

```text
User
 │
 ▼
Streamlit Frontend
 │
 │ HTTP REST API
 ▼
FastAPI Backend
 │
 │ Gemini API
 ▼
Google Gemini