"""
🎮 QUANTUM-AI CYBER GOD - PHASE 3 SERVER
War Games Platform with competitive security challenges and leaderboards
"""

import asyncio
import json
import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from contextlib import asynccontextmanager
from enum import Enum

from fastapi import FastAPI, HTTPException, BackgroundTasks, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn

# Import Phase 3 services
from services.war_games_engine import war_games_engine
from services.challenge_manager import challenge_manager
from services.leaderboard_system import leaderboard_system
from services.team_manager import team_manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Enums for game mechanics
class ChallengeType(str, Enum):
    SMART_CONTRACT_AUDIT = "smart_contract_audit"
    DEFI_EXPLOIT = "defi_exploit"
    FLASH_LOAN_ATTACK = "flash_loan_attack"
    MEV_EXTRACTION = "mev_extraction"
    GOVERNANCE_ATTACK = "governance_attack"
    BRIDGE_EXPLOIT = "bridge_exploit"
    ORACLE_MANIPULATION = "oracle_manipulation"
    REENTRANCY_HUNT = "reentrancy_hunt"

class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"
    LEGENDARY = "legendary"

class GameMode(str, Enum):
    SOLO = "solo"
    TEAM = "team"
    TOURNAMENT = "tournament"
    CAPTURE_THE_FLAG = "ctf"
    KING_OF_THE_HILL = "koth"

# Pydantic models for API requests
class PlayerRegistration(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: str = Field(..., description="Player email")
    skill_level: DifficultyLevel = Field(default=DifficultyLevel.BEGINNER)
    preferred_challenges: List[ChallengeType] = Field(default=[])

class TeamCreation(BaseModel):
    team_name: str = Field(..., min_length=3, max_length=30)
    description: str = Field(default="", max_length=200)
    max_members: int = Field(default=4, ge=2, le=10)
    is_public: bool = Field(default=True)

class ChallengeSubmission(BaseModel):
    challenge_id: str = Field(..., description="Challenge identifier")
    player_id: str = Field(..., description="Player identifier")
    solution_code: str = Field(..., description="Solution code or exploit")
    explanation: str = Field(..., description="Explanation of the solution")
    time_taken: int = Field(..., description="Time taken in seconds")

class TournamentCreation(BaseModel):
    name: str = Field(..., min_length=5, max_length=50)
    description: str = Field(..., max_length=500)
    start_time: datetime = Field(..., description="Tournament start time")
    duration_hours: int = Field(..., ge=1, le=168)
    max_participants: int = Field(default=100, ge=2, le=1000)
    entry_fee: float = Field(default=0.0, ge=0.0)
    prize_pool: float = Field(default=0.0, ge=0.0)
    game_mode: GameMode = Field(default=GameMode.SOLO)

# Global state for active connections
active_connections: Dict[str, WebSocket] = {}
active_games: Dict[str, Dict] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan"""
    logger.info("🎮 Starting Quantum-AI Cyber God Phase 3 - War Games Platform...")
    
    try:
        # Initialize War Games services
        await war_games_engine.initialize()
        await challenge_manager.load_challenges()
        await leaderboard_system.initialize()
        await team_manager.initialize()
        
        # Start background game mechanics
        asyncio.create_task(war_games_engine.start_game_loop())
        asyncio.create_task(leaderboard_system.update_rankings())
        
        logger.info("✅ Phase 3 War Games Platform initialized successfully")
        
    except Exception as e:
        logger.error(f"❌ Error initializing War Games Platform: {e}")
    
    yield
    
    # Cleanup
    logger.info("🛑 Shutting down War Games Platform...")
    await war_games_engine.shutdown()

# Create FastAPI app with lifespan
app = FastAPI(
    title="Quantum-AI Cyber God - Phase 3 War Games",
    description="Competitive cybersecurity challenges and tournaments",
    version="3.0.0",
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
        "phase": "3",
        "platform": "war_games",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "war_games_engine": war_games_engine.is_active,
            "challenge_manager": challenge_manager.is_loaded,
            "leaderboard_system": leaderboard_system.is_active,
            "team_manager": team_manager.is_active
        },
        "active_players": len(active_connections),
        "active_games": len(active_games)
    }

@app.get("/api/status/phase3")
async def phase3_status():
    """Get Phase 3 War Games Platform status"""
    try:
        stats = await war_games_engine.get_platform_stats()
        return {
            "phase": "3",
            "status": "operational",
            "platform": "war_games",
            "timestamp": datetime.now().isoformat(),
            "statistics": stats,
            "active_challenges": await challenge_manager.get_active_challenges_count(),
            "total_players": await leaderboard_system.get_total_players(),
            "active_tournaments": await war_games_engine.get_active_tournaments_count()
        }
    except Exception as e:
        logger.error(f"Error getting Phase 3 status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# PLAYER MANAGEMENT ENDPOINTS
# ============================================================================

@app.post("/api/players/register")
async def register_player(registration: PlayerRegistration):
    """Register a new player for the War Games Platform"""
    try:
        player = await war_games_engine.register_player(
            username=registration.username,
            email=registration.email,
            skill_level=registration.skill_level,
            preferred_challenges=registration.preferred_challenges
        )
        return {
            "success": True,
            "player_id": player["player_id"],
            "message": f"Welcome to the War Games, {registration.username}!",
            "starting_rank": player["rank"],
            "available_challenges": await challenge_manager.get_challenges_for_level(registration.skill_level)
        }
    except Exception as e:
        logger.error(f"Error registering player: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/players/{player_id}/profile")
async def get_player_profile(player_id: str):
    """Get player profile and statistics"""
    try:
        profile = await war_games_engine.get_player_profile(player_id)
        return profile
    except Exception as e:
        logger.error(f"Error getting player profile: {e}")
        raise HTTPException(status_code=404, detail="Player not found")

@app.get("/api/players/{player_id}/achievements")
async def get_player_achievements(player_id: str):
    """Get player achievements and badges"""
    try:
        achievements = await war_games_engine.get_player_achievements(player_id)
        return achievements
    except Exception as e:
        logger.error(f"Error getting player achievements: {e}")
        raise HTTPException(status_code=404, detail="Player not found")

# ============================================================================
# CHALLENGE MANAGEMENT ENDPOINTS
# ============================================================================

@app.get("/api/challenges")
async def get_available_challenges(
    difficulty: Optional[DifficultyLevel] = None,
    challenge_type: Optional[ChallengeType] = None,
    limit: int = Query(20, ge=1, le=100)
):
    """Get available challenges"""
    try:
        challenges = await challenge_manager.get_challenges(
            difficulty=difficulty,
            challenge_type=challenge_type,
            limit=limit
        )
        return {"challenges": challenges, "total": len(challenges)}
    except Exception as e:
        logger.error(f"Error getting challenges: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/challenges/{challenge_id}")
async def get_challenge_details(challenge_id: str):
    """Get detailed information about a specific challenge"""
    try:
        challenge = await challenge_manager.get_challenge_details(challenge_id)
        return challenge
    except Exception as e:
        logger.error(f"Error getting challenge details: {e}")
        raise HTTPException(status_code=404, detail="Challenge not found")

@app.post("/api/challenges/{challenge_id}/start")
async def start_challenge(challenge_id: str, player_id: str):
    """Start a challenge for a player"""
    try:
        game_session = await war_games_engine.start_challenge(challenge_id, player_id)
        return {
            "success": True,
            "session_id": game_session["session_id"],
            "challenge": game_session["challenge"],
            "start_time": game_session["start_time"],
            "time_limit": game_session["time_limit"]
        }
    except Exception as e:
        logger.error(f"Error starting challenge: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/challenges/submit")
async def submit_challenge_solution(submission: ChallengeSubmission):
    """Submit a solution for a challenge"""
    try:
        result = await war_games_engine.submit_solution(
            challenge_id=submission.challenge_id,
            player_id=submission.player_id,
            solution_code=submission.solution_code,
            explanation=submission.explanation,
            time_taken=submission.time_taken
        )
        return result
    except Exception as e:
        logger.error(f"Error submitting solution: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# ============================================================================
# TEAM MANAGEMENT ENDPOINTS
# ============================================================================

@app.post("/api/teams/create")
async def create_team(team_data: TeamCreation, creator_id: str):
    """Create a new team"""
    try:
        team = await team_manager.create_team(
            team_name=team_data.team_name,
            description=team_data.description,
            creator_id=creator_id,
            max_members=team_data.max_members,
            is_public=team_data.is_public
        )
        return {
            "success": True,
            "team_id": team["team_id"],
            "message": f"Team '{team_data.team_name}' created successfully!",
            "team": team
        }
    except Exception as e:
        logger.error(f"Error creating team: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/teams/{team_id}/join")
async def join_team(team_id: str, player_id: str):
    """Join a team"""
    try:
        result = await team_manager.join_team(team_id, player_id)
        return result
    except Exception as e:
        logger.error(f"Error joining team: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/teams/{team_id}")
async def get_team_details(team_id: str):
    """Get team details and member information"""
    try:
        team = await team_manager.get_team_details(team_id)
        return team
    except Exception as e:
        logger.error(f"Error getting team details: {e}")
        raise HTTPException(status_code=404, detail="Team not found")

# ============================================================================
# LEADERBOARD ENDPOINTS
# ============================================================================

@app.get("/api/leaderboard/global")
async def get_global_leaderboard(limit: int = Query(50, ge=1, le=100)):
    """Get global leaderboard"""
    try:
        leaderboard = await leaderboard_system.get_global_leaderboard(limit)
        return leaderboard
    except Exception as e:
        logger.error(f"Error getting global leaderboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/leaderboard/teams")
async def get_team_leaderboard(limit: int = Query(20, ge=1, le=50)):
    """Get team leaderboard"""
    try:
        leaderboard = await leaderboard_system.get_team_leaderboard(limit)
        return leaderboard
    except Exception as e:
        logger.error(f"Error getting team leaderboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/leaderboard/challenge/{challenge_type}")
async def get_challenge_leaderboard(challenge_type: ChallengeType, limit: int = Query(20, ge=1, le=50)):
    """Get leaderboard for specific challenge type"""
    try:
        leaderboard = await leaderboard_system.get_challenge_leaderboard(challenge_type, limit)
        return leaderboard
    except Exception as e:
        logger.error(f"Error getting challenge leaderboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# TOURNAMENT ENDPOINTS
# ============================================================================

@app.post("/api/tournaments/create")
async def create_tournament(tournament: TournamentCreation, organizer_id: str):
    """Create a new tournament"""
    try:
        new_tournament = await war_games_engine.create_tournament(
            name=tournament.name,
            description=tournament.description,
            organizer_id=organizer_id,
            start_time=tournament.start_time,
            duration_hours=tournament.duration_hours,
            max_participants=tournament.max_participants,
            entry_fee=tournament.entry_fee,
            prize_pool=tournament.prize_pool,
            game_mode=tournament.game_mode
        )
        return {
            "success": True,
            "tournament_id": new_tournament["tournament_id"],
            "message": f"Tournament '{tournament.name}' created successfully!",
            "tournament": new_tournament
        }
    except Exception as e:
        logger.error(f"Error creating tournament: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/tournaments/active")
async def get_active_tournaments():
    """Get list of active tournaments"""
    try:
        tournaments = await war_games_engine.get_active_tournaments()
        return {"tournaments": tournaments, "total": len(tournaments)}
    except Exception as e:
        logger.error(f"Error getting active tournaments: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/tournaments/{tournament_id}/join")
async def join_tournament(tournament_id: str, player_id: str):
    """Join a tournament"""
    try:
        result = await war_games_engine.join_tournament(tournament_id, player_id)
        return result
    except Exception as e:
        logger.error(f"Error joining tournament: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# ============================================================================
# REAL-TIME WEBSOCKET ENDPOINTS
# ============================================================================

@app.websocket("/ws/game/{player_id}")
async def websocket_game_endpoint(websocket: WebSocket, player_id: str):
    """WebSocket endpoint for real-time game updates"""
    await websocket.accept()
    active_connections[player_id] = websocket
    
    try:
        while True:
            # Send periodic updates
            game_state = await war_games_engine.get_player_game_state(player_id)
            await websocket.send_json(game_state)
            await asyncio.sleep(1)  # Update every second
            
    except WebSocketDisconnect:
        logger.info(f"Player {player_id} disconnected")
    except Exception as e:
        logger.error(f"WebSocket error for player {player_id}: {e}")
    finally:
        if player_id in active_connections:
            del active_connections[player_id]

@app.websocket("/ws/tournament/{tournament_id}")
async def websocket_tournament_endpoint(websocket: WebSocket, tournament_id: str):
    """WebSocket endpoint for real-time tournament updates"""
    await websocket.accept()
    
    try:
        while True:
            # Send tournament updates
            tournament_state = await war_games_engine.get_tournament_state(tournament_id)
            await websocket.send_json(tournament_state)
            await asyncio.sleep(5)  # Update every 5 seconds
            
    except WebSocketDisconnect:
        logger.info(f"Tournament {tournament_id} viewer disconnected")
    except Exception as e:
        logger.error(f"WebSocket error for tournament {tournament_id}: {e}")

# ============================================================================
# ANALYTICS & INSIGHTS ENDPOINTS
# ============================================================================

@app.get("/api/analytics/platform-stats")
async def get_platform_analytics():
    """Get comprehensive platform analytics"""
    try:
        stats = await war_games_engine.get_comprehensive_analytics()
        return stats
    except Exception as e:
        logger.error(f"Error getting platform analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/player-insights/{player_id}")
async def get_player_insights(player_id: str):
    """Get AI-powered insights for a player"""
    try:
        insights = await war_games_engine.get_player_insights(player_id)
        return insights
    except Exception as e:
        logger.error(f"Error getting player insights: {e}")
        raise HTTPException(status_code=404, detail="Player not found")

# ============================================================================
# MAIN SERVER STARTUP
# ============================================================================

if __name__ == "__main__":
    print("🎮 QUANTUM-AI CYBER GOD - PHASE 3 WAR GAMES PLATFORM 🎮")
    print("=" * 60)
    print("🚀 Starting War Games Platform on port 8003...")
    print("🌐 Dashboard: Open phase3_dashboard.html")
    print("📊 API Docs: http://localhost:8003/docs")
    print("🔍 Health Check: http://localhost:8003/health")
    print("=" * 60)
    
    uvicorn.run(
        "phase3_server:app",
        host="0.0.0.0",
        port=8003,
        reload=True,
        log_level="info"
    ) 