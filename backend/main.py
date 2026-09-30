import os

from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import router


load_dotenv(override=True)

app = FastAPI(
    title="LegalEase API",
    description="AI-powered legal-document generation API.",
    version="1.0.0",
)


origins = [
    item.strip()
    for item in os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:8501,http://127.0.0.1:8501",
    ).split(",")
    if item.strip()
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)


@app.get("/")
def root():

    return {
        "name": os.getenv(
            "APP_NAME",
            "LegalEase",
        ),
        "message": "LegalEase API is running.",
        "docs": "/docs",
    }


@app.get("/health")
def health():

    return {
        "status": "ok",
        "gemini_configured": bool(
            os.getenv("GEMINI_API_KEY")
        ),
        "model": os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash",
        ),
    }