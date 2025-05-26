"""
Quantum-AI Cyber God Backend
Main FastAPI application for the decentralized cyber warfare simulator
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import asyncio
import json
import logging
from typing import List, Dict, Any, Optional
import uvicorn
from datetime import datetime, timedelta
import redis
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Import our custom modules
from models.database import Base, get_db
from models.schemas import (
    ThreatIntelligence, AttackSimulation, SecurityReport,
    SmartContractAnalysis, UserProfile, WarGameSession
)
from services.ai_engine import QuantumAIEngine
from services.blockchain_service import BlockchainService
from services.threat_intelligence import ThreatIntelligenceService
from services.attack_simulator import AttackSimulatorService
from services.defense_automation import DefenseAutomationService
from utils.security import verify_token, create_access_token
from utils.websocket_manager import WebSocketManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Redis connection
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    decode_responses=True
)

# Initialize WebSocket manager
websocket_manager = WebSocketManager()

# Initialize services
ai_engine = QuantumAIEngine()
blockchain_service = BlockchainService()
threat_intel_service = ThreatIntelligenceService()
attack_simulator = AttackSimulatorService()
defense_automation = DefenseAutomationService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("🚀 Starting Quantum-AI Cyber God Backend...")
    
    # Initialize AI models
    await ai_engine.initialize()
    
    # Start background tasks
    asyncio.create_task(threat_intel_service.start_monitoring())
    asyncio.create_task(ai_engine.start_continuous_learning())
    
    logger.info("✅ Backend initialization complete!")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Quantum-AI Cyber God Backend...")
    await ai_engine.cleanup()

# Create FastAPI app
app = FastAPI(
    title="Quantum-AI Cyber God API",
    description="The Ultimate Web3 Defense System API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "ai_engine": ai_engine.is_healthy(),
            "blockchain": blockchain_service.is_connected(),
            "redis": redis_client.ping(),
            "threat_intel": threat_intel_service.is_active()
        }
    }

# Authentication endpoints
@app.post("/auth/login")
async def login(credentials: dict):
    """User authentication"""
    # Implement Web3 wallet authentication
    wallet_address = credentials.get("wallet_address")
    signature = credentials.get("signature")
    
    if blockchain_service.verify_signature(wallet_address, signature):
        token = create_access_token({"wallet": wallet_address})
        return {"access_token": token, "token_type": "bearer"}
    
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Threat Intelligence endpoints
@app.get("/api/threat-intelligence")
async def get_threat_intelligence(
    limit: int = 100,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get latest threat intelligence data"""
    user = verify_token(credentials.credentials)
    threats = await threat_intel_service.get_latest_threats(limit)
    return {"threats": threats, "count": len(threats)}

@app.post("/api/threat-intelligence/scan")
async def scan_for_threats(
    target: dict,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Initiate threat scanning for a target"""
    user = verify_token(credentials.credentials)
    
    scan_id = await threat_intel_service.start_scan(
        target_address=target.get("address"),
        scan_type=target.get("type", "comprehensive"),
        user_id=user["wallet"]
    )
    
    return {"scan_id": scan_id, "status": "initiated"}

# Smart Contract Analysis endpoints
@app.post("/api/smart-contract/analyze")
async def analyze_smart_contract(
    contract_data: dict,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Analyze smart contract for vulnerabilities"""
    user = verify_token(credentials.credentials)
    
    analysis_result = await ai_engine.analyze_smart_contract(
        contract_code=contract_data.get("code"),
        contract_address=contract_data.get("address"),
        blockchain=contract_data.get("blockchain", "ethereum")
    )
    
    return {
        "analysis_id": analysis_result["id"],
        "vulnerabilities": analysis_result["vulnerabilities"],
        "risk_score": analysis_result["risk_score"],
        "recommendations": analysis_result["recommendations"]
    }

# Attack Simulation endpoints
@app.post("/api/attack-simulation/start")
async def start_attack_simulation(
    simulation_config: dict,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Start automated attack simulation"""
    user = verify_token(credentials.credentials)
    
    simulation_id = await attack_simulator.start_simulation(
        target_contract=simulation_config.get("contract_address"),
        attack_vectors=simulation_config.get("attack_vectors", ["all"]),
        intensity=simulation_config.get("intensity", "medium"),
        user_id=user["wallet"]
    )
    
    return {"simulation_id": simulation_id, "status": "started"}

@app.get("/api/attack-simulation/{simulation_id}")
async def get_simulation_results(
    simulation_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get attack simulation results"""
    user = verify_token(credentials.credentials)
    results = await attack_simulator.get_results(simulation_id)
    return results

# Defense Automation endpoints
@app.post("/api/defense/auto-patch")
async def auto_patch_vulnerabilities(
    patch_request: dict,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Automatically generate and apply security patches"""
    user = verify_token(credentials.credentials)
    
    patch_result = await defense_automation.generate_patch(
        contract_address=patch_request.get("contract_address"),
        vulnerabilities=patch_request.get("vulnerabilities"),
        auto_apply=patch_request.get("auto_apply", False)
    )
    
    return patch_result

# War Games endpoints
@app.post("/api/war-games/create")
async def create_war_game(
    game_config: dict,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Create a new war game session"""
    user = verify_token(credentials.credentials)
    
    game_id = await ai_engine.create_war_game(
        name=game_config.get("name"),
        difficulty=game_config.get("difficulty", "medium"),
        participants=game_config.get("participants", [user["wallet"]]),
        duration=game_config.get("duration", 3600)  # 1 hour default
    )
    
    return {"game_id": game_id, "status": "created"}

@app.get("/api/war-games/leaderboard")
async def get_leaderboard():
    """Get war games leaderboard"""
    leaderboard = await ai_engine.get_leaderboard()
    return {"leaderboard": leaderboard}

# Real-time AI Analytics
@app.get("/api/analytics/real-time")
async def get_real_time_analytics(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get real-time security analytics"""
    user = verify_token(credentials.credentials)
    
    analytics = await ai_engine.get_real_time_analytics()
    return analytics

# WebSocket endpoint for real-time updates
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for real-time communication"""
    await websocket_manager.connect(websocket, client_id)
    
    try:
        while True:
            # Listen for client messages
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message["type"] == "subscribe_threats":
                await websocket_manager.subscribe_to_threats(client_id)
            elif message["type"] == "subscribe_simulations":
                await websocket_manager.subscribe_to_simulations(client_id)
            elif message["type"] == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))
                
    except WebSocketDisconnect:
        websocket_manager.disconnect(client_id)

# Background task for broadcasting updates
@app.on_event("startup")
async def start_background_tasks():
    """Start background tasks for real-time updates"""
    asyncio.create_task(broadcast_threat_updates())
    asyncio.create_task(broadcast_simulation_updates())

async def broadcast_threat_updates():
    """Broadcast threat intelligence updates to connected clients"""
    while True:
        try:
            # Get latest threats
            threats = await threat_intel_service.get_latest_threats(10)
            
            # Broadcast to subscribed clients
            await websocket_manager.broadcast_to_subscribers(
                "threats",
                {"type": "threat_update", "data": threats}
            )
            
            await asyncio.sleep(30)  # Update every 30 seconds
            
        except Exception as e:
            logger.error(f"Error broadcasting threat updates: {e}")
            await asyncio.sleep(60)

async def broadcast_simulation_updates():
    """Broadcast simulation updates to connected clients"""
    while True:
        try:
            # Get active simulations
            simulations = await attack_simulator.get_active_simulations()
            
            # Broadcast to subscribed clients
            await websocket_manager.broadcast_to_subscribers(
                "simulations",
                {"type": "simulation_update", "data": simulations}
            )
            
            await asyncio.sleep(10)  # Update every 10 seconds
            
        except Exception as e:
            logger.error(f"Error broadcasting simulation updates: {e}")
            await asyncio.sleep(30)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 