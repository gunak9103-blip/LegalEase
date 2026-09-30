install:
	python -m pip install -r requirements.txt

test:
	python -m pytest -q

backend:
	uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

frontend:
	streamlit run frontend/app.py

run:
	uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000