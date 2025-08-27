# Sentiment Analysis App (FastAPI + Streamlit)

This project is a **full-stack sentiment analysis application** built with:  
- **FastAPI** → Backend REST API (sentiment analysis engine)  
- **Streamlit** → Frontend UI  
- **Docker Compose** → Container orchestration  
- **GitHub Actions** → CI/CD automation  

It analyzes the sentiment of input text (e.g., tweets) using **VADER Sentiment Analysis** and classifies it as *positive, negative, or neutral*.  

---

## Project Structure
```
project-root/
│── backend/                  # FastAPI backend
│   ├── main.py               # Main FastAPI app
│   ├── models.py             # Pydantic models
│   ├── requirements.txt      # Backend dependencies
│   └── Dockerfile            # Backend Dockerfile
│
│── frontend/                 # Streamlit frontend
│   ├── app.py                # Main Streamlit app
│   ├── requirements.txt      # Frontend dependencies
│   └── Dockerfile            # Frontend Dockerfile
│
│── tests/                    # Pytest test cases
│   └── test_backend.py       # Backend tests
│
│── docker-compose.yml        # Orchestration file
│── .github/workflows/ci-cd.yml # GitHub Actions CI/CD workflow
```

---

## Backend (FastAPI)

The backend provides a REST API for sentiment analysis.

### Run Backend Locally
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### API Endpoints
- `GET /` → Health check  
- `POST /analyze` → Accepts JSON `{ "text": "your sentence" }` and returns sentiment result  

Example:
```bash
curl -X POST "http://127.0.0.1:8000/analyze"      -H "Content-Type: application/json"      -d '{"text": "I love FastAPI!"}'
```

Response:
```json
{
  "text": "I love FastAPI!",
  "sentiment": "positive",
  "scores": {
    "neg": 0.0,
    "neu": 0.25,
    "pos": 0.75,
    "compound": 0.87
  }
}
```

---

## Frontend (Streamlit)

The frontend provides a simple UI for entering text and viewing results.

### Run Frontend Locally
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

It connects to the backend at `http://localhost:8000/analyze`.

---

## Docker Setup

Run both frontend and backend with Docker Compose:

```bash
docker-compose up --build
```

- Backend → [http://localhost:8000](http://localhost:8000)  
- Frontend → [http://localhost:8501](http://localhost:8501)  

The frontend communicates with the backend via service name `backend`.

---

## Running Tests

Tests are written with **Pytest** for the backend.

```bash
pytest tests/
```

---

## CI/CD (GitHub Actions)

The workflow (`.github/workflows/ci-cd.yml`) runs automatically on push to `main`:  
1. Install dependencies  
2. Run tests  
3. Build and push Docker images (if tests pass)  

Docker Hub credentials must be set in GitHub secrets.  

---

## Tech Stack
- **Backend:** FastAPI, VADER Sentiment  
- **Frontend:** Streamlit  
- **Testing:** Pytest  
- **Containerization:** Docker & Docker Compose  
- **CI/CD:** GitHub Actions  