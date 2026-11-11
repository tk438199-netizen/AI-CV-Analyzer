from fastapi import FastAPI
from app.routes import cv
from app.database import engine, Base
from app.models import user
from app.routes import auth
from fastapi.middleware.cors import CORSMiddleware


# FastAPI application তৈরি
app = FastAPI(
    title="AI Powered CV Analyzer",
    description="An AI-based CV Analysis System",
    version="1.0.0"
    
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
# Home Route
@app.get("/")
def home():

    return {
        "message": "Welcome to AI Powered CV Analyzer",
        "status": "Backend is Running"
    }


# Health Check Route
@app.get("/health")
def health_check():

    return {
        "status": "OK"
    }

# Register CV Router
app.include_router(cv.router)