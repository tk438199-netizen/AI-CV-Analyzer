from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.database import engine, Base
from app.models import user, analysis
from app.routes import auth, cv


app = FastAPI(
    title="AI Powered CV Analyzer",
    description="An AI-based CV Analysis System",
    version="2.0.0"
)


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-cv-analyzer-frontend-eight.vercel.app",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create database tables
Base.metadata.create_all(bind=engine)


# Safe migration for existing SQLite databases
try:
    with engine.begin() as conn:

        if engine.dialect.name == "sqlite":

            columns = [
                row[1]
                for row in conn.execute(
                    text("PRAGMA table_info(analysis_history)")
                )
            ]

            if "user_id" not in columns:
                conn.execute(
                    text(
                        "ALTER TABLE analysis_history "
                        "ADD COLUMN user_id INTEGER REFERENCES users(id)"
                    )
                )

            conn.execute(
                text(
                    "CREATE INDEX IF NOT EXISTS "
                    "ix_analysis_history_user_id "
                    "ON analysis_history (user_id)"
                )
            )

except Exception as e:
    print("Migration warning:", e)


# Include API Routers
app.include_router(auth.router)
app.include_router(cv.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to AI Powered CV Analyzer",
        "status": "Backend is Running"
    }


@app.get("/health")
def health_check():
    return {"status": "OK"}