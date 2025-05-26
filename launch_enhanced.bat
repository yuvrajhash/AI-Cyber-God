@echo off
echo.
echo ========================================
echo  🛡️ QUANTUM-AI CYBER GOD - ENHANCED 🛡️
echo     Phase 1: Real AI Implementation
echo ========================================
echo.

echo 🚀 Starting Enhanced AI Server with PyTorch/ML...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.7+ first.
    pause
    exit /b 1
)

echo ✅ Python found!

REM Check if required packages are installed
echo 📦 Checking AI dependencies...
python -c "import torch, sklearn, pandas, numpy" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Installing missing AI packages...
    python -m pip install torch scikit-learn pandas numpy matplotlib seaborn
    if errorlevel 1 (
        echo ❌ Failed to install AI packages!
        pause
        exit /b 1
    )
)

echo ✅ AI dependencies ready!

REM Start the enhanced server
echo.
echo 🧠 Initializing Enhanced AI Engine...
echo    - Quantum-Inspired Threat Classifier
echo    - Neural Contract Analyzer  
echo    - LSTM Predictive Engine
echo    - Reinforcement Learning Agent
echo.

cd backend
python enhanced_server.py

REM If server exits, show status
if errorlevel 1 (
    echo.
    echo ❌ Enhanced server encountered an error!
    echo 💡 Troubleshooting tips:
    echo    1. Check if all AI packages are installed
    echo    2. Ensure sufficient memory for ML models
    echo    3. Check the logs above for specific errors
    echo.
) else (
    echo.
    echo ✅ Enhanced server stopped gracefully
)

echo.
echo 📊 Enhanced Features Available:
echo    • Real PyTorch Neural Networks
echo    • Advanced Threat Prediction
echo    • Smart Contract AI Analysis
echo    • Reinforcement Learning Defense
echo    • Pattern Recognition & Anomaly Detection
echo.
echo 🌐 Enhanced API Endpoints:
echo    • http://localhost:8001/ai/status
echo    • http://localhost:8001/ai/analyze-threat
echo    • http://localhost:8001/ai/analyze-contract
echo    • http://localhost:8001/ai/predict-threats
echo    • http://localhost:8001/ai/defense-strategy
echo    • http://localhost:8001/ai/train
echo    • http://localhost:8001/docs (Enhanced API Documentation)
echo.

pause 