# Medietat

Job search engine for medical professionals in Poland.

## Project Structure

```
medi-etat/
├── backend/          # FastAPI backend
├── frontend/         # Next.js frontend (to be added)
├── scripts/          # Scraper scripts (to be added)
└── data/             # Data files (to be added)
```

## Backend Setup

1. Create virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
uvicorn app.main:app --reload
```

4. API will be available at:
- http://localhost:8000
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## Database

SQLite database (`medi-etat.db`) will be created automatically on first run.

## API Endpoints

- `GET /` - Health check
- `GET /health` - Health check
- `GET /api/jobs` - List job offers (with optional `role` filter)
- `GET /api/jobs/{id}` - Get job offer by ID

## Development Status

- ✅ Phase 1: Foundation (Database + FastAPI setup)
- ⏳ Phase 2: Scraper framework
- ⏳ Phase 3: Scrapers for 4 Gdańsk sources
- ⏳ Phase 4: Frontend

