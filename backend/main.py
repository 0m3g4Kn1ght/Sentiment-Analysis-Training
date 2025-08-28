from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import backend.database as database

app = FastAPI()

class RegisterInput(BaseModel):
    username: str
    password: str

class LoginInput(BaseModel):
    username: str
    password: str

class AnalyzeInput(BaseModel):
    account_id: int
    text: str


@app.post("/register")
def register(user: RegisterInput):
    account_id = database.register_user(user.username, user.password)
    if not account_id:
        raise HTTPException(status_code=400, detail="Username already exists")
    return {"account_id": account_id, "message": "Registration successful"}


@app.post("/login")
def login(user: LoginInput):
    account_id = database.verify_user(user.username, user.password)
    if not account_id:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"account_id": account_id, "message": "Login successful"}


@app.post("/analyze")
def analyze(data: AnalyzeInput):
    sentiment = "positive" if "love" in data.text.lower() else "negative"
    database.save_history(data.account_id, data.text, sentiment)
    return {"account_id": data.account_id, "sentiment": sentiment}


@app.get("/history/{account_id}")
def history(account_id: int):
    history = database.get_history(account_id)
    return {"account_id": account_id, "history": history}


@app.post("/logout")
def logout(account_id: int):
    return {"account_id": account_id, "message": "Logged out successfully"}


@app.get("/admin/{account_id}")
def admin_panel(account_id: int):
    if not database.is_admin(account_id):
        raise HTTPException(status_code=403, detail="Not authorized")
    return {"message": "Welcome Admin", "users": database.list_users()}
