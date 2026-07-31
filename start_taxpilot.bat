@echo off
REM TaxPilot launcher (Windows). The server runs in a separate MINIMIZED window
REM named "TaxPilot Server" so accidental Ctrl+C can't kill it.
REM To stop TaxPilot: run stop_taxpilot.bat (or close the "TaxPilot Server"
REM window from the taskbar).
cd /d "%~dp0"

if exist anthropic_key.txt (
  set /p ANTHROPIC_API_KEY=<anthropic_key.txt
  echo API key loaded from anthropic_key.txt
)

where python >nul 2>nul || (echo ERROR: Python is not installed. Get it from https://python.org & pause & exit /b 1)

if not exist .venv (
  echo Creating virtual environment and installing dependencies - first run only...
  python -m venv .venv
  .venv\Scripts\pip install -q -r requirements.txt
)

if "%ANTHROPIC_API_KEY%"=="" echo WARNING: ANTHROPIC_API_KEY not set - chat will show offline. Create anthropic_key.txt with your key.

echo Starting the TaxPilot server in a minimized window...
start "TaxPilot Server" /min .venv\Scripts\python.exe -m uvicorn app.main:app --port 8000
timeout /t 3 >nul
start "" http://localhost:8000
echo.
echo TaxPilot is running at http://localhost:8000
echo To stop it: double-click stop_taxpilot.bat
timeout /t 6 >nul
