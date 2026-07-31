# Smart CV Backend

This backend follows a clean FastAPI project structure.

## Project layout

- `app/`
  - `api/`
    - `v1/`
      - `endpoints/`
      - `api.py`
  - `core/`
    - `config.py`
    - `logging.py`
  - `schemas/`
  - `services/`
  - `prompts/`
  - `utils/`
  - `models/`
  - `main.py`
- `.env`
- `.gitignore`
- `requirements.txt`
- `venv/`

## Run locally

1. Activate your venv:

```powershell
cd smart_cv_backend
.\venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Start the server:

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API

- `GET /api/v1/hello/` - simple health/example endpoint
