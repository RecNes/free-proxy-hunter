#!/bin/bash

set -euo pipefail

REPO_URL="https://github.com/RecNes/free-proxy-hunter.git"
PROJECT_DIR="free-proxy-hunter"
VENV_DIR=".venv"
SCRIPT_NAME="$(basename "$0")"

PYTHON_BIN=$(command -v python3 || true)

if [ -z "$PYTHON_BIN" ]; then
    echo "Python3 is not installed. Please install Python 3.7 or higher."
    rm -- "$SCRIPT_NAME"
    exit 1
fi

PYTHON_VERSION=$("$PYTHON_BIN" -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')
PYTHON_MAJOR=$("$PYTHON_BIN" -c 'import sys; print(sys.version_info[0])')
PYTHON_MINOR=$("$PYTHON_BIN" -c 'import sys; print(sys.version_info[1])')

if [ "$PYTHON_MAJOR" -lt 3 ] || { [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 7 ]; }; then
    echo "Your Python version is $PYTHON_VERSION. This application requires Python 3.7 or higher."
    rm -- "$SCRIPT_NAME"
    exit 1
fi


if [ ! -d "$PROJECT_DIR" ]; then
    echo "Cloning the project..."
    git clone "$REPO_URL"
fi

cd "$PROJECT_DIR"

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
echo "Virtual environment activated."

if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "requirements.txt not found!"
    exit 1
fi

echo "Setup complete."

if [ -f "fpc.py" ]; then
    echo "Launching the application..."
    python fpc.py
else
    echo "fpc.py not found!"
    exit 1
fi
