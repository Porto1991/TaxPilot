@echo off
REM TaxPilot one-click launcher (Windows).
REM Optional: set your API key first ->  set ANTHROPIC_API_KEY=sk-ant-...
cd /d "%~dp0"

where python >nul 2>nul || (echo ERROR: Python is not installed. Get it from https://python.org & pause & exit /b 1)

if not exist .venv (
  echo Creating virtual environment and installing dependencies - first run only...
  python -m venv .venv
  .venv\Scripts\pip install -q -r requirements.txt
)

if "%ANTHROPIC_API_KEY%"=="" echo WARNING: ANTHROPIC_API_KEY not set - chat will show offline. Upload/analysis still work.

echo TaxPilot running at http://localhost:8000  (close this window to stop)
start "" http://localhost:8000
.venv\Scripts\python -m uvicorn app.main:app --port 8000
