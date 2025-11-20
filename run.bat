@echo off
REM Convenience batch script to create venv, install deps, and run the app
IF NOT EXIST .venv (
    python -m venv .venv
)

call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
