"""
🎮 WAR GAMES ENGINE - PHASE 3
Core engine for managing competitive cybersecurity challenges and tournaments
"""

import asyncio
import json
import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import random

logger = logging.getLogger(__name__)

class WarGamesEngine:
    def __init__(self):
        self.is_active = False
        self.players = {}
        self.active_sessions = {}
        self.tournaments = {}
        self.game_loop_task = None
        
        # Mock data for demonstration
        self.mock_challenges = self._generate_mock_challenges()
        self.mock_players = self._generate_mock_players()
        
    async def initialize(self):
        """Initialize the war games engine"""
        try:
            logger.info("🎮 Initializing War Games Engine...")
            self.is_active = True
            
            # Load existing data (in production, this would be from database)
            await self._load_game_data()
            
            logger.info("✅ War Games Engine initialized successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Error initializing War Games Engine: {e}")
            return False
    
    async def shutdown(self):
        """Shutdown the war games engine"""
        logger.info("🛑 Shutting down War Games Engine...")
        self.is_active = False
        
        if self.game_loop_task:
            self.game_loop_task.cancel()
    
    async def start_game_loop(self):
        """Start the main game loop for background processing"""
        self.game_loop_task = asyncio.create_task(self._game_loop())
    
    async def _game_loop(self):
        """Main game loop for processing background tasks"""
        while self.is_active:
            try:
                # Update tournament states
                await self._update_tournaments()
                
                # Process active game sessions
                await self._process_active_sessions()
                
                # Update player statistics
                await self._update_player_stats()
                
                # Sleep for 5 seconds before next iteration
                await asyncio.sleep(5)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in game loop: {e}")
                await asyncio.sleep(1)
    
    async def register_player(self, username: str, email: str, skill_level: str, preferred_challenges: List[str]):
        """Register a new player"""
        player_id = str(uuid.uuid4())
        
        player = {
            "player_id": player_id,
            "username": username,
            "email": email,
            "skill_level": skill_level,
            "preferred_challenges": preferred_challenges,
            "rank": 1000,  # Starting rank
            "score": 0,
            "challenges_completed": 0,
            "tournaments_won": 0,
            "achievements": [],
            "created_at": datetime.now().isoformat(),
            "last_active": datetime.now().isoformat(),
            "stats": {
                "total_time_played": 0,
                "fastest_solve": None,
                "favorite_challenge_type": None,
                "win_rate": 0.0
            }
        }
        
        self.players[player_id] = player
        logger.info(f"✅ Player registered: {username} ({player_id})")
        
        return player
    
    async def get_player_profile(self, player_id: str):
        """Get player profile and statistics"""
        if player_id not in self.players:
            raise ValueError("Player not found")
        
        player = self.players[player_id]
        
        # Add dynamic statistics
        profile = player.copy()
        profile["current_rank"] = await self._calculate_player_rank(player_id)
        profile["recent_activity"] = await self._get_recent_activity(player_id)
        profile["skill_progression"] = await self._get_skill_progression(player_id)
        
        return profile
    
    async def get_player_achievements(self, player_id: str):
        """Get player achievements and badges"""
        if player_id not in self.players:
            raise ValueError("Player not found")
        
        player = self.players[player_id]
        
        # Generate dynamic achievements
        achievements = []
        
        if player["challenges_completed"] >= 1:
            achievements.append({
                "id": "first_blood",
                "name": "First Blood",
                "description": "Complete your first challenge",
                "icon": "🩸",
                "earned_at": player["created_at"]
            })
        
        if player["challenges_completed"] >= 10:
            achievements.append({
                "id": "challenger",
                "name": "Challenger",
                "description": "Complete 10 challenges",
                "icon": "⚔️",
                "earned_at": player["created_at"]
            })
        
        if player["tournaments_won"] >= 1:
            achievements.append({
                "id": "champion",
                "name": "Champion",
                "description": "Win your first tournament",
                "icon": "🏆",
                "earned_at": player["created_at"]
            })
        
        return {
            "player_id": player_id,
            "total_achievements": len(achievements),
            "achievements": achievements,
            "progress": {
                "next_achievement": "Speed Demon - Solve a challenge in under 60 seconds",
                "progress_percentage": min(100, (player["challenges_completed"] / 50) * 100)
            }
        }
    
    async def start_challenge(self, challenge_id: str, player_id: str):
        """Start a challenge for a player"""
        if player_id not in self.players:
            raise ValueError("Player not found")
        
        # Import challenge_manager here to avoid circular imports
        from .challenge_manager import challenge_manager
        
        # Find challenge using the challenge manager
        try:
            challenge = await challenge_manager.get_challenge_details(challenge_id)
        except Exception:
            # Fallback to mock challenges if challenge manager fails
            challenge = None
            for c in self.mock_challenges:
                if c["id"] == challenge_id:
                    challenge = c
                    break
        
        if not challenge:
            raise ValueError("Challenge not found")
        
        session_id = str(uuid.uuid4())
        session = {
            "session_id": session_id,
            "challenge_id": challenge_id,
            "player_id": player_id,
            "challenge": challenge,
            "start_time": datetime.now().isoformat(),
            "time_limit": challenge.get("time_limit", 3600),  # 1 hour default
            "status": "active",
            "hints_used": 0,
            "attempts": 0
        }
        
        self.active_sessions[session_id] = session
        
        logger.info(f"🎯 Challenge started: {challenge['title']} for player {player_id}")
        
        return session
    
    async def submit_solution(self, challenge_id: str, player_id: str, solution_code: str, explanation: str, time_taken: int):
        """Submit a solution for a challenge"""
        # Find active session
        session = None
        for s in self.active_sessions.values():
            if s["challenge_id"] == challenge_id and s["player_id"] == player_id and s["status"] == "active":
                session = s
                break
        
        if not session:
            raise ValueError("No active session found for this challenge")
        
        # Simulate solution evaluation (in production, this would be more sophisticated)
        is_correct = await self._evaluate_solution(challenge_id, solution_code, explanation)
        
        score = 0
        if is_correct:
            # Calculate score based on time, difficulty, and hints used
            base_score = session["challenge"]["points"]
            time_bonus = max(0, (session["time_limit"] - time_taken) / session["time_limit"] * 0.5)
            hint_penalty = session["hints_used"] * 0.1
            score = int(base_score * (1 + time_bonus - hint_penalty))
        
        result = {
            "success": is_correct,
            "score": score,
            "time_taken": time_taken,
            "feedback": await self._generate_feedback(challenge_id, solution_code, is_correct),
            "rank_change": 0,
            "achievements_unlocked": []
        }
        
        if is_correct:
            # Update player stats
            player = self.players[player_id]
            player["score"] += score
            player["challenges_completed"] += 1
            player["last_active"] = datetime.now().isoformat()
            
            # Update session
            session["status"] = "completed"
            session["completion_time"] = datetime.now().isoformat()
            session["score"] = score
            
            # Check for new achievements
            result["achievements_unlocked"] = await self._check_achievements(player_id)
            
            logger.info(f"✅ Challenge completed: {player_id} solved {challenge_id} for {score} points")
        else:
            session["attempts"] += 1
            logger.info(f"❌ Challenge attempt failed: {player_id} for {challenge_id}")
        
        return result
    
    async def create_tournament(self, name: str, description: str, organizer_id: str, 
                              start_time: datetime, duration_hours: int, max_participants: int,
                              entry_fee: float, prize_pool: float, game_mode: str):
        """Create a new tournament"""
        tournament_id = str(uuid.uuid4())
        
        tournament = {
            "tournament_id": tournament_id,
            "name": name,
            "description": description,
            "organizer_id": organizer_id,
            "start_time": start_time.isoformat(),
            "end_time": (start_time + timedelta(hours=duration_hours)).isoformat(),
            "duration_hours": duration_hours,
            "max_participants": max_participants,
            "entry_fee": entry_fee,
            "prize_pool": prize_pool,
            "game_mode": game_mode,
            "status": "upcoming",
            "participants": [],
            "leaderboard": [],
            "challenges": await self._select_tournament_challenges(game_mode),
            "created_at": datetime.now().isoformat()
        }
        
        self.tournaments[tournament_id] = tournament
        
        logger.info(f"🏆 Tournament created: {name} ({tournament_id})")
        
        return tournament
    
    async def join_tournament(self, tournament_id: str, player_id: str):
        """Join a tournament"""
        if tournament_id not in self.tournaments:
            raise ValueError("Tournament not found")
        
        if player_id not in self.players:
            raise ValueError("Player not found")
        
        tournament = self.tournaments[tournament_id]
        
        if len(tournament["participants"]) >= tournament["max_participants"]:
            raise ValueError("Tournament is full")
        
        if player_id in tournament["participants"]:
            raise ValueError("Player already joined this tournament")
        
        tournament["participants"].append(player_id)
        
        return {
            "success": True,
            "message": f"Successfully joined tournament: {tournament['name']}",
            "tournament": tournament,
            "position": len(tournament["participants"])
        }
    
    async def get_active_tournaments(self):
        """Get list of active tournaments"""
        active = []
        current_time = datetime.now()
        
        for tournament in self.tournaments.values():
            start_time = datetime.fromisoformat(tournament["start_time"])
            end_time = datetime.fromisoformat(tournament["end_time"])
            
            if start_time <= current_time <= end_time:
                tournament["status"] = "active"
                active.append(tournament)
            elif current_time < start_time:
                tournament["status"] = "upcoming"
                active.append(tournament)
        
        return active
    
    async def get_active_tournaments_count(self):
        """Get count of active tournaments"""
        tournaments = await self.get_active_tournaments()
        return len(tournaments)
    
    async def get_platform_stats(self):
        """Get comprehensive platform statistics"""
        return {
            "total_players": len(self.players),
            "active_sessions": len(self.active_sessions),
            "total_tournaments": len(self.tournaments),
            "challenges_available": len(self.mock_challenges),
            "total_completions": sum(p["challenges_completed"] for p in self.players.values()),
            "average_score": sum(p["score"] for p in self.players.values()) / max(1, len(self.players)),
            "platform_uptime": "99.9%",
            "last_updated": datetime.now().isoformat()
        }
    
    async def get_comprehensive_analytics(self):
        """Get detailed analytics for the platform"""
        return {
            "player_analytics": {
                "total_registered": len(self.players),
                "active_today": len([p for p in self.players.values() 
                                   if (datetime.now() - datetime.fromisoformat(p["last_active"])).days == 0]),
                "skill_distribution": await self._get_skill_distribution(),
                "retention_rate": 85.5  # Mock data
            },
            "challenge_analytics": {
                "total_challenges": len(self.mock_challenges),
                "completion_rate": 67.8,
                "average_time": 1847,  # seconds
                "difficulty_distribution": await self._get_difficulty_distribution()
            },
            "tournament_analytics": {
                "total_tournaments": len(self.tournaments),
                "average_participants": 23.5,
                "prize_pool_total": sum(t["prize_pool"] for t in self.tournaments.values())
            },
            "performance_metrics": {
                "response_time": "45ms",
                "uptime": "99.9%",
                "concurrent_users": len(self.active_sessions)
            }
        }
    
    async def get_player_insights(self, player_id: str):
        """Get AI-powered insights for a player"""
        if player_id not in self.players:
            raise ValueError("Player not found")
        
        player = self.players[player_id]
        
        return {
            "player_id": player_id,
            "insights": [
                {
                    "type": "strength",
                    "message": f"You excel at {player.get('skill_level', 'beginner')} level challenges",
                    "confidence": 0.85
                },
                {
                    "type": "improvement",
                    "message": "Try focusing on smart contract auditing challenges to improve your ranking",
                    "confidence": 0.72
                },
                {
                    "type": "recommendation",
                    "message": "Join a team tournament to gain collaborative experience",
                    "confidence": 0.68
                }
            ],
            "predicted_rank": player["rank"] + random.randint(-50, 100),
            "skill_trajectory": "improving",
            "recommended_challenges": ["smart_contract_audit", "defi_exploit"],
            "generated_at": datetime.now().isoformat()
        }
    
    async def get_player_game_state(self, player_id: str):
        """Get current game state for a player"""
        if player_id not in self.players:
            return {"error": "Player not found"}
        
        player = self.players[player_id]
        active_session = None
        
        # Find active session for player
        for session in self.active_sessions.values():
            if session["player_id"] == player_id and session["status"] == "active":
                active_session = session
                break
        
        return {
            "player_id": player_id,
            "username": player["username"],
            "current_score": player["score"],
            "rank": player["rank"],
            "active_session": active_session,
            "notifications": await self._get_player_notifications(player_id),
            "timestamp": datetime.now().isoformat()
        }
    
    async def get_tournament_state(self, tournament_id: str):
        """Get current tournament state"""
        if tournament_id not in self.tournaments:
            return {"error": "Tournament not found"}
        
        tournament = self.tournaments[tournament_id]
        
        return {
            "tournament_id": tournament_id,
            "name": tournament["name"],
            "status": tournament["status"],
            "participants": len(tournament["participants"]),
            "max_participants": tournament["max_participants"],
            "leaderboard": tournament["leaderboard"][:10],  # Top 10
            "time_remaining": await self._calculate_time_remaining(tournament),
            "timestamp": datetime.now().isoformat()
        }
    
    # Helper methods
    async def _load_game_data(self):
        """Load game data (mock implementation)"""
        # In production, this would load from database
        pass
    
    async def _update_tournaments(self):
        """Update tournament states"""
        current_time = datetime.now()
        
        for tournament in self.tournaments.values():
            start_time = datetime.fromisoformat(tournament["start_time"])
            end_time = datetime.fromisoformat(tournament["end_time"])
            
            if current_time >= start_time and current_time <= end_time:
                tournament["status"] = "active"
            elif current_time > end_time:
                tournament["status"] = "completed"
    
    async def _process_active_sessions(self):
        """Process active game sessions"""
        current_time = datetime.now()
        
        for session in list(self.active_sessions.values()):
            start_time = datetime.fromisoformat(session["start_time"])
            elapsed = (current_time - start_time).total_seconds()
            
            if elapsed > session["time_limit"]:
                session["status"] = "expired"
                logger.info(f"⏰ Session expired: {session['session_id']}")
    
    async def _update_player_stats(self):
        """Update player statistics"""
        # Mock implementation - in production, this would update various stats
        pass
    
    async def _calculate_player_rank(self, player_id: str):
        """Calculate player's current rank"""
        player = self.players[player_id]
        # Simple ranking based on score
        all_scores = [p["score"] for p in self.players.values()]
        all_scores.sort(reverse=True)
        
        try:
            rank = all_scores.index(player["score"]) + 1
        except ValueError:
            rank = len(all_scores) + 1
        
        return rank
    
    async def _get_recent_activity(self, player_id: str):
        """Get recent activity for a player"""
        return [
            {
                "type": "challenge_completed",
                "description": "Completed Smart Contract Audit Challenge",
                "timestamp": datetime.now().isoformat(),
                "points": 150
            }
        ]
    
    async def _get_skill_progression(self, player_id: str):
        """Get skill progression data"""
        return {
            "current_level": "Intermediate",
            "progress_to_next": 65,
            "skills": {
                "smart_contract_auditing": 75,
                "defi_exploitation": 60,
                "flash_loan_attacks": 45
            }
        }
    
    async def _evaluate_solution(self, challenge_id: str, solution_code: str, explanation: str):
        """Evaluate a solution (mock implementation)"""
        # In production, this would run actual tests
        return random.choice([True, False, True, True])  # 75% success rate
    
    async def _generate_feedback(self, challenge_id: str, solution_code: str, is_correct: bool):
        """Generate feedback for a solution"""
        if is_correct:
            return "Excellent work! Your solution correctly identifies the vulnerability."
        else:
            return "Close, but not quite. Consider checking the reentrancy protection."
    
    async def _check_achievements(self, player_id: str):
        """Check for new achievements"""
        # Mock implementation
        return []
    
    async def _select_tournament_challenges(self, game_mode: str):
        """Select challenges for a tournament"""
        # Return a subset of challenges based on game mode
        return self.mock_challenges[:5]
    
    async def _get_skill_distribution(self):
        """Get skill level distribution"""
        return {
            "beginner": 35,
            "intermediate": 40,
            "advanced": 20,
            "expert": 4,
            "legendary": 1
        }
    
    async def _get_difficulty_distribution(self):
        """Get challenge difficulty distribution"""
        return {
            "beginner": 25,
            "intermediate": 35,
            "advanced": 25,
            "expert": 12,
            "legendary": 3
        }
    
    async def _get_player_notifications(self, player_id: str):
        """Get notifications for a player"""
        return [
            {
                "type": "tournament_starting",
                "message": "Cyber Defense Championship starts in 1 hour!",
                "timestamp": datetime.now().isoformat()
            }
        ]
    
    async def _calculate_time_remaining(self, tournament):
        """Calculate time remaining in tournament"""
        end_time = datetime.fromisoformat(tournament["end_time"])
        remaining = end_time - datetime.now()
        return max(0, int(remaining.total_seconds()))
    
    def _generate_mock_challenges(self):
        """Generate mock challenges for demonstration"""
        return [
            {
                "id": "sc_audit_001",
                "title": "Smart Contract Reentrancy Hunt",
                "description": "Find and exploit the reentrancy vulnerability in this DeFi lending contract",
                "type": "smart_contract_audit",
                "difficulty": "intermediate",
                "points": 250,
                "time_limit": 3600,
                "tags": ["reentrancy", "defi", "solidity"],
                "created_at": datetime.now().isoformat()
            },
            {
                "id": "defi_exploit_001",
                "title": "Flash Loan Arbitrage Attack",
                "description": "Execute a profitable flash loan attack on this AMM protocol",
                "type": "defi_exploit",
                "difficulty": "advanced",
                "points": 500,
                "time_limit": 7200,
                "tags": ["flash_loan", "arbitrage", "amm"],
                "created_at": datetime.now().isoformat()
            },
            {
                "id": "governance_001",
                "title": "DAO Governance Manipulation",
                "description": "Manipulate the voting mechanism to pass a malicious proposal",
                "type": "governance_attack",
                "difficulty": "expert",
                "points": 750,
                "time_limit": 10800,
                "tags": ["dao", "governance", "voting"],
                "created_at": datetime.now().isoformat()
            }
        ]
    
    def _generate_mock_players(self):
        """Generate mock players for demonstration"""
        return {
            "player_001": {
                "player_id": "player_001",
                "username": "CyberNinja",
                "email": "ninja@example.com",
                "skill_level": "advanced",
                "rank": 15,
                "score": 2500,
                "challenges_completed": 12,
                "tournaments_won": 2
            }
        }

# Global instance
war_games_engine = WarGamesEngine() 