from fastapi import FastAPI
from typing import List, Optional
from pydantic import BaseModel
import json
import os

app = FastAPI(title="FastAPI Docker Demo")

# Data file path
DATA_FILE = "app/data/users.json"

class User(BaseModel):
    id: int
    name: str
    email: str

def load_users() -> List[User]:
    """Load users from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            return [User(**user) for user in data]
    return []

def save_users(users: List[User]):
    """Save users to JSON file"""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump([user.dict() for user in users], f, indent=2)

@app.get("/")
def read_root():
    return {
        "message": "FastAPI Docker Demo",
        "status": "running",
        "endpoints": ["/users", "/users/{user_id}"]
    }

@app.get("/users", response_model=List[User])
def get_users():
    """Get all users"""
    return load_users()

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    """Get a specific user"""
    users = load_users()
    for user in users:
        if user.id == user_id:
            return user
    return {"error": "User not found"}

@app.post("/users", response_model=User)
def create_user(user: User):
    """Create a new user"""
    users = load_users()
    users.append(user)
    save_users(users)
    return user

@app.get("/health")
def health_check():
    return {"status": "healthy"}
