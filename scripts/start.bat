@echo off
chcp 65001 >nul
echo ===============================
echo    WISEACRE Bot Launcher
echo ===============================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo Checking dependencies...
if not exist "requirements.txt" (
    echo ERROR: requirements.txt not found
    pause
    exit /b 1
)

echo Installing/updating dependencies...
pip install -r requirements.txt

echo Starting WISEACRE bot...
python bot.py

pause
