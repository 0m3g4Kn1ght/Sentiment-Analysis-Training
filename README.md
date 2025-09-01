# Sentiment Analysis App (FastAPI + Streamlit)

A full-stack sentiment analysis application featuring:

- **FastAPI** backend for sentiment evaluation using VADER  
- **Streamlit** frontend for interactive user experience  
- **Docker Compose** setup for seamless container orchestration  
- **GitHub Actions** for CI/CD automation

---

##  Project Structure

```
project-root/
├── backend/
│   ├── main.py           # FastAPI app logic
│   ├── database.py       # SQLite helper functions and auth logic
│   ├── models.py         # Pydantic data models
│   ├── requirements.txt  # Backend Python dependencies
│   └── Dockerfile        # Backend Docker configuration
├── frontend/
│   ├── app.py            # Streamlit app interface
│   ├── requirements.txt  # Frontend Python dependencies
│   └── Dockerfile        # Frontend Docker configuration
├── tests/
│   └── test_backend.py   # Pytest test suite for backend
├── docker-compose.yml    # Orchestration of backend + frontend
├── .github/
│   └── workflows/
│       └── ci-cd.yml     # GitHub Actions CI/CD workflow
└── README.md             # This documentation
```

---

##  Features

### Backend (FastAPI)

- **Endpoints**:
  - `POST /register`: Register a new user and receive an `account_id`
  - `POST /login`: Authenticate and get back `account_id`
  - `POST /analyze`: Submit text (with `account_id`) to get sentiment and score details
  - `GET /history/{account_id}`: Retrieve sentiment history for a given user
  - `POST /logout`: Acknowledges "logout" (session-free simplified flow)
  - `GET /admin/{account_id}`: Admin-only endpoint to list all registered users

- **Authentication**:  
  Based solely on `account_id`; no complex token system required.

- **Persistence**:  
  SQLite-based storage with tables for users and history.

---

##  Frontend (Streamlit)

- A clean UI for users to enter text and receive live sentiment feedback.
- Communicates with the backend via configured `BACKEND_URL` (either local or Docker network).

---

##  Local Development Setup

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

- **Test endpoint** via:
  ```bash
  curl -X POST http://127.0.0.1:8000/analyze        -H "Content-Type: application/json"        -d '{"account_id": 1, "text": "I love this!"}'
  ```

### Frontend
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

---

##  Containerized Workflow with Docker Compose

```bash
docker-compose up --build
```

- Visit **Backend** at: `http://localhost:8000`
- Visit **Frontend** at: `http://localhost:8501`

---

##  Testing

Run backend tests with **Pytest**:

```bash
pytest tests/
```

---

##  CI & CD (GitHub Actions)

Triggered on pushes to `main`:

1. Installs dependencies and runs tests
2. Upon success, builds and pushes Docker images for backend and frontend

Ensure you set up the following secrets in your repository for Docker image publishing:

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN` (GitHub–or Docker Hub–generated token)

---

##  Tech Stack Summary

| Layer     | Technology                    |
|-----------|-------------------------------|
| Backend   | Python, FastAPI, VADER         |
| Frontend  | Python, Streamlit              |
| Database  | SQLite (via `database.py`)     |
| Container | Docker, Docker Compose         |
| CI/CD     | GitHub Actions, Docker Hub     |
| Testing   | Pytest                         |

---

##  Getting Started

1. **Clone the repository**  
   ```bash
   git clone <repo-url>
   cd Sentiment-Analysis-Training
   ```

2. **Set up the backend and frontend** (either locally per above instructions or via Docker Compose).

3. **Run your tests**:
   ```bash
   pytest
   ```

4. **Deploy** using Docker or let GitHub handle it via CI/CD when you push updates.

---

##  License

This project is open-source and distributed under the **Apache-2.0 License**. Find the full license terms in the `LICENSE` file.

