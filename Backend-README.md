# StockSpies Backend (Django) — Quick Start for Teammates

This backend provides the Upload API consumed by the StockSpies frontend.

Endpoints
- GET `http://127.0.0.1:8000/api/upload`: readiness check JSON.
- POST `http://127.0.0.1:8000/api/upload`: `multipart/form-data` with a `file` field; returns dynamic JSON so you can confirm you’re hitting the backend.

Prerequisites
- Python 3.9+ available as `python3`/`python`.
- Recommended: VS Code + Python extension.

First-Time Setup
1) Create/activate a virtualenv
   - macOS/Linux:
     - `python3 -m venv .venv`
     - `source .venv/bin/activate`
   - Windows (PowerShell):
     - `python -m venv .venv`
     - `.venv\Scripts\Activate.ps1`

2) Install dependencies
   - `pip install -r requirements.txt`

3) Migrate and run
   - `python manage.py migrate`
   - `python manage.py runserver 127.0.0.1:8000`
   - Open http://127.0.0.1:8000/api/upload to verify readiness.

Frontend Wiring (local dev)
- In the frontend repo, set `.env.local`:
  - `VITE_BACKEND_URL=http://127.0.0.1:8000/api`
- Restart Vite if you changed `.env.local`.

Project Layout
- `sle_backend_app/urls.py` — mounts app URLs at `/api/`.
- `sle_backend_app/quickstart/urls.py` — exposes `/api/upload` (with or without trailing slash).
- `sle_backend_app/quickstart/views.py` — `upload` view; returns dynamic JSON and logs the uploaded file.
- `sle_backend_app/settings.py` — includes `corsheaders`, `sle_backend_app.quickstart`, local CORS and allowed hosts.

API Details
- GET `/api/upload`
  - Returns `{ "ok": true, "detail": "upload endpoint is ready; POST a file" }`.
- POST `/api/upload`
  - Body: `multipart/form-data` with `file`.
  - Returns example: `{ "stock_percentage": 37.0, "type": "backend-jpg" }`.

Quick Tests
- Readiness: `curl -i http://127.0.0.1:8000/api/upload`
- Upload: `curl -i -F "file=@/path/to/test.jpg" http://127.0.0.1:8000/api/upload`
- Server log: check your runserver terminal for lines like
  - `[upload] Received file: name=test.jpg, size=12345 bytes`

CSRF & CORS (dev defaults)
- The upload view is CSRF‑exempt for dev to ease wiring.
- CORS allowed origins (in `sle_backend_app/settings.py`):
  - `http://localhost:5173`, `http://127.0.0.1:5173`
- Allowed hosts: `127.0.0.1`, `localhost`.









## Windows Setup (PowerShell)

1) Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If activation is blocked, allow scripts for the current user (one-time):

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force
```

Alternatively, use Command Prompt (cmd.exe):

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

2) Install dependencies

```powershell
pip install -r requirements.txt
```

3) Run migrations and start the server

```powershell
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

4) Verify the API

PowerShell sometimes aliases `curl` to `Invoke-WebRequest`. Use `curl.exe` explicitly:

```powershell
curl.exe -i http://127.0.0.1:8000/api/upload
curl.exe -i -F "file=@C:\path\to\test.jpg" http://127.0.0.1:8000/api/upload
```

Or use Git Bash (if installed) and the same curl commands as macOS/Linux.
