# backend/models.py
from pydantic import BaseModel

class Tweet(BaseModel):
    text: str

class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str
