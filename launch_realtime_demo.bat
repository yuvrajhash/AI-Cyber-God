@echo off
echo ========================================
echo 🚀 QUANTUM-AI CYBER GOD - REAL-TIME DEMO
echo ========================================
echo.
echo 🔧 Initializing Enhanced AI System...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist ".venv" (
    echo 🔧 Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies if needed
echo 🔧 Checking dependencies...
python -c "import torch, sklearn, fastapi, uvicorn, requests" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing missing dependencies...
    python -m pip install -r requirements.txt
    python -m pip install requests
)

echo.
echo ✅ Dependencies ready!
echo.
echo 🚀 Starting Enhanced AI Server...
echo 📊 Server will run on: http://localhost:8001
echo 📚 API Documentation: http://localhost:8001/docs
echo.

REM Start the enhanced server in background
start /B python backend/enhanced_server.py

REM Wait for server to start
echo ⏳ Waiting for server to initialize...
timeout /t 5 /nobreak >nul

REM Test server connection
python -c "import requests; requests.get('http://localhost:8001/health')" >nul 2>&1
if errorlevel 1 (
    echo ❌ Server failed to start! Check logs.
    pause
    exit /b 1
)

echo ✅ Server is running!
echo.

REM Open documentation and status page
echo 🌐 Opening system interfaces...
start http://localhost:8001/docs
start status.html

echo.
echo ========================================
echo 🎯 REAL-TIME DEMO OPTIONS
echo ========================================
echo.
echo 1. Run AI Testing Suite
echo 2. Start Real-time Monitor
echo 3. Open API Documentation
echo 4. View System Status
echo 5. Exit Demo
echo.

:menu
set /p choice="Select option (1-5): "

if "%choice%"=="1" (
    echo.
    echo 🧪 Running AI Testing Suite...
    echo ========================================
    python test_realtime_ai.py
    echo.
    echo Press any key to return to menu...
    pause >nul
    goto menu
)

if "%choice%"=="2" (
    echo.
    echo 📊 Starting Real-time Monitor...
    echo ========================================
    echo Press Ctrl+C to return to menu
    python realtime_monitor.py
    goto menu
)

if "%choice%"=="3" (
    echo.
    echo 📚 Opening API Documentation...
    start http://localhost:8001/docs
    goto menu
)

if "%choice%"=="4" (
    echo.
    echo 🏥 System Status Check...
    echo ========================================
    python -c "import requests; import json; r=requests.get('http://localhost:8001/health'); print(json.dumps(r.json(), indent=2))"
    echo.
    echo Press any key to return to menu...
    pause >nul
    goto menu
)

if "%choice%"=="5" (
    echo.
    echo 🛑 Shutting down demo...
    taskkill /f /im python.exe >nul 2>&1
    echo ✅ Demo stopped. Thank you!
    pause
    exit /b 0
)

echo ❌ Invalid choice. Please select 1-5.
goto menu 