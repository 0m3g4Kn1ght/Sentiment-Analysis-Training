# tests/test_backend.py
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Backend is running!"}

def test_analyze_positive():
    response = client.post("/analyze", json={"text": "I love this project!"})
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] == "positive"

def test_analyze_negative():
    response = client.post("/analyze", json={"text": "I hate bugs!"})
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] == "negative"
