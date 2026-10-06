@echo off
chcp 65001 >nul
cd /d "%~dp0"

set PYTHON_EXE="%~dp0.venv\Scripts\python.exe"

if not exist %PYTHON_EXE% (
    echo [ERROR] Virtual environment python not found.
    pause
    exit /b 1
)

if "%~1"=="" (
    echo ========================================================
    echo   HEIC to PNG Quick Converter
    echo ========================================================
    echo.
    echo   How to use:
    echo   Drag and drop one or multiple .heic files or folders
    echo   directly onto this .bat file to convert them to PNG!
    echo.
    echo ========================================================
    echo.
    pause
    exit /b 0
)

echo Starting conversion...
%PYTHON_EXE% "%~dp0cli.py" %*

echo.
echo Press any key to exit...
pause >nul
