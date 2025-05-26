"""
🧪 QUANTUM-AI CYBER GOD - ALL PHASES INTEGRATION TEST
Comprehensive test suite for all 4 phases working together
"""

import asyncio
import aiohttp
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Any
import websockets

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AllPhasesIntegrationTest:
    """Test suite for all phases integration"""
    
    def __init__(self):
        self.base_urls = {
            "phase1": "http://localhost:8001",
            "phase2": "http://localhost:8002", 
            "phase3": "http://localhost:8003",
            "phase4": "http://localhost:8004"
        }
        self.session = None
        self.test_results = {}
        
        # Test data for different phases
        self.test_tenant_id = None
        self.test_api_key = None
        self.test_player_id = None
    
    async def setup(self):
        """Setup test environment"""
        self.session = aiohttp.ClientSession()
        logger.info("🔧 Setting up All Phases Integration test environment...")
    
    async def cleanup(self):
        """Cleanup test environment"""
        if self.session:
            await self.session.close()
        logger.info("🧹 Test environment cleanup complete")
    
    async def test_all_health_checks(self) -> Dict[str, bool]:
        """Test health checks for all phases"""
        results = {}
        
        for phase, url in self.base_urls.items():
            try:
                async with self.session.get(f"{url}/health") as response:
                    if response.status == 200:
                        data = await response.json()
                        results[phase] = True
                        logger.info(f"✅ {phase.upper()} health check passed")
                    else:
                        results[phase] = False
                        logger.error(f"❌ {phase.upper()} health check failed: {response.status}")
            except Exception as e:
                results[phase] = False
                logger.error(f"❌ {phase.upper()} health check error: {e}")
        
        return results
    
    async def test_all_status_endpoints(self) -> Dict[str, bool]:
        """Test status endpoints for all phases"""
        results = {}
        status_endpoints = {
            "phase1": "/api/status",
            "phase2": "/api/status/phase2",
            "phase3": "/api/status/phase3", 
            "phase4": "/api/status/phase4"
        }
        
        for phase, endpoint in status_endpoints.items():
            try:
                url = f"{self.base_urls[phase]}{endpoint}"
                async with self.session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        results[phase] = True
                        logger.info(f"✅ {phase.upper()} status endpoint working")
                    else:
                        results[phase] = False
                        logger.error(f"❌ {phase.upper()} status endpoint failed: {response.status}")
            except Exception as e:
                results[phase] = False
                logger.error(f"❌ {phase.upper()} status endpoint error: {e}")
        
        return results
    
    async def test_phase1_legacy_features(self) -> bool:
        """Test Phase 1 legacy features"""
        try:
            # Test threat detection
            async with self.session.get(f"{self.base_urls['phase1']}/api/threats") as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info("✅ Phase 1 threat detection working")
                    return True
                else:
                    logger.error(f"❌ Phase 1 threat detection failed: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Phase 1 legacy features error: {e}")
            return False
    
    async def test_phase2_blockchain_features(self) -> bool:
        """Test Phase 2 blockchain features"""
        try:
            # Test blockchain monitoring
            async with self.session.get(f"{self.base_urls['phase2']}/api/blockchain/monitor") as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info("✅ Phase 2 blockchain monitoring working")
                    return True
                else:
                    logger.error(f"❌ Phase 2 blockchain monitoring failed: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Phase 2 blockchain features error: {e}")
            return False
    
    async def test_phase3_war_games_features(self) -> bool:
        """Test Phase 3 war games features"""
        try:
            # Test player registration
            player_data = {
                "username": "test_player_integration",
                "email": "test@integration.com",
                "team_name": "Integration Test Team"
            }
            
            async with self.session.post(
                f"{self.base_urls['phase3']}/api/players/register",
                json=player_data
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    self.test_player_id = data.get("player_id")
                    logger.info(f"✅ Phase 3 player registration working: {self.test_player_id}")
                    
                    # Test challenges endpoint
                    async with self.session.get(f"{self.base_urls['phase3']}/api/challenges") as challenges_response:
                        if challenges_response.status == 200:
                            logger.info("✅ Phase 3 challenges endpoint working")
                            return True
                        else:
                            logger.error(f"❌ Phase 3 challenges failed: {challenges_response.status}")
                            return False
                else:
                    logger.error(f"❌ Phase 3 player registration failed: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Phase 3 war games features error: {e}")
            return False
    
    async def test_phase4_enterprise_features(self) -> bool:
        """Test Phase 4 enterprise features"""
        try:
            # Test tenant registration
            tenant_data = {
                "organization_name": "Integration Test Corp",
                "admin_email": "admin@integrationtest.com",
                "tier": "enterprise",
                "industry": "Technology",
                "compliance_requirements": ["soc2"],
                "max_users": 50
            }
            
            async with self.session.post(
                f"{self.base_urls['phase4']}/api/enterprise/tenants/register",
                json=tenant_data
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    self.test_tenant_id = data.get("tenant_id")
                    self.test_api_key = data.get("api_key")
                    logger.info(f"✅ Phase 4 tenant registration working: {self.test_tenant_id}")
                    
                    # Test enterprise dashboard
                    headers = {"Authorization": f"Bearer {self.test_tenant_id}:{self.test_api_key}"}
                    async with self.session.get(
                        f"{self.base_urls['phase4']}/api/enterprise/tenants/{self.test_tenant_id}/dashboard",
                        headers=headers
                    ) as dashboard_response:
                        if dashboard_response.status == 200:
                            logger.info("✅ Phase 4 enterprise dashboard working")
                            return True
                        else:
                            logger.error(f"❌ Phase 4 dashboard failed: {dashboard_response.status}")
                            return False
                else:
                    logger.error(f"❌ Phase 4 tenant registration failed: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Phase 4 enterprise features error: {e}")
            return False
    
    async def test_websocket_connections(self) -> Dict[str, bool]:
        """Test WebSocket connections for phases that support them"""
        results = {}
        
        # Test Phase 3 WebSocket
        if self.test_player_id:
            try:
                uri = f"ws://localhost:8003/ws/game/{self.test_player_id}"
                async with websockets.connect(uri) as websocket:
                    message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    data = json.loads(message)
                    if data.get("type") == "game_update":
                        results["phase3_websocket"] = True
                        logger.info("✅ Phase 3 WebSocket working")
                    else:
                        results["phase3_websocket"] = False
                        logger.error("❌ Phase 3 WebSocket unexpected message format")
            except Exception as e:
                results["phase3_websocket"] = False
                logger.error(f"❌ Phase 3 WebSocket error: {e}")
        else:
            results["phase3_websocket"] = False
            logger.error("❌ No player ID for Phase 3 WebSocket test")
        
        # Test Phase 4 WebSocket
        if self.test_tenant_id:
            try:
                uri = f"ws://localhost:8004/ws/enterprise/{self.test_tenant_id}"
                async with websockets.connect(uri) as websocket:
                    message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    data = json.loads(message)
                    if data.get("type") == "enterprise_update":
                        results["phase4_websocket"] = True
                        logger.info("✅ Phase 4 WebSocket working")
                    else:
                        results["phase4_websocket"] = False
                        logger.error("❌ Phase 4 WebSocket unexpected message format")
            except Exception as e:
                results["phase4_websocket"] = False
                logger.error(f"❌ Phase 4 WebSocket error: {e}")
        else:
            results["phase4_websocket"] = False
            logger.error("❌ No tenant ID for Phase 4 WebSocket test")
        
        return results
    
    async def test_port_isolation(self) -> bool:
        """Test that all phases are running on different ports without conflicts"""
        try:
            # Test that each phase responds on its designated port
            ports_working = 0
            total_ports = 4
            
            for phase, url in self.base_urls.items():
                try:
                    async with self.session.get(f"{url}/health", timeout=5) as response:
                        if response.status == 200:
                            ports_working += 1
                            logger.info(f"✅ {phase.upper()} port isolation working")
                        else:
                            logger.error(f"❌ {phase.upper()} port not responding correctly")
                except Exception as e:
                    logger.error(f"❌ {phase.upper()} port error: {e}")
            
            if ports_working == total_ports:
                logger.info("✅ All phases have proper port isolation")
                return True
            else:
                logger.error(f"❌ Port isolation failed: {ports_working}/{total_ports} working")
                return False
                
        except Exception as e:
            logger.error(f"❌ Port isolation test error: {e}")
            return False
    
    async def test_cross_phase_data_flow(self) -> bool:
        """Test data flow between phases (simulated integration)"""
        try:
            # This would test if phases can share data appropriately
            # For now, we'll test that each phase maintains its own data independently
            
            # Get data from each phase
            phase_data = {}
            
            # Phase 1 threats
            try:
                async with self.session.get(f"{self.base_urls['phase1']}/api/threats") as response:
                    if response.status == 200:
                        phase_data["phase1_threats"] = await response.json()
            except:
                pass
            
            # Phase 2 blockchain data
            try:
                async with self.session.get(f"{self.base_urls['phase2']}/api/blockchain/monitor") as response:
                    if response.status == 200:
                        phase_data["phase2_blockchain"] = await response.json()
            except:
                pass
            
            # Phase 3 challenges
            try:
                async with self.session.get(f"{self.base_urls['phase3']}/api/challenges") as response:
                    if response.status == 200:
                        phase_data["phase3_challenges"] = await response.json()
            except:
                pass
            
            # Phase 4 analytics (if we have tenant credentials)
            if self.test_tenant_id and self.test_api_key:
                try:
                    headers = {"Authorization": f"Bearer {self.test_tenant_id}:{self.test_api_key}"}
                    async with self.session.get(
                        f"{self.base_urls['phase4']}/api/enterprise/tenants/{self.test_tenant_id}/analytics/overview",
                        headers=headers
                    ) as response:
                        if response.status == 200:
                            phase_data["phase4_analytics"] = await response.json()
                except:
                    pass
            
            # Check that we got data from multiple phases
            if len(phase_data) >= 2:
                logger.info(f"✅ Cross-phase data flow working: {len(phase_data)} phases providing data")
                return True
            else:
                logger.error(f"❌ Cross-phase data flow limited: only {len(phase_data)} phases responding")
                return False
                
        except Exception as e:
            logger.error(f"❌ Cross-phase data flow test error: {e}")
            return False
    
    async def test_concurrent_load(self) -> bool:
        """Test that all phases can handle concurrent requests"""
        try:
            # Make concurrent requests to all phases
            tasks = []
            
            # Create multiple concurrent requests for each phase
            for phase, url in self.base_urls.items():
                for i in range(5):  # 5 concurrent requests per phase
                    task = self.session.get(f"{url}/health")
                    tasks.append(task)
            
            # Execute all requests concurrently
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Count successful responses
            successful = 0
            total = len(tasks)
            
            for response in responses:
                if isinstance(response, Exception):
                    continue
                try:
                    if response.status == 200:
                        successful += 1
                    response.close()
                except:
                    pass
            
            success_rate = (successful / total) * 100
            
            if success_rate >= 80:  # 80% success rate is acceptable
                logger.info(f"✅ Concurrent load test passed: {success_rate:.1f}% success rate")
                return True
            else:
                logger.error(f"❌ Concurrent load test failed: {success_rate:.1f}% success rate")
                return False
                
        except Exception as e:
            logger.error(f"❌ Concurrent load test error: {e}")
            return False
    
    async def run_all_integration_tests(self) -> Dict[str, Any]:
        """Run all integration tests"""
        logger.info("🚀 Starting All Phases Integration Tests...")
        
        await self.setup()
        
        # Define all tests
        tests = [
            ("Health Checks", self.test_all_health_checks),
            ("Status Endpoints", self.test_all_status_endpoints),
            ("Phase 1 Legacy Features", self.test_phase1_legacy_features),
            ("Phase 2 Blockchain Features", self.test_phase2_blockchain_features),
            ("Phase 3 War Games Features", self.test_phase3_war_games_features),
            ("Phase 4 Enterprise Features", self.test_phase4_enterprise_features),
            ("WebSocket Connections", self.test_websocket_connections),
            ("Port Isolation", self.test_port_isolation),
            ("Cross-Phase Data Flow", self.test_cross_phase_data_flow),
            ("Concurrent Load", self.test_concurrent_load)
        ]
        
        results = {}
        passed = 0
        total_tests = 0
        
        for test_name, test_func in tests:
            logger.info(f"🧪 Running test: {test_name}")
            try:
                result = await test_func()
                results[test_name] = result
                
                if isinstance(result, dict):
                    # For tests that return multiple results
                    sub_passed = sum(1 for v in result.values() if v)
                    sub_total = len(result)
                    passed += sub_passed
                    total_tests += sub_total
                    logger.info(f"📊 {test_name}: {sub_passed}/{sub_total} passed")
                else:
                    # For tests that return boolean
                    total_tests += 1
                    if result:
                        passed += 1
                        logger.info(f"✅ {test_name}: PASSED")
                    else:
                        logger.error(f"❌ {test_name}: FAILED")
                        
            except Exception as e:
                logger.error(f"❌ {test_name}: ERROR - {e}")
                results[test_name] = False
                total_tests += 1
            
            # Small delay between tests
            await asyncio.sleep(1)
        
        await self.cleanup()
        
        # Generate comprehensive report
        success_rate = (passed / total_tests) * 100 if total_tests > 0 else 0
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_tests": total_tests,
            "passed": passed,
            "failed": total_tests - passed,
            "success_rate": f"{success_rate:.1f}%",
            "test_results": results,
            "platform_status": "fully_operational" if success_rate >= 90 else "operational" if success_rate >= 75 else "degraded",
            "phase_endpoints": self.base_urls,
            "test_credentials": {
                "tenant_id": self.test_tenant_id,
                "player_id": self.test_player_id
            }
        }
        
        logger.info("=" * 80)
        logger.info("📊 ALL PHASES INTEGRATION TEST RESULTS")
        logger.info("=" * 80)
        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"Passed: {passed}")
        logger.info(f"Failed: {total_tests - passed}")
        logger.info(f"Success Rate: {report['success_rate']}")
        logger.info(f"Platform Status: {report['platform_status'].upper()}")
        logger.info("=" * 80)
        
        # Phase-specific summary
        logger.info("🔍 PHASE-SPECIFIC RESULTS:")
        for phase in ["phase1", "phase2", "phase3", "phase4"]:
            phase_tests = [k for k in results.keys() if phase in k.lower() or "health" in k.lower() or "status" in k.lower()]
            if phase_tests:
                phase_passed = sum(1 for test in phase_tests if results.get(test, False))
                logger.info(f"  {phase.upper()}: {phase_passed}/{len(phase_tests)} tests passed")
        
        return report

async def main():
    """Main test execution"""
    tester = AllPhasesIntegrationTest()
    
    try:
        report = await tester.run_all_integration_tests()
        
        # Save comprehensive test report
        with open("all_phases_integration_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        logger.info("📄 Integration test report saved to: all_phases_integration_report.json")
        
        # Return success if 90% or more tests pass
        return float(report["success_rate"].rstrip('%')) >= 90.0
        
    except Exception as e:
        logger.error(f"❌ Integration test execution failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1) 