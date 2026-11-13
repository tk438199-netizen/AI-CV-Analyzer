from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field
from app.database import get_db
from app.models.user import User
from app.services.auth import hash_password, verify_password
from app.services.security import create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

class UserRegister(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

def public_user(user):
    return {"id": user.id, "full_name": user.full_name, "email": user.email}

@router.post("/register")
def register_user(data: UserRegister, db: Session = Depends(get_db)):
    email = data.email.lower()
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(full_name=data.full_name.strip(), email=email, hashed_password=hash_password(data.password))
    db.add(user); db.commit(); db.refresh(user)
    token = create_access_token(user.id)
    return {"message": "User registered successfully", "access_token": token, "token_type": "bearer", "user": public_user(user)}

@router.post("/login")
def login_user(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email.lower()).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"message": "Login successful", "access_token": create_access_token(user.id), "token_type": "bearer", "user": public_user(user)}

@router.get("/me")
def get_me(user: User = Depends(get_current_user)):
    return {"user": public_user(user)}
