@echo off
REM Database Migration POC - GUI Launcher
REM This script activates the virtual environment and launches the GUI

echo 🚀 Starting Database Migration POC GUI...
echo.

REM Change to the project directory
cd /d "%~dp0"

REM Activate virtual environment and run GUI
call "db-venv\Scripts\activate.bat"
echo ✅ Virtual environment activated
echo.

echo 🖥️ Launching GUI application...
python gui.py

echo.
echo 👋 GUI application closed.
pause
