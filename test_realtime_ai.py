#!/usr/bin/env python3
"""
Real-time AI Testing Script for Quantum-AI Cyber God
Demonstrates live AI analysis capabilities
"""

import requests
import json
import time
from datetime import datetime

# Server configuration
BASE_URL = "http://localhost:8001"

def test_ai_status():
    """Test AI system status"""
    print("🔍 Testing AI System Status...")
    try:
        response = requests.get(f"{BASE_URL}/ai/status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ AI Status: {data['status']}")
            print(f"📊 Device: {data['device']}")
            print(f"🧠 Models Trained: {data['models_trained']}")
            print(f"📈 Metrics: {data['metrics']}")
            return True
        else:
            print(f"❌ AI Status Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False

def test_threat_analysis():
    """Test real-time threat analysis"""
    print("\n🛡️ Testing Real-time Threat Analysis...")
    
    threat_data = {
        "type": "smart_contract",
        "severity": 0.8,
        "confidence": 0.9,
        "description": "Suspicious smart contract deployment with unusual gas patterns and potential reentrancy vulnerability",
        "affected_systems": ["ethereum_mainnet", "polygon_network"],
        "impact_score": 0.85
    }
    
    try:
        response = requests.post(f"{BASE_URL}/ai/analyze-threat", json=threat_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Threat Analysis Complete!")
            print(f"🎯 Classification: {result.get('classification', 'N/A')}")
            print(f"⚠️ Risk Score: {result.get('risk_score', 'N/A')}")
            print(f"🔮 Quantum Analysis: {result.get('quantum_analysis', {}).get('threat_probability', 'N/A')}")
            print(f"🧠 Neural Insights: {result.get('neural_analysis', {}).get('pattern_detected', 'N/A')}")
            return True
        else:
            print(f"❌ Threat Analysis Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Analysis Error: {e}")
        return False

def test_contract_analysis():
    """Test smart contract vulnerability analysis"""
    print("\n🔍 Testing Smart Contract Analysis...")
    
    contract_code = """
    pragma solidity ^0.8.0;
    
    contract VulnerableContract {
        mapping(address => uint256) public balances;
        
        function withdraw() public {
            uint256 amount = balances[msg.sender];
            require(amount > 0, "No balance");
            
            // Vulnerable to reentrancy attack
            (bool success, ) = msg.sender.call{value: amount}("");
            require(success, "Transfer failed");
            
            balances[msg.sender] = 0;
        }
        
        function deposit() public payable {
            balances[msg.sender] += msg.value;
        }
    }
    """
    
    try:
        response = requests.post(f"{BASE_URL}/ai/analyze-contract", 
                               json={"contract_code": contract_code})
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Contract Analysis Complete!")
            print(f"🚨 Vulnerabilities Found: {len(result.get('vulnerabilities', []))}")
            print(f"⚠️ Risk Score: {result.get('risk_score', 'N/A')}")
            print(f"🧠 Neural Analysis: {result.get('neural_analysis', {}).get('vulnerability_patterns', 'N/A')}")
            
            # Show vulnerabilities
            for vuln in result.get('vulnerabilities', [])[:3]:  # Show first 3
                print(f"  🔴 {vuln.get('type', 'Unknown')}: {vuln.get('description', 'No description')}")
            
            return True
        else:
            print(f"❌ Contract Analysis Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Analysis Error: {e}")
        return False

def test_threat_prediction():
    """Test threat prediction capabilities"""
    print("\n🔮 Testing Threat Prediction...")
    
    try:
        response = requests.get(f"{BASE_URL}/ai/predict-threats?hours=12")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Threat Prediction Complete!")
            print(f"📊 Predicted Threats: {len(result.get('predictions', []))}")
            print(f"📈 Trend Analysis: {result.get('trend_analysis', {}).get('overall_trend', 'N/A')}")
            print(f"🎯 Confidence: {result.get('confidence', 'N/A')}")
            
            # Show top predictions
            for pred in result.get('predictions', [])[:3]:  # Show first 3
                print(f"  ⚡ {pred.get('threat_type', 'Unknown')}: {pred.get('probability', 'N/A')} probability")
            
            return True
        else:
            print(f"❌ Prediction Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Prediction Error: {e}")
        return False

def test_defense_strategy():
    """Test defense strategy generation"""
    print("\n🛡️ Testing Defense Strategy Generation...")
    
    defense_request = {
        "active_threats": 5,
        "avg_severity": 0.7,
        "system_health": 0.85,
        "additional_context": {
            "recent_attacks": ["reentrancy", "flash_loan"],
            "network": "ethereum"
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/ai/defense-strategy", json=defense_request)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Defense Strategy Generated!")
            print(f"🎯 Strategy Type: {result.get('strategy_type', 'N/A')}")
            print(f"⚡ Priority Level: {result.get('priority', 'N/A')}")
            print(f"🔧 Actions: {len(result.get('recommended_actions', []))}")
            
            # Show top actions
            for action in result.get('recommended_actions', [])[:3]:  # Show first 3
                print(f"  🔹 {action.get('action', 'Unknown')}: {action.get('description', 'No description')}")
            
            return True
        else:
            print(f"❌ Defense Strategy Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Strategy Error: {e}")
        return False

def main():
    """Run comprehensive real-time AI testing"""
    print("🚀 Quantum-AI Cyber God - Real-time AI Testing")
    print("=" * 60)
    print(f"⏰ Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Server: {BASE_URL}")
    print("=" * 60)
    
    # Test sequence
    tests = [
        ("AI System Status", test_ai_status),
        ("Threat Analysis", test_threat_analysis),
        ("Contract Analysis", test_contract_analysis),
        ("Threat Prediction", test_threat_prediction),
        ("Defense Strategy", test_defense_strategy)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        success = test_func()
        results.append((test_name, success))
        time.sleep(1)  # Brief pause between tests
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name:.<40} {status}")
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All AI systems operational! Real-time analysis ready!")
    else:
        print("⚠️ Some systems need attention. Check server logs.")
    
    print(f"⏰ Test Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main() 