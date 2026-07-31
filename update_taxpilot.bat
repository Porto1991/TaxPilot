@echo off
REM TaxPilot self-updater (Windows): downloads the latest version from GitHub
REM and updates this folder, keeping your anthropic_key.txt and the installed .venv.
cd /d "%~dp0"

echo Downloading the latest TaxPilot from GitHub...
powershell -NoProfile -Command "Invoke-WebRequest -Uri 'https://codeload.github.com/Porto1991/TaxPilot/zip/refs/heads/main' -OutFile $env:TEMP\taxpilot_update.zip" || (echo ERROR: download failed - check internet/VPN & pause & exit /b 1)

echo Unpacking...
powershell -NoProfile -Command "Remove-Item -Recurse -Force $env:TEMP\taxpilot_update -ErrorAction SilentlyContinue; Expand-Archive -Force $env:TEMP\taxpilot_update.zip $env:TEMP\taxpilot_update"

echo Updating files...
robocopy "%TEMP%\taxpilot_update\TaxPilot-main" . /E /XF anthropic_key.txt /XD .venv >nul
if %ERRORLEVEL% GEQ 8 (echo ERROR: copy failed & pause & exit /b 1)

echo.
echo Updated successfully. Now double-click start_taxpilot.bat
pause
