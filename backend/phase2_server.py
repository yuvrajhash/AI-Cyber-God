"""
🚀 QUANTUM-AI CYBER GOD - PHASE 2 SERVER
Enhanced blockchain integration with real-time monitoring and analytics
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn

# Import Phase 2 services
from services.blockchain_monitor import blockchain_monitor
from services.realtime_analytics import realtime_analytics
from services.web3_integration import web3_integration

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models for API requests
class SmartContractAnalysisRequest(BaseModel):
    chain_id: int = Field(..., description="Blockchain chain ID")
    contract_address: str = Field(..., description="Smart contract address")

class TransactionSimulationRequest(BaseModel):
    chain_id: int = Field(..., description="Blockchain chain ID")
    to: Optional[str] = Field(None, description="Transaction recipient")
    value: Optional[int] = Field(0, description="Transaction value in wei")
    gas_limit: Optional[int] = Field(21000, description="Gas limit")
    data: Optional[str] = Field("", description="Transaction data")

class LiquidityPoolRequest(BaseModel):
    chain_id: int = Field(..., description="Blockchain chain ID")
    pool_address: str = Field(..., description="Liquidity pool address")

class DeFiRiskRequest(BaseModel):
    chain_id: int = Field(..., description="Blockchain chain ID")
    protocol_name: str = Field(..., description="DeFi protocol name")

# Background task management
background_tasks_active = False

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan"""
    global background_tasks_active
    
    logger.info("🚀 Starting Quantum-AI Cyber God Phase 2...")
    
    # Initialize services
    try:
        # Initialize Web3 connections
        await web3_integration.initialize_web3_connections([1, 137, 56])
        
        # Initialize blockchain monitoring
        await blockchain_monitor.initialize_connections([1, 137, 56])
        
        # Start background services
        background_tasks_active = True
        
        # Start analytics in background
        asyncio.create_task(realtime_analytics.start_analytics())
        
        # Start blockchain monitoring in background (limited for demo)
        # asyncio.create_task(blockchain_monitor.start_monitoring([11155111]))  # Only testnet for demo
        
        logger.info("✅ Phase 2 services initialized successfully")
        
    except Exception as e:
        logger.error(f"❌ Error initializing services: {e}")
    
    yield
    
    # Cleanup
    logger.info("🛑 Shutting down Phase 2 services...")
    background_tasks_active = False
    await realtime_analytics.stop_analytics()
    await blockchain_monitor.stop_monitoring()

# Create FastAPI app with lifespan
app = FastAPI(
    title="Quantum-AI Cyber God - Phase 2",
    description="Advanced blockchain security monitoring with real-time analytics",
    version="2.0.0",
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
        "phase": "2",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "blockchain_monitor": blockchain_monitor.monitoring_active,
            "realtime_analytics": realtime_analytics.analytics_active,
            "web3_integration": len(web3_integration.web3_connections) > 0
        }
    }

@app.get("/api/status/phase2")
async def phase2_status():
    """Get Phase 2 system status"""
    try:
        # Get blockchain monitoring stats
        blockchain_stats = await blockchain_monitor.get_real_time_stats()
        
        # Get Web3 integration summary
        web3_summary = await web3_integration.get_multi_chain_summary()
        
        # Get analytics dashboard data
        analytics_data = realtime_analytics.get_dashboard_data()
        
        return {
            "phase": "2",
            "status": "operational",
            "timestamp": datetime.now().isoformat(),
            "blockchain_monitoring": blockchain_stats,
            "web3_integration": web3_summary,
            "analytics_summary": {
                "metrics_tracked": len(analytics_data["metrics"]),
                "recent_alerts": len(analytics_data["recent_alerts"]),
                "threat_level": analytics_data["threat_summary"]["current_threat_level"],
                "network_health": analytics_data["network_health"]["overall_score"]
            }
        }
    except Exception as e:
        logger.error(f"Error getting Phase 2 status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# BLOCKCHAIN MONITORING ENDPOINTS
# ============================================================================

@app.get("/api/blockchain/monitoring/stats")
async def get_blockchain_monitoring_stats():
    """Get real-time blockchain monitoring statistics"""
    try:
        stats = await blockchain_monitor.get_real_time_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting blockchain stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/blockchain/contract/analyze")
async def analyze_smart_contract(request: SmartContractAnalysisRequest):
    """Analyze smart contract for vulnerabilities"""
    try:
        analysis = await blockchain_monitor.analyze_smart_contract(
            request.chain_id, 
            request.contract_address
        )
        return analysis
    except Exception as e:
        logger.error(f"Error analyzing contract: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/blockchain/events/recent")
async def get_recent_blockchain_events(limit: int = Query(10, ge=1, le=100)):
    """Get recent blockchain security events"""
    try:
        # For now, return mock events since we're not running full monitoring
        events = []
        for i in range(min(limit, 5)):
            events.append({
                "event_id": f"mock_event_{i}",
                "chain_id": 1,
                "event_type": "CONTRACT_INTERACTION",
                "risk_score": 0.3 + (i * 0.1),
                "timestamp": datetime.now().isoformat(),
                "description": f"Mock blockchain event {i}"
            })
        
        return {"events": events, "total": len(events)}
    except Exception as e:
        logger.error(f"Error getting recent events: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# REAL-TIME ANALYTICS ENDPOINTS
# ============================================================================

@app.get("/api/analytics/dashboard")
async def get_analytics_dashboard():
    """Get comprehensive analytics dashboard data"""
    try:
        dashboard_data = realtime_analytics.get_dashboard_data()
        return dashboard_data
    except Exception as e:
        logger.error(f"Error getting dashboard data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/metrics/{metric_name}")
async def get_metric_history(
    metric_name: str, 
    hours: int = Query(24, ge=1, le=168)
):
    """Get historical data for a specific metric"""
    try:
        history = realtime_analytics.get_historical_data(metric_name, hours)
        return {
            "metric_name": metric_name,
            "hours": hours,
            "data": history
        }
    except Exception as e:
        logger.error(f"Error getting metric history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/alerts/recent")
async def get_recent_alerts(limit: int = Query(10, ge=1, le=50)):
    """Get recent threat alerts"""
    try:
        dashboard_data = realtime_analytics.get_dashboard_data()
        alerts = dashboard_data["recent_alerts"][:limit]
        return {"alerts": alerts, "total": len(alerts)}
    except Exception as e:
        logger.error(f"Error getting recent alerts: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/threat-summary")
async def get_threat_summary():
    """Get current threat summary"""
    try:
        dashboard_data = realtime_analytics.get_dashboard_data()
        return dashboard_data["threat_summary"]
    except Exception as e:
        logger.error(f"Error getting threat summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# WEB3 INTEGRATION ENDPOINTS
# ============================================================================

@app.get("/api/web3/chains/summary")
async def get_multi_chain_summary():
    """Get summary across all connected blockchain networks"""
    try:
        summary = await web3_integration.get_multi_chain_summary()
        return summary
    except Exception as e:
        logger.error(f"Error getting multi-chain summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/web3/token/info")
async def get_token_info(chain_id: int, token_address: str):
    """Get detailed token information"""
    try:
        token_info = await web3_integration.get_token_info(chain_id, token_address)
        if token_info:
            return {
                "address": token_info.address,
                "symbol": token_info.symbol,
                "name": token_info.name,
                "decimals": token_info.decimals,
                "chain_id": token_info.chain_id,
                "price_usd": token_info.price_usd,
                "market_cap": token_info.market_cap
            }
        else:
            raise HTTPException(status_code=404, detail="Token not found")
    except Exception as e:
        logger.error(f"Error getting token info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/web3/pool/analyze")
async def analyze_liquidity_pool(request: LiquidityPoolRequest):
    """Analyze a liquidity pool"""
    try:
        pool_info = await web3_integration.analyze_liquidity_pool(
            request.chain_id, 
            request.pool_address
        )
        if pool_info:
            return {
                "pool_address": pool_info.pool_address,
                "token0": {
                    "address": pool_info.token0.address,
                    "symbol": pool_info.token0.symbol,
                    "name": pool_info.token0.name
                },
                "token1": {
                    "address": pool_info.token1.address,
                    "symbol": pool_info.token1.symbol,
                    "name": pool_info.token1.name
                },
                "reserve0": pool_info.reserve0,
                "reserve1": pool_info.reserve1,
                "fee_tier": pool_info.fee_tier,
                "protocol": pool_info.protocol
            }
        else:
            raise HTTPException(status_code=404, detail="Pool not found")
    except Exception as e:
        logger.error(f"Error analyzing pool: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/web3/transaction/simulate")
async def simulate_transaction(request: TransactionSimulationRequest):
    """Simulate a transaction to predict outcomes"""
    try:
        simulation = await web3_integration.simulate_transaction(
            request.chain_id,
            {
                "to": request.to,
                "value": request.value,
                "gas_limit": request.gas_limit,
                "data": request.data
            }
        )
        return simulation
    except Exception as e:
        logger.error(f"Error simulating transaction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# DEFI SECURITY ENDPOINTS
# ============================================================================

@app.post("/api/defi/risks/analyze")
async def analyze_defi_risks(request: DeFiRiskRequest):
    """Analyze risks in DeFi protocols"""
    try:
        risks = await web3_integration.detect_defi_risks(
            request.chain_id, 
            request.protocol_name
        )
        return risks
    except Exception as e:
        logger.error(f"Error analyzing DeFi risks: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/defi/protocols/health/{chain_id}")
async def get_defi_protocol_health(chain_id: int):
    """Get health metrics for DeFi protocols on a chain"""
    try:
        health = await web3_integration.get_defi_protocol_health(chain_id)
        return health
    except Exception as e:
        logger.error(f"Error getting DeFi protocol health: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/defi/flash-loans/{chain_id}")
async def monitor_flash_loan_activity(chain_id: int):
    """Monitor flash loan activity for potential attacks"""
    try:
        activity = await web3_integration.monitor_flash_loan_activity(chain_id)
        return activity
    except Exception as e:
        logger.error(f"Error monitoring flash loans: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/defi/mev/{chain_id}")
async def analyze_mev_opportunities(chain_id: int):
    """Analyze MEV (Maximal Extractable Value) opportunities"""
    try:
        mev_analysis = await web3_integration.analyze_mev_opportunities(chain_id)
        return mev_analysis
    except Exception as e:
        logger.error(f"Error analyzing MEV: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# ADVANCED ANALYTICS ENDPOINTS
# ============================================================================

@app.get("/api/analytics/network-health")
async def get_network_health():
    """Get comprehensive network health metrics"""
    try:
        dashboard_data = realtime_analytics.get_dashboard_data()
        return dashboard_data["network_health"]
    except Exception as e:
        logger.error(f"Error getting network health: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/time-series/{metric}")
async def get_time_series_data(metric: str):
    """Get time series data for charts"""
    try:
        dashboard_data = realtime_analytics.get_dashboard_data()
        if metric in dashboard_data["time_series"]:
            return {
                "metric": metric,
                "data": list(dashboard_data["time_series"][metric])
            }
        else:
            raise HTTPException(status_code=404, detail="Metric not found")
    except Exception as e:
        logger.error(f"Error getting time series data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/insights")
async def get_ai_insights():
    """Get AI-generated security insights"""
    try:
        # Mock AI insights for now
        insights = [
            {
                "type": "trend_analysis",
                "message": "Threat levels have decreased by 15% in the last hour",
                "confidence": 0.85,
                "timestamp": datetime.now().isoformat()
            },
            {
                "type": "pattern_detection",
                "message": "Unusual gas price spike detected on Ethereum",
                "confidence": 0.72,
                "timestamp": datetime.now().isoformat()
            },
            {
                "type": "risk_assessment",
                "message": "DeFi protocol health remains stable across all chains",
                "confidence": 0.91,
                "timestamp": datetime.now().isoformat()
            }
        ]
        return {"insights": insights}
    except Exception as e:
        logger.error(f"Error getting AI insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# LEGACY ENDPOINTS (for backward compatibility)
# ============================================================================

@app.get("/api/threat-intelligence")
async def get_threat_intelligence():
    """Legacy threat intelligence endpoint"""
    try:
        dashboard_data = realtime_analytics.get_dashboard_data()
        return {
            "threats": dashboard_data["recent_alerts"][:5],
            "threat_level": dashboard_data["threat_summary"]["current_threat_level"],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting threat intelligence: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/real-time")
async def get_real_time_analytics():
    """Legacy real-time analytics endpoint"""
    try:
        dashboard_data = realtime_analytics.get_dashboard_data()
        return {
            "active_threats": dashboard_data["threat_summary"]["active_threats"],
            "defense_effectiveness": dashboard_data["network_health"]["defense_effectiveness"],
            "network_health": dashboard_data["network_health"]["overall_score"],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting real-time analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    logger.info("🚀 Launching Quantum-AI Cyber God Phase 2 Server...")
    uvicorn.run(
        "phase2_server:app",
        host="0.0.0.0",
        port=8002,
        reload=False,
        log_level="info"
    ) 