#!/usr/bin/env python3
"""
Real-time Monitoring Dashboard for Quantum-AI Cyber God
Live system status and AI metrics visualization
"""

import requests
import json
import time
import os
from datetime import datetime

# Server configuration
BASE_URL = "http://localhost:8001"

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_system_status():
    """Get comprehensive system status"""
    try:
        # Health check
        health_response = requests.get(f"{BASE_URL}/health", timeout=5)
        health_data = health_response.json() if health_response.status_code == 200 else {}
        
        # AI status
        ai_response = requests.get(f"{BASE_URL}/ai/status", timeout=5)
        ai_data = ai_response.json() if ai_response.status_code == 200 else {}
        
        # Real-time analytics
        analytics_response = requests.get(f"{BASE_URL}/api/analytics/real-time", timeout=5)
        analytics_data = analytics_response.json() if analytics_response.status_code == 200 else {}
        
        return {
            'health': health_data,
            'ai': ai_data,
            'analytics': analytics_data,
            'timestamp': datetime.now()
        }
    except Exception as e:
        return {
            'error': str(e),
            'timestamp': datetime.now()
        }

def format_uptime(seconds):
    """Format uptime in human readable format"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        return f"{seconds/60:.1f}m"
    else:
        return f"{seconds/3600:.1f}h"

def display_dashboard(status_data):
    """Display the real-time dashboard"""
    clear_screen()
    
    print("🚀 QUANTUM-AI CYBER GOD - REAL-TIME MONITORING DASHBOARD")
    print("=" * 80)
    print(f"⏰ Last Update: {status_data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    if 'error' in status_data:
        print(f"❌ CONNECTION ERROR: {status_data['error']}")
        print("🔄 Retrying connection...")
        return
    
    # System Health Section
    health = status_data.get('health', {})
    print("\n🏥 SYSTEM HEALTH")
    print("-" * 40)
    
    if health:
        status_icon = "🟢" if health.get('status') == 'healthy' else "🔴"
        print(f"{status_icon} Status: {health.get('status', 'Unknown').upper()}")
        print(f"⏱️  Uptime: {format_uptime(health.get('uptime_seconds', 0))}")
        print(f"📊 Requests: {health.get('requests_processed', 0)}")
        print(f"🔧 Version: {health.get('version', 'Unknown')}")
        
        # Services status
        services = health.get('services', {})
        print(f"\n🔧 SERVICES STATUS")
        for service, status in services.items():
            icon = "🟢" if status else "🔴"
            print(f"  {icon} {service.replace('_', ' ').title()}: {'Online' if status else 'Offline'}")
    else:
        print("🔴 No health data available")
    
    # AI System Section
    ai = status_data.get('ai', {})
    print(f"\n🧠 AI SYSTEM STATUS")
    print("-" * 40)
    
    if ai:
        ai_status_icon = "🟢" if ai.get('status') == 'operational' else "🟡" if ai.get('status') == 'initializing' else "🔴"
        print(f"{ai_status_icon} AI Status: {ai.get('status', 'Unknown').upper()}")
        print(f"💻 Device: {ai.get('device', 'Unknown')}")
        print(f"🎓 Models Trained: {'Yes' if ai.get('models_trained') else 'No'}")
        
        # AI Metrics
        metrics = ai.get('metrics', {})
        if metrics:
            print(f"\n📈 AI METRICS")
            print(f"  🎯 Threats Analyzed: {metrics.get('total_threats_analyzed', 0)}")
            print(f"  🔍 Contracts Scanned: {metrics.get('contracts_scanned', 0)}")
            print(f"  🔮 Predictions Made: {metrics.get('predictions_made', 0)}")
            print(f"  🛡️  Defense Actions: {metrics.get('defense_actions_recommended', 0)}")
            print(f"  ⚡ Avg Response Time: {metrics.get('avg_response_time_ms', 0):.1f}ms")
    else:
        print("🔴 No AI data available")
    
    # Real-time Analytics Section
    analytics = status_data.get('analytics', {})
    print(f"\n📊 REAL-TIME ANALYTICS")
    print("-" * 40)
    
    if analytics:
        print(f"🚨 Active Threats: {analytics.get('active_threats', 0)}")
        print(f"⚠️  Avg Severity: {analytics.get('avg_severity', 0):.2f}")
        print(f"💚 System Health: {analytics.get('system_health', 0):.1%}")
        print(f"🔄 Scan Rate: {analytics.get('scan_rate_per_minute', 0)}/min")
        
        # Recent threats
        recent_threats = analytics.get('recent_threats', [])
        if recent_threats:
            print(f"\n🚨 RECENT THREATS")
            for threat in recent_threats[:5]:  # Show last 5
                severity_icon = "🔴" if threat.get('severity', 0) > 0.7 else "🟡" if threat.get('severity', 0) > 0.4 else "🟢"
                print(f"  {severity_icon} {threat.get('type', 'Unknown')} - {threat.get('description', 'No description')[:50]}...")
    else:
        print("🔴 No analytics data available")
    
    # API Endpoints Status
    print(f"\n🌐 API ENDPOINTS")
    print("-" * 40)
    endpoints = [
        ("/health", "Health Check"),
        ("/ai/status", "AI Status"),
        ("/ai/analyze-threat", "Threat Analysis"),
        ("/ai/analyze-contract", "Contract Analysis"),
        ("/ai/predict-threats", "Threat Prediction"),
        ("/ai/defense-strategy", "Defense Strategy"),
        ("/docs", "API Documentation")
    ]
    
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=2)
            icon = "🟢" if response.status_code == 200 else "🟡" if response.status_code < 500 else "🔴"
            print(f"  {icon} {description}: {BASE_URL}{endpoint}")
        except:
            print(f"  🔴 {description}: {BASE_URL}{endpoint}")
    
    print(f"\n🔄 Auto-refresh in 5 seconds... (Ctrl+C to exit)")
    print("=" * 80)

def main():
    """Main monitoring loop"""
    print("🚀 Starting Quantum-AI Cyber God Real-time Monitor...")
    print("🔄 Connecting to server...")
    
    try:
        while True:
            status_data = get_system_status()
            display_dashboard(status_data)
            time.sleep(5)  # Refresh every 5 seconds
            
    except KeyboardInterrupt:
        clear_screen()
        print("\n👋 Monitoring stopped by user")
        print("🛡️  Quantum-AI Cyber God monitoring session ended")
        print(f"⏰ Session ended: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        print(f"\n❌ Monitoring error: {e}")

if __name__ == "__main__":
    main() 