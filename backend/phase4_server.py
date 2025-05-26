"""
🏢 QUANTUM-AI CYBER GOD - PHASE 4 SERVER
Enterprise Features with Multi-tenant Architecture and Advanced Analytics
"""

import asyncio
import json
import logging
import uuid
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set
from contextlib import asynccontextmanager
from enum import Enum
import secrets
from collections import defaultdict, deque

from fastapi import FastAPI, HTTPException, BackgroundTasks, Query, WebSocket, WebSocketDisconnect, Depends, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
import uvicorn

# Import Phase 4 enterprise services
from services.enterprise_manager import enterprise_manager
from services.custom_threat_models import custom_threat_models
from services.api_rate_limiter import api_rate_limiter
from services.advanced_analytics import advanced_analytics
from services.compliance_auditor import compliance_auditor
from services.integration_hub import integration_hub

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Enterprise Enums
class TenantTier(str, Enum):
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    ENTERPRISE_PLUS = "enterprise_plus"

class ThreatModelType(str, Enum):
    FINANCIAL_SERVICES = "financial_services"
    HEALTHCARE = "healthcare"
    GOVERNMENT = "government"
    MANUFACTURING = "manufacturing"
    RETAIL = "retail"
    CUSTOM = "custom"

class ComplianceFramework(str, Enum):
    SOC2 = "soc2"
    ISO27001 = "iso27001"
    GDPR = "gdpr"
    HIPAA = "hipaa"
    PCI_DSS = "pci_dss"
    NIST = "nist"

class IntegrationType(str, Enum):
    SIEM = "siem"
    SOAR = "soar"
    TICKETING = "ticketing"
    SLACK = "slack"
    TEAMS = "teams"
    EMAIL = "email"
    WEBHOOK = "webhook"

# Enterprise Pydantic Models
class TenantRegistration(BaseModel):
    organization_name: str = Field(..., min_length=2, max_length=100)
    admin_email: str = Field(..., description="Primary admin email")
    tier: TenantTier = Field(default=TenantTier.STARTER)
    industry: str = Field(..., description="Industry sector")
    compliance_requirements: List[ComplianceFramework] = Field(default=[])
    max_users: int = Field(default=10, ge=1, le=10000)
    custom_domain: Optional[str] = Field(None, description="Custom domain for tenant")

class CustomThreatModel(BaseModel):
    model_name: str = Field(..., min_length=3, max_length=50)
    model_type: ThreatModelType = Field(..., description="Type of threat model")
    industry_focus: str = Field(..., description="Industry-specific focus")
    threat_vectors: List[str] = Field(..., description="Specific threat vectors to monitor")
    sensitivity_level: float = Field(default=0.7, ge=0.1, le=1.0)
    custom_rules: Dict[str, Any] = Field(default={}, description="Custom detection rules")
    compliance_mapping: List[ComplianceFramework] = Field(default=[])

class EnterpriseUser(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: str = Field(..., description="User email")
    role: str = Field(..., description="User role in organization")
    permissions: List[str] = Field(default=[], description="Specific permissions")
    department: str = Field(..., description="Department/team")
    access_level: int = Field(default=1, ge=1, le=5, description="Access level 1-5")

class IntegrationConfig(BaseModel):
    integration_name: str = Field(..., min_length=3, max_length=50)
    integration_type: IntegrationType = Field(..., description="Type of integration")
    endpoint_url: str = Field(..., description="Integration endpoint URL")
    api_key: Optional[str] = Field(None, description="API key for integration")
    webhook_secret: Optional[str] = Field(None, description="Webhook secret")
    custom_headers: Dict[str, str] = Field(default={}, description="Custom headers")
    event_filters: List[str] = Field(default=[], description="Event types to forward")

class ComplianceReport(BaseModel):
    framework: ComplianceFramework = Field(..., description="Compliance framework")
    report_period: str = Field(..., description="Reporting period")
    include_recommendations: bool = Field(default=True)
    detailed_findings: bool = Field(default=False)

# Global enterprise state
enterprise_tenants: Dict[str, Dict] = {}
active_enterprise_connections: Dict[str, WebSocket] = {}
tenant_rate_limits: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
security_bearer = HTTPBearer()

# Rate limiting decorator
def rate_limit_check(tenant_id: str, endpoint: str, tier: TenantTier) -> bool:
    """Check if request is within rate limits for tenant tier"""
    current_time = time.time()
    tenant_requests = tenant_rate_limits[f"{tenant_id}:{endpoint}"]
    
    # Define rate limits per tier (requests per minute)
    limits = {
        TenantTier.STARTER: 100,
        TenantTier.PROFESSIONAL: 500,
        TenantTier.ENTERPRISE: 2000,
        TenantTier.ENTERPRISE_PLUS: 10000
    }
    
    # Clean old requests (older than 1 minute)
    while tenant_requests and tenant_requests[0] < current_time - 60:
        tenant_requests.popleft()
    
    # Check if under limit
    if len(tenant_requests) < limits[tier]:
        tenant_requests.append(current_time)
        return True
    
    return False

async def get_tenant_from_token(credentials: HTTPAuthorizationCredentials = Depends(security_bearer)) -> Dict:
    """Extract tenant information from JWT token"""
    try:
        # In a real implementation, this would validate JWT and extract tenant info
        # For demo purposes, we'll use a simple token format: tenant_id:api_key
        token_parts = credentials.credentials.split(':')
        if len(token_parts) != 2:
            raise HTTPException(status_code=401, detail="Invalid token format")
        
        tenant_id, api_key = token_parts
        
        if tenant_id not in enterprise_tenants:
            raise HTTPException(status_code=401, detail="Invalid tenant")
        
        tenant = enterprise_tenants[tenant_id]
        if tenant.get('api_key') != api_key:
            raise HTTPException(status_code=401, detail="Invalid API key")
        
        return tenant
    
    except Exception as e:
        raise HTTPException(status_code=401, detail="Authentication failed")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan"""
    logger.info("🏢 Starting Quantum-AI Cyber God Phase 4 - Enterprise Platform...")
    
    try:
        # Initialize Enterprise services
        await enterprise_manager.initialize()
        await custom_threat_models.initialize()
        await api_rate_limiter.initialize()
        await advanced_analytics.initialize()
        await compliance_auditor.initialize()
        await integration_hub.initialize()
        
        # Start background enterprise processes
        asyncio.create_task(enterprise_manager.start_tenant_monitoring())
        asyncio.create_task(advanced_analytics.start_analytics_engine())
        asyncio.create_task(compliance_auditor.start_compliance_monitoring())
        
        logger.info("✅ Phase 4 Enterprise Platform initialized successfully")
        
    except Exception as e:
        logger.error(f"❌ Error initializing Enterprise Platform: {e}")
    
    yield
    
    # Cleanup
    logger.info("🛑 Shutting down Enterprise Platform...")
    await enterprise_manager.shutdown()

# Create FastAPI app with lifespan
app = FastAPI(
    title="Quantum-AI Cyber God - Phase 4 Enterprise",
    description="Enterprise cybersecurity platform with multi-tenant architecture",
    version="4.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# HEALTH & STATUS ENDPOINTS
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "phase": "4",
        "platform": "enterprise",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "enterprise_manager": enterprise_manager.is_active,
            "custom_threat_models": custom_threat_models.is_active,
            "api_rate_limiter": api_rate_limiter.is_active,
            "advanced_analytics": advanced_analytics.is_active,
            "compliance_auditor": compliance_auditor.is_active,
            "integration_hub": integration_hub.is_active
        },
        "active_tenants": len(enterprise_tenants),
        "active_connections": len(active_enterprise_connections)
    }

@app.get("/api/status/phase4")
async def phase4_status():
    """Get Phase 4 Enterprise Platform status"""
    try:
        stats = await enterprise_manager.get_platform_stats()
        return {
            "phase": "4",
            "status": "operational",
            "platform": "enterprise",
            "timestamp": datetime.now().isoformat(),
            "statistics": stats,
            "total_tenants": len(enterprise_tenants),
            "active_threat_models": await custom_threat_models.get_active_models_count(),
            "compliance_frameworks": await compliance_auditor.get_supported_frameworks()
        }
    except Exception as e:
        logger.error(f"Error getting Phase 4 status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# TENANT MANAGEMENT ENDPOINTS
# ============================================================================

@app.post("/api/enterprise/tenants/register")
async def register_tenant(registration: TenantRegistration):
    """Register a new enterprise tenant"""
    try:
        tenant = await enterprise_manager.register_tenant(
            organization_name=registration.organization_name,
            admin_email=registration.admin_email,
            tier=registration.tier,
            industry=registration.industry,
            compliance_requirements=registration.compliance_requirements,
            max_users=registration.max_users,
            custom_domain=registration.custom_domain
        )
        
        # Store tenant in global state
        enterprise_tenants[tenant["tenant_id"]] = tenant
        
        return {
            "success": True,
            "tenant_id": tenant["tenant_id"],
            "api_key": tenant["api_key"],
            "message": f"Enterprise tenant '{registration.organization_name}' registered successfully",
            "dashboard_url": f"/enterprise/dashboard/{tenant['tenant_id']}",
            "api_endpoints": {
                "base_url": f"/api/enterprise/tenants/{tenant['tenant_id']}",
                "threat_models": f"/api/enterprise/tenants/{tenant['tenant_id']}/threat-models",
                "analytics": f"/api/enterprise/tenants/{tenant['tenant_id']}/analytics",
                "compliance": f"/api/enterprise/tenants/{tenant['tenant_id']}/compliance"
            }
        }
    except Exception as e:
        logger.error(f"Error registering tenant: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/enterprise/tenants/{tenant_id}/dashboard")
async def get_enterprise_dashboard(tenant_id: str, tenant: Dict = Depends(get_tenant_from_token)):
    """Get enterprise dashboard data"""
    try:
        if not rate_limit_check(tenant_id, "dashboard", tenant["tier"]):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        dashboard_data = await enterprise_manager.get_dashboard_data(tenant_id)
        return {
            "tenant_info": tenant,
            "dashboard": dashboard_data,
            "real_time_metrics": await advanced_analytics.get_real_time_metrics(tenant_id),
            "threat_summary": await custom_threat_models.get_threat_summary(tenant_id),
            "compliance_status": await compliance_auditor.get_compliance_status(tenant_id)
        }
    except Exception as e:
        logger.error(f"Error getting enterprise dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# CUSTOM THREAT MODELS ENDPOINTS
# ============================================================================

@app.post("/api/enterprise/tenants/{tenant_id}/threat-models")
async def create_custom_threat_model(
    tenant_id: str, 
    model: CustomThreatModel, 
    tenant: Dict = Depends(get_tenant_from_token)
):
    """Create a custom threat model for the tenant"""
    try:
        if not rate_limit_check(tenant_id, "threat_models", tenant["tier"]):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        threat_model = await custom_threat_models.create_model(
            tenant_id=tenant_id,
            model_name=model.model_name,
            model_type=model.model_type,
            industry_focus=model.industry_focus,
            threat_vectors=model.threat_vectors,
            sensitivity_level=model.sensitivity_level,
            custom_rules=model.custom_rules,
            compliance_mapping=model.compliance_mapping
        )
        
        return {
            "success": True,
            "model_id": threat_model["model_id"],
            "message": f"Custom threat model '{model.model_name}' created successfully",
            "model_details": threat_model,
            "training_status": "initializing",
            "estimated_training_time": "15-30 minutes"
        }
    except Exception as e:
        logger.error(f"Error creating custom threat model: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/enterprise/tenants/{tenant_id}/threat-models")
async def get_tenant_threat_models(tenant_id: str, tenant: Dict = Depends(get_tenant_from_token)):
    """Get all threat models for a tenant"""
    try:
        if not rate_limit_check(tenant_id, "threat_models", tenant["tier"]):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        models = await custom_threat_models.get_tenant_models(tenant_id)
        return {
            "tenant_id": tenant_id,
            "total_models": len(models),
            "models": models,
            "model_performance": await custom_threat_models.get_models_performance(tenant_id)
        }
    except Exception as e:
        logger.error(f"Error getting tenant threat models: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# ADVANCED ANALYTICS ENDPOINTS
# ============================================================================

@app.get("/api/enterprise/tenants/{tenant_id}/analytics/overview")
async def get_analytics_overview(tenant_id: str, tenant: Dict = Depends(get_tenant_from_token)):
    """Get comprehensive analytics overview"""
    try:
        if not rate_limit_check(tenant_id, "analytics", tenant["tier"]):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        analytics = await advanced_analytics.get_comprehensive_overview(tenant_id)
        return {
            "tenant_id": tenant_id,
            "analytics_period": "last_30_days",
            "overview": analytics,
            "key_insights": await advanced_analytics.get_key_insights(tenant_id),
            "recommendations": await advanced_analytics.get_recommendations(tenant_id)
        }
    except Exception as e:
        logger.error(f"Error getting analytics overview: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/enterprise/tenants/{tenant_id}/analytics/threats")
async def get_threat_analytics(
    tenant_id: str, 
    time_range: str = Query("7d", description="Time range: 1h, 24h, 7d, 30d"),
    tenant: Dict = Depends(get_tenant_from_token)
):
    """Get detailed threat analytics"""
    try:
        if not rate_limit_check(tenant_id, "analytics", tenant["tier"]):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        threat_analytics = await advanced_analytics.get_threat_analytics(tenant_id, time_range)
        return {
            "tenant_id": tenant_id,
            "time_range": time_range,
            "threat_analytics": threat_analytics,
            "trend_analysis": await advanced_analytics.get_threat_trends(tenant_id, time_range),
            "geographic_distribution": await advanced_analytics.get_geographic_threats(tenant_id)
        }
    except Exception as e:
        logger.error(f"Error getting threat analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# COMPLIANCE & AUDITING ENDPOINTS
# ============================================================================

@app.get("/api/enterprise/tenants/{tenant_id}/compliance/status")
async def get_compliance_status(tenant_id: str, tenant: Dict = Depends(get_tenant_from_token)):
    """Get current compliance status"""
    try:
        if not rate_limit_check(tenant_id, "compliance", tenant["tier"]):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        compliance_status = await compliance_auditor.get_detailed_status(tenant_id)
        return {
            "tenant_id": tenant_id,
            "compliance_status": compliance_status,
            "frameworks": await compliance_auditor.get_framework_status(tenant_id),
            "recent_audits": await compliance_auditor.get_recent_audits(tenant_id),
            "upcoming_requirements": await compliance_auditor.get_upcoming_requirements(tenant_id)
        }
    except Exception as e:
        logger.error(f"Error getting compliance status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/enterprise/tenants/{tenant_id}/compliance/reports")
async def generate_compliance_report(
    tenant_id: str, 
    report_config: ComplianceReport, 
    tenant: Dict = Depends(get_tenant_from_token)
):
    """Generate a compliance report"""
    try:
        if not rate_limit_check(tenant_id, "compliance", tenant["tier"]):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        report = await compliance_auditor.generate_report(
            tenant_id=tenant_id,
            framework=report_config.framework,
            report_period=report_config.report_period,
            include_recommendations=report_config.include_recommendations,
            detailed_findings=report_config.detailed_findings
        )
        
        return {
            "success": True,
            "report_id": report["report_id"],
            "framework": report_config.framework,
            "report_url": f"/api/enterprise/tenants/{tenant_id}/compliance/reports/{report['report_id']}",
            "generated_at": datetime.now().isoformat(),
            "report_summary": report["summary"]
        }
    except Exception as e:
        logger.error(f"Error generating compliance report: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# ============================================================================
# INTEGRATION HUB ENDPOINTS
# ============================================================================

@app.post("/api/enterprise/tenants/{tenant_id}/integrations")
async def create_integration(
    tenant_id: str, 
    integration: IntegrationConfig, 
    tenant: Dict = Depends(get_tenant_from_token)
):
    """Create a new enterprise integration"""
    try:
        if not rate_limit_check(tenant_id, "integrations", tenant["tier"]):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        integration_result = await integration_hub.create_integration(
            tenant_id=tenant_id,
            integration_name=integration.integration_name,
            integration_type=integration.integration_type,
            endpoint_url=integration.endpoint_url,
            api_key=integration.api_key,
            webhook_secret=integration.webhook_secret,
            custom_headers=integration.custom_headers,
            event_filters=integration.event_filters
        )
        
        return {
            "success": True,
            "integration_id": integration_result["integration_id"],
            "message": f"Integration '{integration.integration_name}' created successfully",
            "status": "active",
            "test_endpoint": f"/api/enterprise/tenants/{tenant_id}/integrations/{integration_result['integration_id']}/test"
        }
    except Exception as e:
        logger.error(f"Error creating integration: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/enterprise/tenants/{tenant_id}/integrations")
async def get_tenant_integrations(tenant_id: str, tenant: Dict = Depends(get_tenant_from_token)):
    """Get all integrations for a tenant"""
    try:
        if not rate_limit_check(tenant_id, "integrations", tenant["tier"]):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        integrations = await integration_hub.get_tenant_integrations(tenant_id)
        return {
            "tenant_id": tenant_id,
            "total_integrations": len(integrations),
            "integrations": integrations,
            "integration_health": await integration_hub.get_integration_health(tenant_id)
        }
    except Exception as e:
        logger.error(f"Error getting tenant integrations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# USER MANAGEMENT ENDPOINTS
# ============================================================================

@app.post("/api/enterprise/tenants/{tenant_id}/users")
async def create_enterprise_user(
    tenant_id: str, 
    user: EnterpriseUser, 
    tenant: Dict = Depends(get_tenant_from_token)
):
    """Create a new enterprise user"""
    try:
        if not rate_limit_check(tenant_id, "users", tenant["tier"]):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        enterprise_user = await enterprise_manager.create_user(
            tenant_id=tenant_id,
            username=user.username,
            email=user.email,
            role=user.role,
            permissions=user.permissions,
            department=user.department,
            access_level=user.access_level
        )
        
        return {
            "success": True,
            "user_id": enterprise_user["user_id"],
            "message": f"Enterprise user '{user.username}' created successfully",
            "login_url": f"/enterprise/login/{tenant_id}",
            "initial_password": enterprise_user["initial_password"]
        }
    except Exception as e:
        logger.error(f"Error creating enterprise user: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# ============================================================================
# WEBSOCKET ENDPOINTS
# ============================================================================

@app.websocket("/ws/enterprise/{tenant_id}")
async def websocket_enterprise_endpoint(websocket: WebSocket, tenant_id: str):
    """WebSocket endpoint for real-time enterprise updates"""
    await websocket.accept()
    active_enterprise_connections[tenant_id] = websocket
    
    try:
        while True:
            # Send real-time enterprise updates
            updates = await enterprise_manager.get_real_time_updates(tenant_id)
            await websocket.send_json({
                "type": "enterprise_update",
                "tenant_id": tenant_id,
                "timestamp": datetime.now().isoformat(),
                "updates": updates
            })
            
            await asyncio.sleep(5)  # Update every 5 seconds
            
    except WebSocketDisconnect:
        logger.info(f"Enterprise WebSocket disconnected for tenant: {tenant_id}")
    except Exception as e:
        logger.error(f"Enterprise WebSocket error: {e}")
    finally:
        if tenant_id in active_enterprise_connections:
            del active_enterprise_connections[tenant_id]

# ============================================================================
# MAIN SERVER STARTUP
# ============================================================================

if __name__ == "__main__":
    logger.info("🏢 Starting Quantum-AI Cyber God Phase 4 - Enterprise Platform")
    uvicorn.run(
        "phase4_server:app",
        host="0.0.0.0",
        port=8004,
        reload=True,
        log_level="info"
    ) 