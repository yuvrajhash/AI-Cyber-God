# 🛠️ QUANTUM-AI CYBER GOD - TROUBLESHOOTING GUIDE

## 🚀 Quick Fix: Launch Issues

### Problem: "API links not working" or "CORS errors"

**✅ SOLUTION 1: Use Interactive API Documentation**
1. Open your browser
2. Go to: `http://localhost:8001/docs`
3. Test all endpoints directly in the Swagger UI interface

**✅ SOLUTION 2: Test API Endpoints Manually**
1. Open new browser tabs
2. Copy and paste these URLs directly:
   - `http://localhost:8001/health`
   - `http://localhost:8001/api/threat-intelligence`
   - `http://localhost:8001/api/analytics/real-time`

**✅ SOLUTION 3: Use the Test Buttons**
1. Open `status.html` in your browser
2. Click the "Test" buttons next to each API endpoint
3. View responses directly in the page

## 🔧 Backend Issues

### Problem: "Backend not responding" or "Connection failed"

**Check if backend is running:**
```bash
curl http://localhost:8001/health
```

**If not running, start it manually:**
```bash
cd backend
python minimal_server.py
```

**Alternative start method:**
```bash
cd backend
python -m uvicorn minimal_server:app --host 0.0.0.0 --port 8001
```

### Problem: "Python not found" or "Module not found"

**Install required packages:**
```bash
python -m pip install fastapi uvicorn
```

**Check Python installation:**
```bash
python --version
```

## 🌐 Browser Issues

### Problem: "Page not loading" or "File not found"

**Method 1: Direct file access**
- Navigate to your project folder
- Double-click `status.html`

**Method 2: Use launch script**
- Double-click `launch.bat`
- Wait for both windows to open

**Method 3: Manual browser navigation**
- Open browser
- Press Ctrl+O (or Cmd+O on Mac)
- Navigate to project folder
- Select `status.html`

## 🔍 Port Conflicts

### Problem: "Port already in use" or "Address already in use"

**Check what's using port 8001:**
```bash
netstat -an | findstr :8001
```

**Use different port:**
1. Edit `backend/minimal_server.py`
2. Change `port=8001` to `port=8002`
3. Update `status.html` API_BASE to `http://localhost:8002`

## 📊 API Testing Methods

### Method 1: Browser Direct Access
- Open: `http://localhost:8001/docs`
- Click "Try it out" on any endpoint
- Click "Execute" to test

### Method 2: Command Line Testing
```bash
# Health check
curl http://localhost:8001/health

# Threat intelligence
curl http://localhost:8001/api/threat-intelligence

# Analytics
curl http://localhost:8001/api/analytics/real-time
```

### Method 3: Status Page Testing
- Open `status.html`
- Click "Test" buttons
- View JSON responses inline

## 🚨 Emergency Reset

### If everything fails:

1. **Close all terminal windows**
2. **Restart your computer** (clears all ports)
3. **Navigate to project folder**
4. **Run these commands in order:**

```bash
# Install dependencies
python -m pip install fastapi uvicorn

# Start backend
cd backend
python minimal_server.py
```

5. **In a new terminal/command prompt:**
```bash
# Test backend
curl http://localhost:8001/health
```

6. **Open status page:**
   - Double-click `status.html`
   - Or open `http://localhost:8001/docs`

## ✅ Success Indicators

**Backend is working when:**
- ✅ Terminal shows: "Uvicorn running on http://0.0.0.0:8001"
- ✅ `curl http://localhost:8001/health` returns JSON
- ✅ Browser shows API docs at `http://localhost:8001/docs`

**Frontend is working when:**
- ✅ `status.html` opens in browser
- ✅ Status indicators are green/pulsing
- ✅ Test buttons show JSON responses
- ✅ API links open in new tabs

## 🎯 Quick Verification Commands

```bash
# Check if backend is running
curl http://localhost:8001/health

# Check if Python is available
python --version

# Check if required packages are installed
python -c "import fastapi, uvicorn; print('All packages available')"

# Test all endpoints quickly
curl http://localhost:8001/health && curl http://localhost:8001/api/threat-intelligence && curl http://localhost:8001/api/analytics/real-time
```

## 🆘 Still Having Issues?

1. **Check the terminal output** for error messages
2. **Ensure Python 3.7+ is installed**
3. **Try running commands one by one** instead of using the batch file
4. **Check Windows Firewall** isn't blocking localhost connections
5. **Try a different browser** (Chrome, Firefox, Edge)

## 🏆 Expected Results

When everything is working correctly:

- **Backend**: JSON responses from all API endpoints
- **Frontend**: Interactive status page with working test buttons
- **Documentation**: Swagger UI accessible at `/docs`
- **Real-time**: Status indicators updating automatically

**🛡️ The Quantum-AI Cyber God should be fully operational!** ⚡ 