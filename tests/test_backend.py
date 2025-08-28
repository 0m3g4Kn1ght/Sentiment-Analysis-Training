# backend/test_main.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from backend.main import app

client = TestClient(app)


@pytest.fixture
def mock_register_user():
    with patch("backend.database.register_user") as mock:
        yield mock


@pytest.fixture
def mock_verify_user():
    with patch("backend.database.verify_user") as mock:
        yield mock


@pytest.fixture
def mock_save_history():
    with patch("backend.database.save_history") as mock:
        yield mock


@pytest.fixture
def mock_get_history():
    with patch("backend.database.get_history") as mock:
        yield mock


@pytest.fixture
def mock_is_admin():
    with patch("backend.database.is_admin") as mock:
        yield mock


@pytest.fixture
def mock_list_users():
    with patch("backend.database.list_users") as mock:
        yield mock


def test_register_success(mock_register_user):
    mock_register_user.return_value = 1
    response = client.post("/register", json={"username": "test", "password": "123"})
    assert response.status_code == 200
    assert response.json() == {"account_id": 1, "message": "Registration successful"}


def test_register_fail(mock_register_user):
    mock_register_user.return_value = None
    response = client.post("/register", json={"username": "test", "password": "123"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists"


def test_login_success(mock_verify_user):
    mock_verify_user.return_value = 2
    response = client.post("/login", json={"username": "test", "password": "123"})
    assert response.status_code == 200
    assert response.json() == {"account_id": 2, "message": "Login successful"}


def test_login_fail(mock_verify_user):
    mock_verify_user.return_value = None
    response = client.post("/login", json={"username": "wrong", "password": "bad"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_analyze_positive(mock_save_history):
    response = client.post(
        "/analyze",
        json={"account_id": 1, "text": "I love this project!"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["account_id"] == 1
    assert data["sentiment"] in ["positive", "neutral", "negative"]
    mock_save_history.assert_called_once()


def test_history(mock_get_history):
    mock_get_history.return_value = [
        {"text": "Good job", "sentiment": "positive"}
    ]
    response = client.get("/history/1")
    assert response.status_code == 200
    data = response.json()
    assert data["account_id"] == 1
    assert len(data["history"]) == 1
    assert data["history"][0]["sentiment"] == "positive"


def test_logout():
    response = client.post("/logout", params={"account_id": 1})
    assert response.status_code == 200
    assert response.json() == {"account_id": 1, "message": "Logged out successfully"}


def test_admin_authorized(mock_is_admin, mock_list_users):
    mock_is_admin.return_value = True
    mock_list_users.return_value = ["user1", "user2"]
    response = client.get("/admin/1")
    assert response.status_code == 200
    assert response.json()["users"] == ["user1", "user2"]


def test_admin_unauthorized(mock_is_admin):
    mock_is_admin.return_value = False
    response = client.get("/admin/1")
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authorized"
