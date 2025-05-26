@echo off
echo.
echo ========================================
echo 🏢 QUANTUM-AI CYBER GOD - PHASE 4
echo Enterprise Platform Launch
echo ========================================
echo.

REM Check if Python virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found. Please run setup first.
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Check if required packages are installed
echo 📦 Checking dependencies...
python -c "import fastapi, uvicorn, redis" 2>nul
if errorlevel 1 (
    echo ⚠️ Installing missing dependencies...
    pip install redis
)

REM Start Phase 4 backend server
echo.
echo 🚀 Starting Phase 4 Enterprise Backend Server...
echo 📍 Server will be available at: http://localhost:8004
echo 📊 Enterprise Dashboard: http://localhost:8004/docs
echo.
echo 🏢 Enterprise Features:
echo   • Multi-tenant Architecture
echo   • Custom Threat Models
echo   • Advanced Analytics
echo   • API Rate Limiting
echo   • Compliance Auditing
echo   • Integration Hub
echo.
echo 💡 Press Ctrl+C to stop the server
echo.

REM Start the server
cd backend
python -m uvicorn phase4_server:app --host 0.0.0.0 --port 8004 --reload

echo.
echo 🛑 Phase 4 Enterprise Platform stopped.
pause 