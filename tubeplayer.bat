@echo off

if not exist "TubePlayer\Scripts\activate.bat" (
    python -m venv TubePlayer
)

call TubePlayer\Scripts\activate.bat

python setup\install.py

python yt.py
