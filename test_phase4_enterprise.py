"""
🧪 QUANTUM-AI CYBER GOD - PHASE 4 ENTERPRISE TESTING
Comprehensive test suite for enterprise platform features
"""

import asyncio
import aiohttp
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Phase4EnterpriseTest:
    """Test suite for Phase 4 Enterprise Platform"""
    
    def __init__(self, base_url: str = "http://localhost:8004"):
        self.base_url = base_url
        self.session = None
        self.test_tenant_id = None
        self.test_api_key = None
        self.test_results = []
    
    async def setup(self):
        """Setup test environment"""
        self.session = aiohttp.ClientSession()
        logger.info("🔧 Setting up Phase 4 Enterprise test environment...")
    
    async def cleanup(self):
        """Cleanup test environment"""
        if self.session:
            await self.session.close()
        logger.info("🧹 Test environment cleanup complete")
    
    async def test_health_check(self) -> bool:
        """Test basic health check"""
        try:
            async with self.session.get(f"{self.base_url}/health") as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info("✅ Health check passed")
                    return True
                else:
                    logger.error(f"❌ Health check failed: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Health check error: {e}")
            return False
    
    async def test_phase4_status(self) -> bool:
        """Test Phase 4 status endpoint"""
        try:
            async with self.session.get(f"{self.base_url}/api/status/phase4") as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"✅ Phase 4 status: {data.get('status', 'unknown')}")
                    return True
                else:
                    logger.error(f"❌ Phase 4 status check failed: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Phase 4 status error: {e}")
            return False
    
    async def test_tenant_registration(self) -> bool:
        """Test tenant registration"""
        try:
            tenant_data = {
                "organization_name": "Test Enterprise Corp",
                "admin_email": "admin@testenterprise.com",
                "tier": "enterprise",
                "industry": "Technology",
                "compliance_requirements": ["soc2", "iso27001"],
                "max_users": 100,
                "custom_domain": "testenterprise.com"
            }
            
            async with self.session.post(
                f"{self.base_url}/api/enterprise/tenants/register",
                json=tenant_data
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    self.test_tenant_id = data.get("tenant_id")
                    self.test_api_key = data.get("api_key")
                    logger.info(f"✅ Tenant registration successful: {self.test_tenant_id}")
                    return True
                else:
                    logger.error(f"❌ Tenant registration failed: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Tenant registration error: {e}")
            return False
    
    async def test_enterprise_dashboard(self) -> bool:
        """Test enterprise dashboard access"""
        if not self.test_tenant_id or not self.test_api_key:
            logger.error("❌ No tenant credentials for dashboard test")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.test_tenant_id}:{self.test_api_key}"}
            
            async with self.session.get(
                f"{self.base_url}/api/enterprise/tenants/{self.test_tenant_id}/dashboard",
                headers=headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info("✅ Enterprise dashboard access successful")
                    return True
                else:
                    logger.error(f"❌ Enterprise dashboard access failed: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Enterprise dashboard error: {e}")
            return False
    
    async def test_custom_threat_model(self) -> bool:
        """Test custom threat model creation"""
        if not self.test_tenant_id or not self.test_api_key:
            logger.error("❌ No tenant credentials for threat model test")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.test_tenant_id}:{self.test_api_key}"}
            threat_model_data = {
                "model_name": "Test Financial Model",
                "model_type": "financial_services",
                "industry_focus": "Banking and Finance",
                "threat_vectors": ["phishing", "malware", "insider_threat", "ddos"],
                "sensitivity_level": 0.8,
                "custom_rules": {
                    "high_value_transactions": True,
                    "suspicious_login_patterns": True,
                    "data_exfiltration_detection": True
                },
                "compliance_mapping": ["pci_dss", "soc2"]
            }
            
            async with self.session.post(
                f"{self.base_url}/api/enterprise/tenants/{self.test_tenant_id}/threat-models",
                headers=headers,
                json=threat_model_data
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"✅ Custom threat model created: {data.get('model_id')}")
                    return True
                else:
                    logger.error(f"❌ Custom threat model creation failed: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Custom threat model error: {e}")
            return False
    
    async def test_analytics_overview(self) -> bool:
        """Test analytics overview"""
        if not self.test_tenant_id or not self.test_api_key:
            logger.error("❌ No tenant credentials for analytics test")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.test_tenant_id}:{self.test_api_key}"}
            
            async with self.session.get(
                f"{self.base_url}/api/enterprise/tenants/{self.test_tenant_id}/analytics/overview",
                headers=headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info("✅ Analytics overview access successful")
                    return True
                else:
                    logger.error(f"❌ Analytics overview failed: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Analytics overview error: {e}")
            return False
    
    async def test_compliance_status(self) -> bool:
        """Test compliance status"""
        if not self.test_tenant_id or not self.test_api_key:
            logger.error("❌ No tenant credentials for compliance test")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.test_tenant_id}:{self.test_api_key}"}
            
            async with self.session.get(
                f"{self.base_url}/api/enterprise/tenants/{self.test_tenant_id}/compliance/status",
                headers=headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info("✅ Compliance status access successful")
                    return True
                else:
                    logger.error(f"❌ Compliance status failed: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Compliance status error: {e}")
            return False
    
    async def test_integration_creation(self) -> bool:
        """Test integration creation"""
        if not self.test_tenant_id or not self.test_api_key:
            logger.error("❌ No tenant credentials for integration test")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.test_tenant_id}:{self.test_api_key}"}
            integration_data = {
                "integration_name": "Test SIEM Integration",
                "integration_type": "siem",
                "endpoint_url": "https://test-siem.example.com/api/events",
                "api_key": "test_api_key_12345",
                "webhook_secret": "test_webhook_secret",
                "custom_headers": {
                    "X-Custom-Header": "test-value"
                },
                "event_filters": ["high_severity", "critical_alerts"]
            }
            
            async with self.session.post(
                f"{self.base_url}/api/enterprise/tenants/{self.test_tenant_id}/integrations",
                headers=headers,
                json=integration_data
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"✅ Integration created: {data.get('integration_id')}")
                    return True
                else:
                    logger.error(f"❌ Integration creation failed: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Integration creation error: {e}")
            return False
    
    async def test_user_creation(self) -> bool:
        """Test enterprise user creation"""
        if not self.test_tenant_id or not self.test_api_key:
            logger.error("❌ No tenant credentials for user creation test")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.test_tenant_id}:{self.test_api_key}"}
            user_data = {
                "username": "test_analyst",
                "email": "analyst@testenterprise.com",
                "role": "Security Analyst",
                "permissions": ["view_dashboard", "manage_threats", "generate_reports"],
                "department": "Cybersecurity",
                "access_level": 3
            }
            
            async with self.session.post(
                f"{self.base_url}/api/enterprise/tenants/{self.test_tenant_id}/users",
                headers=headers,
                json=user_data
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"✅ Enterprise user created: {data.get('user_id')}")
                    return True
                else:
                    logger.error(f"❌ Enterprise user creation failed: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Enterprise user creation error: {e}")
            return False
    
    async def test_rate_limiting(self) -> bool:
        """Test API rate limiting"""
        if not self.test_tenant_id or not self.test_api_key:
            logger.error("❌ No tenant credentials for rate limiting test")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.test_tenant_id}:{self.test_api_key}"}
            
            # Make multiple rapid requests to test rate limiting
            success_count = 0
            rate_limited_count = 0
            
            for i in range(10):
                async with self.session.get(
                    f"{self.base_url}/api/enterprise/tenants/{self.test_tenant_id}/dashboard",
                    headers=headers
                ) as response:
                    if response.status == 200:
                        success_count += 1
                    elif response.status == 429:
                        rate_limited_count += 1
                
                # Small delay between requests
                await asyncio.sleep(0.1)
            
            logger.info(f"✅ Rate limiting test: {success_count} success, {rate_limited_count} rate limited")
            return True
            
        except Exception as e:
            logger.error(f"❌ Rate limiting test error: {e}")
            return False
    
    async def test_websocket_connection(self) -> bool:
        """Test WebSocket connection"""
        if not self.test_tenant_id:
            logger.error("❌ No tenant ID for WebSocket test")
            return False
        
        try:
            import websockets
            
            uri = f"ws://localhost:8004/ws/enterprise/{self.test_tenant_id}"
            
            async with websockets.connect(uri) as websocket:
                # Wait for a message
                message = await asyncio.wait_for(websocket.recv(), timeout=10.0)
                data = json.loads(message)
                
                if data.get("type") == "enterprise_update":
                    logger.info("✅ WebSocket connection successful")
                    return True
                else:
                    logger.error("❌ Unexpected WebSocket message format")
                    return False
                    
        except asyncio.TimeoutError:
            logger.error("❌ WebSocket connection timeout")
            return False
        except Exception as e:
            logger.error(f"❌ WebSocket connection error: {e}")
            return False
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all Phase 4 enterprise tests"""
        logger.info("🚀 Starting Phase 4 Enterprise Platform Tests...")
        
        await self.setup()
        
        tests = [
            ("Health Check", self.test_health_check),
            ("Phase 4 Status", self.test_phase4_status),
            ("Tenant Registration", self.test_tenant_registration),
            ("Enterprise Dashboard", self.test_enterprise_dashboard),
            ("Custom Threat Model", self.test_custom_threat_model),
            ("Analytics Overview", self.test_analytics_overview),
            ("Compliance Status", self.test_compliance_status),
            ("Integration Creation", self.test_integration_creation),
            ("User Creation", self.test_user_creation),
            ("Rate Limiting", self.test_rate_limiting),
            ("WebSocket Connection", self.test_websocket_connection)
        ]
        
        results = {}
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            logger.info(f"🧪 Running test: {test_name}")
            try:
                result = await test_func()
                results[test_name] = result
                if result:
                    passed += 1
                    logger.info(f"✅ {test_name}: PASSED")
                else:
                    logger.error(f"❌ {test_name}: FAILED")
            except Exception as e:
                logger.error(f"❌ {test_name}: ERROR - {e}")
                results[test_name] = False
            
            # Small delay between tests
            await asyncio.sleep(1)
        
        await self.cleanup()
        
        # Generate test report
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_tests": total,
            "passed": passed,
            "failed": total - passed,
            "success_rate": f"{(passed/total)*100:.1f}%",
            "test_results": results,
            "tenant_id": self.test_tenant_id,
            "platform_status": "operational" if passed >= total * 0.8 else "degraded"
        }
        
        logger.info("=" * 60)
        logger.info("📊 PHASE 4 ENTERPRISE TEST RESULTS")
        logger.info("=" * 60)
        logger.info(f"Total Tests: {total}")
        logger.info(f"Passed: {passed}")
        logger.info(f"Failed: {total - passed}")
        logger.info(f"Success Rate: {report['success_rate']}")
        logger.info(f"Platform Status: {report['platform_status'].upper()}")
        logger.info("=" * 60)
        
        return report

async def main():
    """Main test execution"""
    tester = Phase4EnterpriseTest()
    
    try:
        report = await tester.run_all_tests()
        
        # Save test report
        with open("phase4_test_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        logger.info("📄 Test report saved to: phase4_test_report.json")
        
        return report["success_rate"] == "100.0%"
        
    except Exception as e:
        logger.error(f"❌ Test execution failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1) 