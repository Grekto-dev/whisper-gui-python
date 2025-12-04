@echo off
cd /d "%~dp0"

title Launcher Whisper GUI

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python not found!
    echo Please install Python and check the "Add Python to PATH" option during installation.
    echo.
    pause
    exit /b
)

echo Starting Whisper GUI...
python whisper_gui.py

if %errorlevel% neq 0 (
    echo.
    echo ---------------------------------------------------
    echo The program has terminated due to an error.
    echo Check the messages above.
    echo ---------------------------------------------------
    pause
)