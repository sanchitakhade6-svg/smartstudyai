"""
SmartStudy AI — FastAPI Backend
================================
Run with:  uvicorn main:app --reload
Docs at:   http://localhost:8000/docs
"""
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config import settings
from database import init_db

# ── Routers ───────────────────────────────────────────────────────────────────
from routers.auth import router as auth_router
from routers.documents import router as documents_router
from routers.summaries import router as summaries_router
from routers.flashcards import router as flashcards_router
from routers.quizzes import router as quizzes_router
from routers.tutor import router as tutor_router
from routers.progress import router as progress_router
from routers.parent import router as parent_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create DB tables and upload directory on startup."""
    os.makedirs(settings.upload_dir, exist_ok=True)
    await init_db()
    print(f"[OK] SmartStudy AI backend started -- Gemini AI: {'enabled' if settings.gemini_api_key else 'DEMO MODE (no API key)'}")
    yield
    # Cleanup on shutdown (nothing needed for SQLite)


app = FastAPI(
    title="SmartStudy AI API",
    description=(
        "Backend API for SmartStudy AI — an AI-powered study companion. "
        "Features: document upload, NLP summarization, flashcard generation (SM-2 spaced repetition), "
        "quiz generation, AI tutor chat, performance tracking, and parent/teacher dashboards."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Tighten this in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ────────────────────────────────────────────────────────────────────
app.include_router(auth_router)
app.include_router(documents_router)
app.include_router(summaries_router)
app.include_router(flashcards_router)
app.include_router(quizzes_router)
app.include_router(tutor_router)
app.include_router(progress_router)
app.include_router(parent_router)

# Serve the merged frontend from the same FastAPI server.
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/app", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")


@app.get("/", tags=["Root"])
async def root():
    return {
        "app": settings.app_name,
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running",
        "ai_mode": "gemini" if settings.gemini_api_key else "demo",
    }


@app.get("/health", tags=["Root"])
async def health():
    return {"status": "ok"}
