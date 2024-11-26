@echo off
REM Check if Python is installed
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python is not installed. Please install Python 3.7+ and try again.
    pause
    exit /b
)

REM Ensure pip is up to date
echo Updating pip...
python -m pip install --upgrade pip

REM Install required packages
echo Installing required Python packages (PyQt5 and watchdog)...
pip install PyQt5

REM Run the configuration menu
echo Opening configuration menu...
python menu.py

pause
