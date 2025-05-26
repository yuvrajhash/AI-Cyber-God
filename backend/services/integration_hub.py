"""
🔗 Integration Hub Service
Enterprise system integrations for SIEM, SOAR, ticketing, and communication platforms
"""

import asyncio
import json
import logging
import uuid
import random
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from enum import Enum
import aiohttp

logger = logging.getLogger(__name__)

class IntegrationType(str, Enum):
    SIEM = "siem"
    SOAR = "soar"
    TICKETING = "ticketing"
    SLACK = "slack"
    TEAMS = "teams"
    EMAIL = "email"
    WEBHOOK = "webhook"

class IntegrationStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    TESTING = "testing"

class IntegrationHub:
    def __init__(self):
        self.is_active = False
        self.tenant_integrations: Dict[str, List[Dict]] = {}
        self.integration_health: Dict[str, Dict] = {}
        self.integration_templates = {
            IntegrationType.SIEM: {
                "name": "SIEM Integration",
                "description": "Security Information and Event Management",
                "supported_platforms": ["Splunk", "QRadar", "ArcSight", "LogRhythm", "Sentinel"],
                "event_types": ["threat_detected", "incident_created", "alert_triggered"],
                "required_fields": ["endpoint_url", "api_key"],
                "optional_fields": ["custom_headers", "event_filters"],
                "test_endpoint": "/api/test/siem"
            },
            IntegrationType.SOAR: {
                "name": "SOAR Integration", 
                "description": "Security Orchestration, Automation and Response",
                "supported_platforms": ["Phantom", "Demisto", "Swimlane", "Siemplify", "Resilient"],
                "event_types": ["incident_created", "playbook_triggered", "response_automated"],
                "required_fields": ["endpoint_url", "api_key"],
                "optional_fields": ["playbook_id", "custom_headers"],
                "test_endpoint": "/api/test/soar"
            },
            IntegrationType.TICKETING: {
                "name": "Ticketing System Integration",
                "description": "IT Service Management and Ticketing",
                "supported_platforms": ["ServiceNow", "Jira", "Remedy", "Zendesk", "Freshservice"],
                "event_types": ["ticket_created", "incident_escalated", "status_updated"],
                "required_fields": ["endpoint_url", "api_key"],
                "optional_fields": ["project_key", "priority_mapping"],
                "test_endpoint": "/api/test/ticketing"
            },
            IntegrationType.SLACK: {
                "name": "Slack Integration",
                "description": "Team communication and notifications",
                "supported_platforms": ["Slack"],
                "event_types": ["message_sent", "alert_posted", "channel_notification"],
                "required_fields": ["webhook_url"],
                "optional_fields": ["channel", "username", "icon_emoji"],
                "test_endpoint": "/api/test/slack"
            },
            IntegrationType.TEAMS: {
                "name": "Microsoft Teams Integration",
                "description": "Microsoft Teams notifications and collaboration",
                "supported_platforms": ["Microsoft Teams"],
                "event_types": ["message_sent", "card_posted", "adaptive_card"],
                "required_fields": ["webhook_url"],
                "optional_fields": ["theme_color", "card_template"],
                "test_endpoint": "/api/test/teams"
            },
            IntegrationType.EMAIL: {
                "name": "Email Integration",
                "description": "Email notifications and alerts",
                "supported_platforms": ["SMTP", "SendGrid", "Mailgun", "SES"],
                "event_types": ["email_sent", "alert_emailed", "report_delivered"],
                "required_fields": ["smtp_server", "smtp_port", "username", "password"],
                "optional_fields": ["from_address", "reply_to", "template_id"],
                "test_endpoint": "/api/test/email"
            },
            IntegrationType.WEBHOOK: {
                "name": "Generic Webhook Integration",
                "description": "Custom webhook endpoints for any system",
                "supported_platforms": ["Any HTTP endpoint"],
                "event_types": ["webhook_triggered", "data_posted", "event_forwarded"],
                "required_fields": ["endpoint_url"],
                "optional_fields": ["webhook_secret", "custom_headers", "payload_template"],
                "test_endpoint": "/api/test/webhook"
            }
        }

    async def initialize(self):
        """Initialize the integration hub"""
        try:
            logger.info("🔗 Initializing Integration Hub...")
            
            # Initialize demo integrations
            await self._initialize_demo_integrations()
            
            self.is_active = True
            logger.info("✅ Integration Hub initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Error initializing Integration Hub: {e}")
            raise

    async def _initialize_demo_integrations(self):
        """Initialize demo integrations for testing"""
        demo_integrations = [
            {
                "tenant_id": "demo-tenant-1",
                "integration_name": "Splunk SIEM",
                "integration_type": IntegrationType.SIEM,
                "endpoint_url": "https://splunk.company.com/api/events",
                "api_key": "demo-splunk-key-123",
                "event_filters": ["threat_detected", "incident_created"]
            },
            {
                "tenant_id": "demo-tenant-1",
                "integration_name": "Security Team Slack",
                "integration_type": IntegrationType.SLACK,
                "endpoint_url": "https://hooks.slack.com/services/demo/webhook",
                "custom_headers": {"Content-Type": "application/json"},
                "event_filters": ["alert_triggered"]
            },
            {
                "tenant_id": "demo-tenant-2",
                "integration_name": "ServiceNow ITSM",
                "integration_type": IntegrationType.TICKETING,
                "endpoint_url": "https://company.service-now.com/api/incidents",
                "api_key": "demo-servicenow-key-456",
                "event_filters": ["incident_created", "incident_escalated"]
            }
        ]
        
        for integration_data in demo_integrations:
            await self.create_integration(**integration_data)

    async def create_integration(
        self,
        tenant_id: str,
        integration_name: str,
        integration_type: IntegrationType,
        endpoint_url: str,
        api_key: Optional[str] = None,
        webhook_secret: Optional[str] = None,
        custom_headers: Dict[str, str] = None,
        event_filters: List[str] = None
    ) -> Dict:
        """Create a new integration for a tenant"""
        try:
            integration_id = str(uuid.uuid4())
            
            if custom_headers is None:
                custom_headers = {}
            if event_filters is None:
                event_filters = []
            
            # Get integration template
            template = self.integration_templates.get(integration_type, {})
            
            integration = {
                "integration_id": integration_id,
                "tenant_id": tenant_id,
                "integration_name": integration_name,
                "integration_type": integration_type,
                "template_info": template,
                "configuration": {
                    "endpoint_url": endpoint_url,
                    "api_key": api_key,
                    "webhook_secret": webhook_secret,
                    "custom_headers": custom_headers,
                    "event_filters": event_filters
                },
                "status": IntegrationStatus.TESTING,
                "created_at": datetime.now().isoformat(),
                "last_tested": None,
                "last_used": None,
                "success_count": 0,
                "error_count": 0,
                "last_error": None,
                "health_score": 100.0
            }
            
            # Initialize tenant integrations list if needed
            if tenant_id not in self.tenant_integrations:
                self.tenant_integrations[tenant_id] = []
            
            self.tenant_integrations[tenant_id].append(integration)
            
            # Initialize health tracking
            self.integration_health[integration_id] = {
                "status": IntegrationStatus.TESTING,
                "last_check": datetime.now().isoformat(),
                "response_time": 0.0,
                "uptime_percentage": 100.0,
                "error_rate": 0.0
            }
            
            # Test the integration
            await self._test_integration(integration_id)
            
            logger.info(f"✅ Created integration: {integration_name} ({integration_id})")
            return integration
            
        except Exception as e:
            logger.error(f"❌ Error creating integration: {e}")
            raise

    async def _test_integration(self, integration_id: str):
        """Test an integration to verify connectivity"""
        try:
            # Find the integration
            integration = None
            for tenant_integrations in self.tenant_integrations.values():
                for integ in tenant_integrations:
                    if integ["integration_id"] == integration_id:
                        integration = integ
                        break
                if integration:
                    break
            
            if not integration:
                return False
            
            # Simulate integration test
            test_success = random.choice([True, True, True, False])  # 75% success rate
            response_time = random.uniform(0.1, 2.0)
            
            integration["last_tested"] = datetime.now().isoformat()
            
            if test_success:
                integration["status"] = IntegrationStatus.ACTIVE
                integration["health_score"] = random.uniform(85, 100)
                self.integration_health[integration_id]["status"] = IntegrationStatus.ACTIVE
                self.integration_health[integration_id]["response_time"] = response_time
                logger.info(f"✅ Integration test passed: {integration['integration_name']}")
            else:
                integration["status"] = IntegrationStatus.ERROR
                integration["last_error"] = "Connection timeout during test"
                integration["error_count"] += 1
                integration["health_score"] = random.uniform(20, 60)
                self.integration_health[integration_id]["status"] = IntegrationStatus.ERROR
                logger.warning(f"❌ Integration test failed: {integration['integration_name']}")
            
            self.integration_health[integration_id]["last_check"] = datetime.now().isoformat()
            
            return test_success
            
        except Exception as e:
            logger.error(f"❌ Error testing integration: {e}")
            return False

    async def get_tenant_integrations(self, tenant_id: str) -> List[Dict]:
        """Get all integrations for a tenant"""
        try:
            integrations = self.tenant_integrations.get(tenant_id, [])
            
            # Return sanitized integration data (without sensitive info)
            sanitized_integrations = []
            for integration in integrations:
                sanitized = integration.copy()
                # Remove sensitive configuration data
                if "api_key" in sanitized["configuration"]:
                    sanitized["configuration"]["api_key"] = "***REDACTED***"
                if "webhook_secret" in sanitized["configuration"]:
                    sanitized["configuration"]["webhook_secret"] = "***REDACTED***"
                
                sanitized_integrations.append(sanitized)
            
            return sanitized_integrations
            
        except Exception as e:
            logger.error(f"❌ Error getting tenant integrations: {e}")
            return []

    async def get_integration_health(self, tenant_id: str) -> Dict:
        """Get health status for all tenant integrations"""
        try:
            tenant_integrations = self.tenant_integrations.get(tenant_id, [])
            
            health_summary = {
                "total_integrations": len(tenant_integrations),
                "active_integrations": 0,
                "error_integrations": 0,
                "average_health_score": 0.0,
                "average_response_time": 0.0,
                "integration_details": {}
            }
            
            if not tenant_integrations:
                return health_summary
            
            total_health = 0
            total_response_time = 0
            
            for integration in tenant_integrations:
                integration_id = integration["integration_id"]
                health_data = self.integration_health.get(integration_id, {})
                
                if integration["status"] == IntegrationStatus.ACTIVE:
                    health_summary["active_integrations"] += 1
                elif integration["status"] == IntegrationStatus.ERROR:
                    health_summary["error_integrations"] += 1
                
                total_health += integration["health_score"]
                total_response_time += health_data.get("response_time", 0)
                
                health_summary["integration_details"][integration_id] = {
                    "name": integration["integration_name"],
                    "type": integration["integration_type"],
                    "status": integration["status"],
                    "health_score": integration["health_score"],
                    "response_time": health_data.get("response_time", 0),
                    "last_check": health_data.get("last_check"),
                    "success_count": integration["success_count"],
                    "error_count": integration["error_count"]
                }
            
            health_summary["average_health_score"] = round(total_health / len(tenant_integrations), 1)
            health_summary["average_response_time"] = round(total_response_time / len(tenant_integrations), 2)
            
            return health_summary
            
        except Exception as e:
            logger.error(f"❌ Error getting integration health: {e}")
            return {}

    async def send_event(self, tenant_id: str, event_type: str, event_data: Dict) -> Dict:
        """Send an event to all relevant integrations for a tenant"""
        try:
            tenant_integrations = self.tenant_integrations.get(tenant_id, [])
            results = []
            
            for integration in tenant_integrations:
                if integration["status"] != IntegrationStatus.ACTIVE:
                    continue
                
                # Check if integration should receive this event type
                event_filters = integration["configuration"].get("event_filters", [])
                if event_filters and event_type not in event_filters:
                    continue
                
                # Send event to integration
                result = await self._send_to_integration(integration, event_type, event_data)
                results.append({
                    "integration_id": integration["integration_id"],
                    "integration_name": integration["integration_name"],
                    "success": result["success"],
                    "response_time": result["response_time"],
                    "error": result.get("error")
                })
                
                # Update integration statistics
                if result["success"]:
                    integration["success_count"] += 1
                    integration["last_used"] = datetime.now().isoformat()
                else:
                    integration["error_count"] += 1
                    integration["last_error"] = result.get("error", "Unknown error")
                
                # Update health score
                await self._update_integration_health(integration["integration_id"], result)
            
            return {
                "event_type": event_type,
                "tenant_id": tenant_id,
                "integrations_notified": len(results),
                "successful_deliveries": sum(1 for r in results if r["success"]),
                "failed_deliveries": sum(1 for r in results if not r["success"]),
                "results": results
            }
            
        except Exception as e:
            logger.error(f"❌ Error sending event: {e}")
            return {"error": str(e)}

    async def _send_to_integration(self, integration: Dict, event_type: str, event_data: Dict) -> Dict:
        """Send data to a specific integration"""
        try:
            integration_type = integration["integration_type"]
            config = integration["configuration"]
            
            # Simulate sending to different integration types
            start_time = datetime.now()
            
            if integration_type == IntegrationType.SIEM:
                success = await self._send_to_siem(config, event_type, event_data)
            elif integration_type == IntegrationType.SOAR:
                success = await self._send_to_soar(config, event_type, event_data)
            elif integration_type == IntegrationType.TICKETING:
                success = await self._send_to_ticketing(config, event_type, event_data)
            elif integration_type == IntegrationType.SLACK:
                success = await self._send_to_slack(config, event_type, event_data)
            elif integration_type == IntegrationType.TEAMS:
                success = await self._send_to_teams(config, event_type, event_data)
            elif integration_type == IntegrationType.EMAIL:
                success = await self._send_to_email(config, event_type, event_data)
            elif integration_type == IntegrationType.WEBHOOK:
                success = await self._send_to_webhook(config, event_type, event_data)
            else:
                success = False
            
            response_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "success": success,
                "response_time": response_time,
                "error": None if success else f"Failed to send to {integration_type}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "response_time": 0.0,
                "error": str(e)
            }

    async def _send_to_siem(self, config: Dict, event_type: str, event_data: Dict) -> bool:
        """Send event to SIEM system"""
        # Simulate SIEM API call
        await asyncio.sleep(random.uniform(0.1, 0.5))
        return random.choice([True, True, True, False])  # 75% success rate

    async def _send_to_soar(self, config: Dict, event_type: str, event_data: Dict) -> bool:
        """Send event to SOAR platform"""
        # Simulate SOAR API call
        await asyncio.sleep(random.uniform(0.2, 0.8))
        return random.choice([True, True, True, False])  # 75% success rate

    async def _send_to_ticketing(self, config: Dict, event_type: str, event_data: Dict) -> bool:
        """Send event to ticketing system"""
        # Simulate ticketing API call
        await asyncio.sleep(random.uniform(0.3, 1.0))
        return random.choice([True, True, True, False])  # 75% success rate

    async def _send_to_slack(self, config: Dict, event_type: str, event_data: Dict) -> bool:
        """Send message to Slack"""
        # Simulate Slack webhook call
        await asyncio.sleep(random.uniform(0.1, 0.3))
        return random.choice([True, True, True, True, False])  # 80% success rate

    async def _send_to_teams(self, config: Dict, event_type: str, event_data: Dict) -> bool:
        """Send message to Microsoft Teams"""
        # Simulate Teams webhook call
        await asyncio.sleep(random.uniform(0.1, 0.4))
        return random.choice([True, True, True, True, False])  # 80% success rate

    async def _send_to_email(self, config: Dict, event_type: str, event_data: Dict) -> bool:
        """Send email notification"""
        # Simulate email sending
        await asyncio.sleep(random.uniform(0.5, 2.0))
        return random.choice([True, True, True, False])  # 75% success rate

    async def _send_to_webhook(self, config: Dict, event_type: str, event_data: Dict) -> bool:
        """Send to generic webhook"""
        # Simulate webhook call
        await asyncio.sleep(random.uniform(0.1, 0.6))
        return random.choice([True, True, True, False])  # 75% success rate

    async def _update_integration_health(self, integration_id: str, result: Dict):
        """Update health metrics for an integration"""
        try:
            if integration_id not in self.integration_health:
                return
            
            health = self.integration_health[integration_id]
            
            # Update response time
            health["response_time"] = result["response_time"]
            health["last_check"] = datetime.now().isoformat()
            
            # Update status based on result
            if result["success"]:
                health["status"] = IntegrationStatus.ACTIVE
                # Improve health score slightly on success
                current_score = 100.0  # Default if not set
                for tenant_integrations in self.tenant_integrations.values():
                    for integration in tenant_integrations:
                        if integration["integration_id"] == integration_id:
                            current_score = integration["health_score"]
                            integration["health_score"] = min(100.0, current_score + 1.0)
                            break
            else:
                health["status"] = IntegrationStatus.ERROR
                # Decrease health score on failure
                for tenant_integrations in self.tenant_integrations.values():
                    for integration in tenant_integrations:
                        if integration["integration_id"] == integration_id:
                            current_score = integration["health_score"]
                            integration["health_score"] = max(0.0, current_score - 5.0)
                            break
            
        except Exception as e:
            logger.error(f"❌ Error updating integration health: {e}")

    async def get_integration_templates(self) -> Dict:
        """Get available integration templates"""
        try:
            return self.integration_templates
        except Exception as e:
            logger.error(f"❌ Error getting integration templates: {e}")
            return {}

    async def test_integration_endpoint(self, integration_id: str) -> Dict:
        """Test a specific integration endpoint"""
        try:
            result = await self._test_integration(integration_id)
            
            return {
                "integration_id": integration_id,
                "test_successful": result,
                "test_time": datetime.now().isoformat(),
                "message": "Integration test passed" if result else "Integration test failed"
            }
            
        except Exception as e:
            logger.error(f"❌ Error testing integration endpoint: {e}")
            return {
                "integration_id": integration_id,
                "test_successful": False,
                "error": str(e)
            }

    async def delete_integration(self, tenant_id: str, integration_id: str) -> bool:
        """Delete an integration"""
        try:
            if tenant_id not in self.tenant_integrations:
                return False
            
            # Find and remove the integration
            tenant_integrations = self.tenant_integrations[tenant_id]
            for i, integration in enumerate(tenant_integrations):
                if integration["integration_id"] == integration_id:
                    del tenant_integrations[i]
                    
                    # Remove health tracking
                    if integration_id in self.integration_health:
                        del self.integration_health[integration_id]
                    
                    logger.info(f"✅ Deleted integration: {integration_id}")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Error deleting integration: {e}")
            return False

    async def get_integration_statistics(self, tenant_id: str) -> Dict:
        """Get integration usage statistics for a tenant"""
        try:
            tenant_integrations = self.tenant_integrations.get(tenant_id, [])
            
            stats = {
                "total_integrations": len(tenant_integrations),
                "active_integrations": sum(1 for i in tenant_integrations if i["status"] == IntegrationStatus.ACTIVE),
                "total_events_sent": sum(i["success_count"] for i in tenant_integrations),
                "total_errors": sum(i["error_count"] for i in tenant_integrations),
                "success_rate": 0.0,
                "integration_breakdown": {}
            }
            
            total_attempts = stats["total_events_sent"] + stats["total_errors"]
            if total_attempts > 0:
                stats["success_rate"] = round((stats["total_events_sent"] / total_attempts) * 100, 2)
            
            # Breakdown by integration type
            for integration in tenant_integrations:
                int_type = integration["integration_type"]
                if int_type not in stats["integration_breakdown"]:
                    stats["integration_breakdown"][int_type] = {
                        "count": 0,
                        "active": 0,
                        "events_sent": 0,
                        "errors": 0
                    }
                
                breakdown = stats["integration_breakdown"][int_type]
                breakdown["count"] += 1
                if integration["status"] == IntegrationStatus.ACTIVE:
                    breakdown["active"] += 1
                breakdown["events_sent"] += integration["success_count"]
                breakdown["errors"] += integration["error_count"]
            
            return stats
            
        except Exception as e:
            logger.error(f"❌ Error getting integration statistics: {e}")
            return {}

    async def shutdown(self):
        """Shutdown the integration hub"""
        try:
            logger.info("🛑 Shutting down Integration Hub...")
            self.is_active = False
            
        except Exception as e:
            logger.error(f"❌ Error shutting down Integration Hub: {e}")

# Global integration hub instance
integration_hub = IntegrationHub() 