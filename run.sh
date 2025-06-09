#!/bin/bash
# Check if the virtual environment exists
if [ ! -d "$HOME/venv_squeezy" ]; then
    echo "Virtual environment not found. Creating a new one..."
    python3 -m venv "$HOME/venv_squeezy"
else
    echo "Virtual environment found."
fi
source "$HOME/venv/bin/activate"

pip install -r src/requirements.txt

# Run pytest and check its exit status
echo "Running tests..."
pytest
if [ $? -eq 0 ]; then
    echo "Tests passed. Proceeding to run the application."
    cd src
    python3 main.py
else
    echo "Tests failed. Aborting further execution."
    exit 1
fi