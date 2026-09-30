from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_root():

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "LegalEase"

    assert data["message"] == (
        "LegalEase API is running."
    )

    assert data["docs"] == "/docs"


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"

    assert "gemini_configured" in data

    assert "model" in data


def test_generate_validation():

    response = client.post(
        "/generate",
        json={},
    )

    assert response.status_code == 422


def test_generate_missing_terms():

    response = client.post(
        "/generate",
        json={
            "document_type": "Service Agreement",
            "parties": "Client and Provider",
            "terms": "",
            "effective_date": "2026-01-01",
        },
    )

    assert response.status_code == 422