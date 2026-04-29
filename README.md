# MedSense AI

A full-stack AI system for analyzing medical health reports using advanced NLP and computer vision.

## Features

- PDF and image report parsing
- ChromaDB vector storage for RAG
- LangGraph multi-agent pipeline (Analyzer, Diet Advisor, Comparator)
- Real-time SSE streaming
- Hindi/English language support
- TrueFoundry LLM integration

## Architecture

```
Frontend (React/TypeScript) <-> FastAPI Backend <-> ChromaDB + LangGraph + TrueFoundry LLM
```

## Local Setup

### Backend

1. Install Python 3.10+
2. `cd backend`
3. `pip install -r requirements.txt`
4. Create `.env` with your TrueFoundry API key
5. `uvicorn main:app --reload`

### Frontend

1. Install Node.js 18+
2. `cd frontend`
3. `npm install`
4. `npm run dev`

## API Endpoints

- `POST /upload`: Upload PDF/image, returns report_id
- `POST /analyze`: Stream analysis via SSE
- `GET /reports/{patient_id}`: List past reports

## TrueFoundry Setup

1. Sign up at truefoundry.com
2. Get API key from dashboard
3. Add to `.env`: `TRUEFOUNDRY_API_KEY=your_key`

## Deployment

Deploy to Render using `render.yaml`.

## Usage

1. Upload medical report
2. Enter patient details
3. Click analyze for streaming insights
