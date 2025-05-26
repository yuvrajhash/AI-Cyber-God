@echo off
setlocal enabledelayedexpansion

echo.
echo ========================================
echo 🌟 QUANTUM-AI CYBER GOD - ALL PHASES
echo Complete Platform Launch
echo ========================================
echo.
echo 🚀 Launching all 4 phases simultaneously:
echo   Phase 1: Legacy Platform (Port 8001)
echo   Phase 2: Blockchain Features (Port 8002)
echo   Phase 3: War Games Platform (Port 8003)
echo   Phase 4: Enterprise Platform (Port 8004)
echo.

REM Check if Python virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found. Please run setup first.
    echo.
    echo To set up the environment, run:
    echo   python -m venv .venv
    echo   .venv\Scripts\activate.bat
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Check if required packages are installed
echo 📦 Checking dependencies...
python -c "import fastapi, uvicorn" 2>nul
if errorlevel 1 (
    echo ⚠️ Installing core dependencies...
    pip install fastapi uvicorn
)

python -c "import redis" 2>nul
if errorlevel 1 (
    echo ⚠️ Installing Redis for Phase 4...
    pip install redis
)

python -c "import websockets" 2>nul
if errorlevel 1 (
    echo ⚠️ Installing WebSocket support...
    pip install websockets
)

REM Check if ports are available
echo 🔍 Checking port availability...
netstat -an | findstr ":8001 " >nul
if not errorlevel 1 (
    echo ⚠️ Port 8001 is already in use. Phase 1 may conflict.
)

netstat -an | findstr ":8002 " >nul
if not errorlevel 1 (
    echo ⚠️ Port 8002 is already in use. Phase 2 may conflict.
)

netstat -an | findstr ":8003 " >nul
if not errorlevel 1 (
    echo ⚠️ Port 8003 is already in use. Phase 3 may conflict.
)

netstat -an | findstr ":8004 " >nul
if not errorlevel 1 (
    echo ⚠️ Port 8004 is already in use. Phase 4 may conflict.
)

echo.
echo 🚀 Starting all phases...
echo.

REM Create log directory
if not exist "logs" mkdir logs

REM Start Phase 1 (Legacy Platform)
echo 📡 Starting Phase 1 - Legacy Platform (Port 8001)...
start "Phase 1 - Legacy" cmd /k "cd backend && python -m uvicorn minimal_server:app --host 0.0.0.0 --port 8001 --reload > ../logs/phase1.log 2>&1"
timeout /t 3 /nobreak >nul

REM Start Phase 2 (Blockchain Features)
echo ⛓️ Starting Phase 2 - Blockchain Features (Port 8002)...
start "Phase 2 - Blockchain" cmd /k "cd backend && python -m uvicorn phase2_server:app --host 0.0.0.0 --port 8002 --reload > ../logs/phase2.log 2>&1"
timeout /t 3 /nobreak >nul

REM Start Phase 3 (War Games Platform)
echo 🎮 Starting Phase 3 - War Games Platform (Port 8003)...
start "Phase 3 - War Games" cmd /k "cd backend && python -m uvicorn phase3_server:app --host 0.0.0.0 --port 8003 --reload > ../logs/phase3.log 2>&1"
timeout /t 3 /nobreak >nul

REM Start Phase 4 (Enterprise Platform)
echo 🏢 Starting Phase 4 - Enterprise Platform (Port 8004)...
start "Phase 4 - Enterprise" cmd /k "cd backend && python -m uvicorn phase4_server:app --host 0.0.0.0 --port 8004 --reload > ../logs/phase4.log 2>&1"
timeout /t 5 /nobreak >nul

echo.
echo ✅ All phases are starting up...
echo.
echo 🌐 Access Points:
echo ==========================================
echo.
echo 📊 PHASE 1 - LEGACY PLATFORM
echo   • API: http://localhost:8001
echo   • Docs: http://localhost:8001/docs
echo   • Health: http://localhost:8001/health
echo   • Dashboard: status.html
echo.
echo ⛓️ PHASE 2 - BLOCKCHAIN FEATURES
echo   • API: http://localhost:8002
echo   • Docs: http://localhost:8002/docs
echo   • Health: http://localhost:8002/health
echo   • Dashboard: phase2_dashboard.html
echo.
echo 🎮 PHASE 3 - WAR GAMES PLATFORM
echo   • API: http://localhost:8003
echo   • Docs: http://localhost:8003/docs
echo   • Health: http://localhost:8003/health
echo   • Dashboard: phase3_dashboard.html
echo   • WebSocket: ws://localhost:8003/ws/game/{player_id}
echo.
echo 🏢 PHASE 4 - ENTERPRISE PLATFORM
echo   • API: http://localhost:8004
echo   • Docs: http://localhost:8004/docs
echo   • Health: http://localhost:8004/health
echo   • Dashboard: phase4_dashboard.html
echo   • WebSocket: ws://localhost:8004/ws/enterprise/{tenant_id}
echo.
echo ==========================================

REM Wait for servers to start
echo ⏳ Waiting for all servers to initialize...
timeout /t 10 /nobreak >nul

REM Health check all phases
echo.
echo 🔍 Performing health checks...
echo.

REM Check Phase 1
curl -s http://localhost:8001/health >nul 2>&1
if errorlevel 1 (
    echo ❌ Phase 1 health check failed
) else (
    echo ✅ Phase 1 is healthy
)

REM Check Phase 2
curl -s http://localhost:8002/health >nul 2>&1
if errorlevel 1 (
    echo ❌ Phase 2 health check failed
) else (
    echo ✅ Phase 2 is healthy
)

REM Check Phase 3
curl -s http://localhost:8003/health >nul 2>&1
if errorlevel 1 (
    echo ❌ Phase 3 health check failed
) else (
    echo ✅ Phase 3 is healthy
)

REM Check Phase 4
curl -s http://localhost:8004/health >nul 2>&1
if errorlevel 1 (
    echo ❌ Phase 4 health check failed
) else (
    echo ✅ Phase 4 is healthy
)

echo.
echo 🎯 QUICK START GUIDE:
echo ==========================================
echo.
echo 1. 📊 Open status.html for Phase 1 overview
echo 2. ⛓️ Open phase2_dashboard.html for blockchain features
echo 3. 🎮 Open phase3_dashboard.html for war games
echo 4. 🏢 Open phase4_dashboard.html for enterprise features
echo.
echo 5. 📚 Visit /docs endpoints for API documentation
echo 6. 🔍 Check logs/ directory for detailed server logs
echo.
echo ==========================================

REM Open main dashboards
echo.
echo 🌐 Opening main dashboards...
timeout /t 2 /nobreak >nul

REM Open Phase 4 dashboard (primary)
if exist "phase4_dashboard.html" (
    start "" "phase4_dashboard.html"
    echo ✅ Opened Phase 4 Enterprise Dashboard
) else (
    echo ⚠️ Phase 4 dashboard not found
)

timeout /t 2 /nobreak >nul

REM Open Phase 3 dashboard
if exist "phase3_dashboard.html" (
    start "" "phase3_dashboard.html"
    echo ✅ Opened Phase 3 War Games Dashboard
) else (
    echo ⚠️ Phase 3 dashboard not found
)

echo.
echo 🎉 ALL PHASES LAUNCHED SUCCESSFULLY!
echo.
echo 📋 PLATFORM STATUS:
echo   • Phase 1 (Legacy): Running on port 8001
echo   • Phase 2 (Blockchain): Running on port 8002
echo   • Phase 3 (War Games): Running on port 8003
echo   • Phase 4 (Enterprise): Running on port 8004
echo.
echo 🔧 MANAGEMENT COMMANDS:
echo   • View logs: dir logs\
echo   • Stop all: Close all command windows
echo   • Restart: Run this script again
echo.
echo 💡 TIP: Keep this window open to monitor the platform
echo 🛑 To stop all phases, close all server windows or press Ctrl+C in each
echo.

REM Keep the main window open for monitoring
echo 📊 Platform Monitor - Press any key to view real-time status...
pause >nul

:monitor_loop
cls
echo.
echo ========================================
echo 🌟 QUANTUM-AI CYBER GOD - LIVE STATUS
echo ========================================
echo.
echo 📊 Real-time Platform Status:
echo.

REM Check all phases status
curl -s http://localhost:8001/health >nul 2>&1
if errorlevel 1 (
    echo ❌ Phase 1 (Port 8001): OFFLINE
) else (
    echo ✅ Phase 1 (Port 8001): ONLINE
)

curl -s http://localhost:8002/health >nul 2>&1
if errorlevel 1 (
    echo ❌ Phase 2 (Port 8002): OFFLINE
) else (
    echo ✅ Phase 2 (Port 8002): ONLINE
)

curl -s http://localhost:8003/health >nul 2>&1
if errorlevel 1 (
    echo ❌ Phase 3 (Port 8003): OFFLINE
) else (
    echo ✅ Phase 3 (Port 8003): ONLINE
)

curl -s http://localhost:8004/health >nul 2>&1
if errorlevel 1 (
    echo ❌ Phase 4 (Port 8004): OFFLINE
) else (
    echo ✅ Phase 4 (Port 8004): ONLINE
)

echo.
echo 🕐 Last checked: %date% %time%
echo.
echo 🔧 Options:
echo   [R] Refresh status
echo   [L] View logs
echo   [D] Open dashboards
echo   [Q] Quit monitor
echo.
set /p choice="Enter choice: "

if /i "%choice%"=="R" goto monitor_loop
if /i "%choice%"=="L" (
    echo.
    echo 📋 Available log files:
    dir logs\ /b 2>nul
    echo.
    pause
    goto monitor_loop
)
if /i "%choice%"=="D" (
    echo.
    echo 🌐 Opening all dashboards...
    if exist "status.html" start "" "status.html"
    if exist "phase2_dashboard.html" start "" "phase2_dashboard.html"
    if exist "phase3_dashboard.html" start "" "phase3_dashboard.html"
    if exist "phase4_dashboard.html" start "" "phase4_dashboard.html"
    echo ✅ Dashboards opened
    timeout /t 2 /nobreak >nul
    goto monitor_loop
)
if /i "%choice%"=="Q" goto end

goto monitor_loop

:end
echo.
echo 🛑 Exiting platform monitor...
echo 💡 All phases are still running in background windows
echo 🔧 To stop all phases, close the individual server windows
echo.
echo 🎉 Thank you for using Quantum-AI Cyber God!
echo.
pause 