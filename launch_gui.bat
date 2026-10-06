@echo off
cd /d "%~dp0"

set PYTHON_EXE="%~dp0.venv\Scripts\pythonw.exe"
if not exist %PYTHON_EXE% (
    set PYTHON_EXE="%~dp0.venv\Scripts\python.exe"
)

if not exist %PYTHON_EXE% (
    echo [ERROR] Virtual environment python not found.
    pause
    exit /b 1
)

start "" %PYTHON_EXE% "%~dp0gui.py"
exit
