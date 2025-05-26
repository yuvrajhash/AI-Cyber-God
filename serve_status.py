#!/usr/bin/env python3
"""
Simple HTTP server to serve the Quantum-AI Cyber God status page
This avoids CORS issues when accessing the API from the browser
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

PORT = 3000

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def main():
    # Change to the project directory
    os.chdir(Path(__file__).parent)
    
    print("🚀 Starting Quantum-AI Cyber God Status Server...")
    print(f"📡 Server will run on: http://localhost:{PORT}")
    print("🌐 Status page will open automatically in your browser")
    print("⚡ This server enables full API functionality without CORS issues")
    print()
    
    try:
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            print(f"✅ Server started successfully on port {PORT}")
            
            # Open the status page in the default browser
            webbrowser.open(f'http://localhost:{PORT}/status.html')
            
            print("🛡️ Quantum-AI Cyber God Status Dashboard is now accessible!")
            print("📊 All API endpoints should work properly now")
            print()
            print("Press Ctrl+C to stop the server")
            print("=" * 50)
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        sys.exit(0)
    except OSError as e:
        if e.errno == 10048:  # Port already in use on Windows
            print(f"❌ Port {PORT} is already in use!")
            print("💡 Try closing other applications or use a different port")
            print("🔄 Or wait a moment and try again")
        else:
            print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 