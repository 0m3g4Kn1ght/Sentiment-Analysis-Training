import pytest
from fastapi.testclient import TestClient
from backend.main import app
import backend.database as database

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    database.init_db()
    yield


def test_register_user():
    response = client.post("/register", json={"username": "alice", "password": "password123"})
    assert response.status_code == 200
    data = response.json()
    assert "account_id" in data
    assert data["message"] == "Registration successful"


def test_login_logout():
    r = client.post("/register", json={"username": "bob", "password": "secret"})
    account_id = r.json()["account_id"]

    response = client.post("/login", json={"username": "bob", "password": "secret"})
    assert response.status_code == 200
    data = response.json()
    assert data["account_id"] == account_id
    assert data["message"] == "Login successful"

    response = client.post("/logout", params={"account_id": account_id})
    assert response.status_code == 200
    assert response.json()["message"] == "Logged out successfully"


def test_analyze_and_history():
    r = client.post("/register", json={"username": "charlie", "password": "mypassword"})
    account_id = r.json()["account_id"]

    response = client.post("/analyze", json={"account_id": account_id, "text": "I love coding!"})
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] in ["positive", "negative"]

    response = client.get(f"/history/{account_id}")
    assert response.status_code == 200
    history = response.json()["history"]
    assert len(history) > 0
    assert history[0]["text"] == "I love coding!"


def test_admin_panel():
    r1 = client.post("/register", json={"username": "dave", "password": "123"})
    user_id = r1.json()["account_id"]

    r2 = client.post("/register", json={"username": "admin", "password": "adminpass"})
    admin_id = r2.json()["account_id"]

    conn = database.sqlite3.connect(database.DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE users SET is_admin=1 WHERE id=?", (admin_id,))
    conn.commit()
    conn.close()

    response = client.get(f"/admin/{user_id}")
    assert response.status_code == 403

    response = client.get(f"/admin/{admin_id}")
    assert response.status_code == 200
    data = response.json()
    assert "users" in data
