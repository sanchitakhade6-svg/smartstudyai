# SmartStudy AI — Merged Project

This package combines the SmartStudy AI frontend and FastAPI backend.

## What is merged
- `frontend/index.html` — working landing page + login/register + study app UI.
- `backend/` — FastAPI API, SQLite database layer, authentication, documents, summaries, flashcards, quizzes, tutor and progress endpoints.
- The backend serves the frontend at `http://127.0.0.1:8000/app/`.

## Windows — easiest way
1. Install Python 3.11+.
2. Double-click `run.bat`.
3. It installs the Python dependencies, starts FastAPI, and opens the app.
4. Register a student account and test the app.

The backend works in **Demo Mode** without a Gemini API key. To enable Gemini AI, copy `backend/.env.example` to `backend/.env` and set `GEMINI_API_KEY` and a strong `SECRET_KEY`.

## API docs
While the backend is running: `http://127.0.0.1:8000/docs`

## Important
The original local database and `.env` secrets were intentionally not copied into this package. A fresh SQLite database is created on first run.

### Offline/demo AI behavior
If `GEMINI_API_KEY` is not configured, document summarization uses local extractive NLP based on the uploaded text, and concept maps use local keyword extraction. Flashcards/quiz/tutor remain demo fallbacks until a Gemini API key is configured.

## Demo-mode behavior
When no Gemini API key is configured, summaries, flashcards, quizzes, and AI Tutor responses are generated from the uploaded document's extracted text using local NLP. They are not unrelated mock questions or generic tutor replies.
