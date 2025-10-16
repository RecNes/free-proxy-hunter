@echo off
setlocal enabledelayedexpansion

REM Configuration
set REPO_URL=https://github.com/RecNes/free-proxy-hunter.git
set PROJECT_DIR=free-proxy-hunter
set VENV_DIR=.venv

REM Check Python installation
where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python is not installed. Please install Python 3.7 or higher.
    goto :cleanup
)

REM Check Python version
for /f "tokens=2 delims= " %%A in ('python -V 2^>^&1') do set PYTHON_VERSION=%%A
for /f "tokens=1,2 delims=." %%A in ("!PYTHON_VERSION!") do (
    set MAJOR=%%A
    set MINOR=%%B
)

if !MAJOR! LSS 3 (
    echo [ERROR] Python version !PYTHON_VERSION! is too old. Minimum required is 3.7.
    goto :cleanup
) else if !MAJOR! EQU 3 if !MINOR! LSS 7 (
    echo [ERROR] Python version !PYTHON_VERSION! is too old. Minimum required is 3.7.
    goto :cleanup
)

echo [INFO] Python version !PYTHON_VERSION! is compatible.

REM Clone repo if not exists
if not exist "!PROJECT_DIR!" (
    echo [INFO] Cloning repository...
    git clone !REPO_URL!
) else (
    echo [INFO] Project folder already exists. Skipping clone.
)

cd /d "!PROJECT_DIR!"

REM Create virtual environment
if not exist "!VENV_DIR!" (
    echo [INFO] Creating virtual environment...
    python -m venv "!VENV_DIR!"
)

REM Activate virtual environment
call "!VENV_DIR!\Scripts\activate.bat"
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment.
    goto :cleanup
)

REM Install dependencies
if exist requirements.txt (
    echo [INFO] Installing dependencies...
    pip install --upgrade pip
    pip install -r requirements.txt
) else (
    echo [WARNING] requirements.txt not found.
    goto :cleanup
)

echo [SUCCESS] Setup completed.

REM Run main script
if exist fpc.py (
    echo [INFO] Launching application...
    python fpc.py
) else (
    echo [WARNING] fpc.py not found.
    goto :cleanup
)

goto :eof

:cleanup
echo [INFO] Cleaning up...
exit /b 1
