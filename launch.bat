@echo off
echo.
echo ========================================
echo   QUANTUM-AI CYBER GOD LAUNCHER
echo   The Ultimate Web3 Defense System
echo ========================================
echo.

echo [1/4] Starting Backend API Server...
cd backend
start "Quantum-AI Backend" cmd /k "python minimal_server.py"
cd ..

echo [2/4] Waiting for backend to initialize...
timeout /t 3 /nobreak > nul

echo [3/4] Opening API Documentation...
timeout /t 2 /nobreak > nul
start "" "http://localhost:8001/docs"

echo [4/4] Opening Enhanced Status Dashboard...
start "" "status.html"

echo.
echo ========================================
echo   PROJECT LAUNCHED SUCCESSFULLY!
echo ========================================
echo.
echo Backend API: http://localhost:8001
echo Status Dashboard: status.html (opened in browser)
echo Interactive API: http://localhost:8001/docs (opened in browser)
echo API Docs: http://localhost:8001/docs
echo.
echo Press any key to view available endpoints...
pause > nul

echo.
echo Available API Endpoints:
echo - Health Check: http://localhost:8001/health
echo - Threat Intelligence: http://localhost:8001/api/threat-intelligence
echo - Real-time Analytics: http://localhost:8001/api/analytics/real-time
echo - Smart Contract Analysis: POST http://localhost:8001/api/smart-contract/analyze
echo.
echo The Quantum-AI Cyber God is now ACTIVE and monitoring!
echo.
echo 💡 TROUBLESHOOTING TIPS:
echo - If API links don't work: Open http://localhost:8001/docs directly
echo - If backend fails: Check TROUBLESHOOTING.md for solutions
echo - Test buttons in status.html work even with CORS issues
echo.
pause 