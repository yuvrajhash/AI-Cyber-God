@echo off
echo.
echo 🎮 QUANTUM-AI CYBER GOD - PHASE 3 WAR GAMES PLATFORM 🎮
echo ================================================================
echo.
echo 🚀 Starting Phase 3 War Games Platform...
echo.
echo ⚔️  Features:
echo    • Competitive Cybersecurity Challenges
echo    • Real-time Leaderboards & Rankings
echo    • Team-based Competitions
echo    • Tournament System
echo    • Player Achievements & Progression
echo    • WebSocket Real-time Updates
echo.
echo 🌐 Access Points:
echo    • War Games Dashboard: phase3_dashboard.html
echo    • Phase 3 API: http://localhost:8003
echo    • API Documentation: http://localhost:8003/docs
echo    • Health Check: http://localhost:8003/health
echo    • Platform Status: http://localhost:8003/api/status/phase3
echo.
echo ================================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist ".venv" (
    echo 📦 Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo 📚 Installing dependencies...
pip install fastapi uvicorn websockets

REM Change to backend directory
cd backend

echo.
echo 🌐 Starting Phase 3 Server on port 8003...
echo.
echo 📊 Dashboard will open automatically...
echo 🔍 API Documentation: http://localhost:8003/docs
echo 💡 Health Check: http://localhost:8003/health
echo 📈 Platform Status: http://localhost:8003/api/status/phase3
echo.

REM Start the Phase 3 server in background
start /B python phase3_server.py

REM Wait a moment for server to start
timeout /t 3 /nobreak >nul

REM Open the Phase 3 dashboard
cd ..
start phase3_dashboard.html

echo.
echo ✅ Phase 3 War Games Platform is now running!
echo.
echo 🎯 Available Endpoints:
echo    • GET  /health - Health check
echo    • GET  /api/status/phase3 - Platform status
echo    • POST /api/players/register - Register new player
echo    • GET  /api/challenges - Get available challenges
echo    • GET  /api/leaderboard/global - Global leaderboard
echo    • POST /api/teams/create - Create new team
echo    • GET  /api/tournaments/active - Active tournaments
echo    • WS   /ws/game/{player_id} - Real-time game updates
echo.
echo 🏆 Ready for competitive cybersecurity challenges!
echo.
echo Press any key to stop the server...
pause >nul

REM Stop the server
echo.
echo 🛑 Stopping Phase 3 server...
taskkill /f /im python.exe >nul 2>&1

echo.
echo 👋 Phase 3 War Games Platform stopped.
echo Thank you for playing!
pause 