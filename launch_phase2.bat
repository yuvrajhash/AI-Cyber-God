@echo off
echo.
echo ========================================
echo 🚀 QUANTUM-AI CYBER GOD - PHASE 2 🚀
echo ========================================
echo.
echo Advanced Blockchain Integration
echo Real-time Monitoring & Analytics
echo Multi-chain DeFi Security
echo.

cd /d "%~dp0"

echo 🔧 Checking Python environment...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python not found! Please install Python 3.8+
    pause
    exit /b 1
)

echo.
echo 📦 Installing/Updating dependencies...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo 🌐 Starting Phase 2 Server on port 8002...
echo.
echo 📊 Features Available:
echo   • Real-time blockchain monitoring
echo   • Multi-chain Web3 integration  
echo   • Advanced DeFi security analysis
echo   • Live threat analytics dashboard
echo   • MEV opportunity detection
echo   • Flash loan monitoring
echo   • Smart contract vulnerability scanning
echo.
echo 🔗 Access Points:
echo   • API Server: http://localhost:8002
echo   • Health Check: http://localhost:8002/health
echo   • API Docs: http://localhost:8002/docs
echo   • Phase 2 Status: http://localhost:8002/api/status/phase2
echo.

cd backend
python phase2_server.py

echo.
echo 🛑 Phase 2 server stopped.
pause 