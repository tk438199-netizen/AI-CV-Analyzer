from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.database import engine, Base
from app.models import user, analysis
from app.routes import auth, cv

app = FastAPI(title="AI Powered CV Analyzer", description="An AI-based CV Analysis System", version="2.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "https://ai-cv-analyzer-frontend-eight.vercel.app"
    ],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)
Base.metadata.create_all(bind=engine)

# Safe lightweight migration for existing SQLite databases.
try:
    with engine.begin() as conn:
        columns = [row[1] for row in conn.execute(text("PRAGMA table_info(analysis_history)"))] if engine.dialect.name == "sqlite" else []
        if engine.dialect.name == "sqlite" and "user_id" not in columns:
            conn.execute(text("ALTER TABLE analysis_history ADD COLUMN user_id INTEGER REFERENCES users(id)"))
        if engine.dialect.name == "sqlite":
            conn.execute(text("CREATE INDEX IF NOT EXISTS ix_analysis_history_user_id ON analysis_history (user_id)"))
except Exception:
    pass

app.include_router(auth.router)
app.include_router(cv.router)

@app.get("/")
def home():
    return {"message": "Welcome to AI Powered CV Analyzer", "status": "Backend is Running"}

@app.get("/health")
def health_check():
    return {"status": "OK"}
