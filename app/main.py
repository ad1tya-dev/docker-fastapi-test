from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schema import UserCreateSchema
from app.services import get_users, create_user

app = FastAPI(title="FastAPI Docker Test")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return {"message": "Hello from FastAPI - Deployed by Jenkins! 🚀"}

@app.get("/users")
def read_users():
    users = get_users()
    return {"data": users}

@app.post("/users")
def add_user(user: UserCreateSchema):
    create_user(user.dict())
    return {"success": True}
