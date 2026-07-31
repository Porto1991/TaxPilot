@echo off
REM Stops the TaxPilot server started by start_taxpilot.bat.
taskkill /f /fi "WINDOWTITLE eq TaxPilot Server*" >nul 2>nul
echo TaxPilot stopped.
timeout /t 2 >nul
