@echo off
title TTG Genesis Enhanced - Startup Script

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                                                                              ║
echo ║    🎮 TTG GENESIS ENHANCED - STARTUP SCRIPT                                 ║
echo ║                                                                              ║
echo ║    Transform your imagination into playable UE5 game worlds!                ║
echo ║                                                                              ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

echo 🔍 Checking system requirements...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo 💡 Please install Python from https://python.org
    echo    Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✅ Python is installed
python --version

echo.
echo 🔍 Checking for required packages...

REM Try to import Flask
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Flask is not installed
    echo 📦 Installing required packages...
    pip install flask flask-cors requests pyyaml
    if %errorlevel% neq 0 (
        echo ❌ Failed to install packages
        echo 💡 Try running as administrator or use: python -m pip install flask flask-cors requests pyyaml
        pause
        exit /b 1
    )
)

echo ✅ Required packages are available

echo.
echo 🚀 Starting TTG Genesis Enhanced Server...
echo.

REM Navigate to backend directory
cd /d "%~dp0\02-Web-Interface\backend"

REM Check if test server exists and run it first
if exist "test_server.py" (
    echo 🧪 Running system test first...
    python test_server.py
    if %errorlevel% neq 0 (
        echo ❌ System test failed
        pause
        exit /b 1
    )
)

REM Check if enhanced server exists
if exist "enhanced-start-server.py" (
    echo 🌟 Starting Enhanced Server with full features...
    python enhanced-start-server.py
) else if exist "enhanced_app.py" (
    echo 🌟 Starting Enhanced App...
    python enhanced_app.py
) else if exist "simple-demo.py" (
    echo 🎮 Starting Demo Server...
    python simple-demo.py
) else (
    echo ❌ No server files found!
    echo 💡 Make sure you're running this from the TTG-Genesis-Complete folder
    echo    and all files are properly extracted.
    pause
    exit /b 1
)

echo.
echo 🛑 Server stopped
pause
