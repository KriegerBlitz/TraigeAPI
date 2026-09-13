# Clinical Triage & Patient Prioritization Service

A lightweight RESTful API built with **FastAPI** and **SQLite** to manage patient intakes and compute deterministic urgency scores for clinical prioritization.

## Features
* **Automated Urgency Scoring**: Dynamically calculates triage scores based on patient age brackets and self-reported pain levels.
* **Persistent Relational Storage**: Stores records locally with SQLite using parameterized queries to prevent SQL injection.
* **Data Validation**: Enforces strict request/response schemas using Pydantic models.
* **Interactive API Docs**: Auto-generates OpenAPI (Swagger UI) documentation out of the box.
* **Containerized Deployment**: Includes a `Dockerfile` for reproducible container runtime environments.

## Tech Stack
* **Language**: Python 3.11+
* **Framework**: FastAPI, Uvicorn
* **Database**: SQLite3
* **Testing**: PyTest, HTTPX
* **Containerization**: Docker

## Quickstart

### Local Setup
```bash
git clone https://github.com/<YOUR_USERNAME>/clinical-triage-api.git
cd clinical-triage-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser to test endpoints via Swagger UI.

### Run Tests
```bash
pytest
```
