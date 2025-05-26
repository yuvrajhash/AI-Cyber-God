"""
🏆 LEADERBOARD SYSTEM - PHASE 3
Manages rankings, scoring, and competitive elements for the War Games Platform
"""

import asyncio
import json
import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import random

logger = logging.getLogger(__name__)

class LeaderboardSystem:
    def __init__(self):
        self.is_active = False
        self.global_rankings = {}
        self.team_rankings = {}
        self.challenge_rankings = {}
        self.seasonal_rankings = {}
        self.update_task = None
        
    async def initialize(self):
        """Initialize the leaderboard system"""
        try:
            logger.info("🏆 Initializing Leaderboard System...")
            
            # Initialize ranking structures
            await self._initialize_rankings()
            
            # Generate mock data for demonstration
            await self._generate_mock_rankings()
            
            self.is_active = True
            logger.info("✅ Leaderboard System initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Error initializing Leaderboard System: {e}")
            self.is_active = False
    
    async def update_rankings(self):
        """Start periodic ranking updates"""
        self.update_task = asyncio.create_task(self._ranking_update_loop())
    
    async def _ranking_update_loop(self):
        """Periodic ranking update loop"""
        while self.is_active:
            try:
                await self._update_global_rankings()
                await self._update_team_rankings()
                await self._update_challenge_rankings()
                await self._update_seasonal_rankings()
                
                # Update every 30 seconds
                await asyncio.sleep(30)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in ranking update loop: {e}")
                await asyncio.sleep(5)
    
    async def get_global_leaderboard(self, limit: int = 50):
        """Get global leaderboard"""
        # Sort players by score and other metrics
        sorted_players = sorted(
            self.global_rankings.values(),
            key=lambda x: (x["total_score"], x["challenges_completed"], -x["average_time"]),
            reverse=True
        )
        
        # Add rank positions
        for i, player in enumerate(sorted_players[:limit]):
            player["rank"] = i + 1
            player["rank_change"] = self._calculate_rank_change(player["player_id"])
        
        return {
            "leaderboard": sorted_players[:limit],
            "total_players": len(self.global_rankings),
            "last_updated": datetime.now().isoformat(),
            "season": "Season 1 - 2025"
        }
    
    async def get_team_leaderboard(self, limit: int = 20):
        """Get team leaderboard"""
        sorted_teams = sorted(
            self.team_rankings.values(),
            key=lambda x: (x["total_score"], x["challenges_completed"], x["tournament_wins"]),
            reverse=True
        )
        
        for i, team in enumerate(sorted_teams[:limit]):
            team["rank"] = i + 1
            team["rank_change"] = self._calculate_team_rank_change(team["team_id"])
        
        return {
            "leaderboard": sorted_teams[:limit],
            "total_teams": len(self.team_rankings),
            "last_updated": datetime.now().isoformat()
        }
    
    async def get_challenge_leaderboard(self, challenge_type: str, limit: int = 20):
        """Get leaderboard for specific challenge type"""
        if challenge_type not in self.challenge_rankings:
            return {"leaderboard": [], "total_players": 0}
        
        sorted_players = sorted(
            self.challenge_rankings[challenge_type].values(),
            key=lambda x: (x["score"], -x["completion_time"]),
            reverse=True
        )
        
        for i, player in enumerate(sorted_players[:limit]):
            player["rank"] = i + 1
        
        return {
            "challenge_type": challenge_type,
            "leaderboard": sorted_players[:limit],
            "total_players": len(self.challenge_rankings[challenge_type]),
            "last_updated": datetime.now().isoformat()
        }
    
    async def get_seasonal_leaderboard(self, season: str = "current", limit: int = 50):
        """Get seasonal leaderboard"""
        current_season = "2025_season_1"
        
        if current_season not in self.seasonal_rankings:
            return {"leaderboard": [], "total_players": 0}
        
        sorted_players = sorted(
            self.seasonal_rankings[current_season].values(),
            key=lambda x: (x["seasonal_score"], x["seasonal_challenges"]),
            reverse=True
        )
        
        for i, player in enumerate(sorted_players[:limit]):
            player["rank"] = i + 1
        
        return {
            "season": current_season,
            "leaderboard": sorted_players[:limit],
            "total_players": len(self.seasonal_rankings[current_season]),
            "season_start": "2025-01-01T00:00:00Z",
            "season_end": "2025-12-31T23:59:59Z",
            "last_updated": datetime.now().isoformat()
        }
    
    async def update_player_score(self, player_id: str, challenge_id: str, score: int, 
                                 completion_time: int, challenge_type: str):
        """Update player score after challenge completion"""
        # Update global rankings
        if player_id not in self.global_rankings:
            self.global_rankings[player_id] = self._create_empty_player_ranking(player_id)
        
        player_ranking = self.global_rankings[player_id]
        player_ranking["total_score"] += score
        player_ranking["challenges_completed"] += 1
        player_ranking["last_active"] = datetime.now().isoformat()
        
        # Update average completion time
        total_time = player_ranking["average_time"] * (player_ranking["challenges_completed"] - 1)
        player_ranking["average_time"] = (total_time + completion_time) / player_ranking["challenges_completed"]
        
        # Update challenge-specific rankings
        if challenge_type not in self.challenge_rankings:
            self.challenge_rankings[challenge_type] = {}
        
        if player_id not in self.challenge_rankings[challenge_type]:
            self.challenge_rankings[challenge_type][player_id] = {
                "player_id": player_id,
                "username": player_ranking["username"],
                "score": 0,
                "completions": 0,
                "best_time": float('inf'),
                "completion_time": completion_time
            }
        
        challenge_ranking = self.challenge_rankings[challenge_type][player_id]
        challenge_ranking["score"] += score
        challenge_ranking["completions"] += 1
        challenge_ranking["best_time"] = min(challenge_ranking["best_time"], completion_time)
        challenge_ranking["completion_time"] = completion_time
        
        # Update seasonal rankings
        current_season = "2025_season_1"
        if current_season not in self.seasonal_rankings:
            self.seasonal_rankings[current_season] = {}
        
        if player_id not in self.seasonal_rankings[current_season]:
            self.seasonal_rankings[current_season][player_id] = {
                "player_id": player_id,
                "username": player_ranking["username"],
                "seasonal_score": 0,
                "seasonal_challenges": 0,
                "season_start": "2025-01-01T00:00:00Z"
            }
        
        seasonal_ranking = self.seasonal_rankings[current_season][player_id]
        seasonal_ranking["seasonal_score"] += score
        seasonal_ranking["seasonal_challenges"] += 1
        
        logger.info(f"🏆 Updated rankings for player {player_id}: +{score} points")
    
    async def update_team_score(self, team_id: str, score: int, challenge_completed: bool = False):
        """Update team score"""
        if team_id not in self.team_rankings:
            self.team_rankings[team_id] = self._create_empty_team_ranking(team_id)
        
        team_ranking = self.team_rankings[team_id]
        team_ranking["total_score"] += score
        
        if challenge_completed:
            team_ranking["challenges_completed"] += 1
        
        team_ranking["last_active"] = datetime.now().isoformat()
        
        logger.info(f"🏆 Updated team rankings for {team_id}: +{score} points")
    
    async def get_player_rank(self, player_id: str):
        """Get current rank for a specific player"""
        if player_id not in self.global_rankings:
            return None
        
        # Get all players sorted by score
        sorted_players = sorted(
            self.global_rankings.values(),
            key=lambda x: (x["total_score"], x["challenges_completed"]),
            reverse=True
        )
        
        for i, player in enumerate(sorted_players):
            if player["player_id"] == player_id:
                return {
                    "rank": i + 1,
                    "total_players": len(sorted_players),
                    "percentile": ((len(sorted_players) - i) / len(sorted_players)) * 100,
                    "score": player["total_score"],
                    "rank_change": self._calculate_rank_change(player_id)
                }
        
        return None
    
    async def get_team_rank(self, team_id: str):
        """Get current rank for a specific team"""
        if team_id not in self.team_rankings:
            return None
        
        sorted_teams = sorted(
            self.team_rankings.values(),
            key=lambda x: (x["total_score"], x["challenges_completed"]),
            reverse=True
        )
        
        for i, team in enumerate(sorted_teams):
            if team["team_id"] == team_id:
                return {
                    "rank": i + 1,
                    "total_teams": len(sorted_teams),
                    "score": team["total_score"],
                    "rank_change": self._calculate_team_rank_change(team_id)
                }
        
        return None
    
    async def get_total_players(self):
        """Get total number of players in rankings"""
        return len(self.global_rankings)
    
    async def get_ranking_statistics(self):
        """Get comprehensive ranking statistics"""
        total_players = len(self.global_rankings)
        total_teams = len(self.team_rankings)
        
        if total_players == 0:
            return {"error": "No ranking data available"}
        
        # Calculate statistics
        all_scores = [p["total_score"] for p in self.global_rankings.values()]
        avg_score = sum(all_scores) / len(all_scores)
        max_score = max(all_scores)
        min_score = min(all_scores)
        
        return {
            "total_players": total_players,
            "total_teams": total_teams,
            "average_score": round(avg_score, 2),
            "highest_score": max_score,
            "lowest_score": min_score,
            "active_seasons": len(self.seasonal_rankings),
            "challenge_categories": len(self.challenge_rankings),
            "last_updated": datetime.now().isoformat()
        }
    
    async def get_top_performers(self, category: str = "overall", limit: int = 10):
        """Get top performers in various categories"""
        if category == "overall":
            sorted_players = sorted(
                self.global_rankings.values(),
                key=lambda x: x["total_score"],
                reverse=True
            )
        elif category == "speed":
            sorted_players = sorted(
                self.global_rankings.values(),
                key=lambda x: x["average_time"]
            )
        elif category == "consistency":
            sorted_players = sorted(
                self.global_rankings.values(),
                key=lambda x: x["challenges_completed"],
                reverse=True
            )
        else:
            return {"error": "Invalid category"}
        
        return {
            "category": category,
            "top_performers": sorted_players[:limit],
            "last_updated": datetime.now().isoformat()
        }
    
    # Helper methods
    async def _initialize_rankings(self):
        """Initialize ranking data structures"""
        self.global_rankings = {}
        self.team_rankings = {}
        self.challenge_rankings = {}
        self.seasonal_rankings = {}
    
    async def _generate_mock_rankings(self):
        """Generate mock ranking data for demonstration"""
        # Generate mock players
        mock_players = [
            {"id": "player_001", "username": "CyberNinja", "score": 2500, "challenges": 15},
            {"id": "player_002", "username": "EthHacker", "score": 2200, "challenges": 12},
            {"id": "player_003", "username": "DeFiExplorer", "score": 1950, "challenges": 18},
            {"id": "player_004", "username": "SmartContractAuditor", "score": 1800, "challenges": 10},
            {"id": "player_005", "username": "MEVBot", "score": 1650, "challenges": 8},
            {"id": "player_006", "username": "FlashLoanMaster", "score": 1500, "challenges": 14},
            {"id": "player_007", "username": "GovernanceHacker", "score": 1350, "challenges": 9},
            {"id": "player_008", "username": "BridgeBreaker", "score": 1200, "challenges": 7},
            {"id": "player_009", "username": "OracleManipulator", "score": 1100, "challenges": 11},
            {"id": "player_010", "username": "ReentrancyHunter", "score": 1000, "challenges": 6}
        ]
        
        for player in mock_players:
            self.global_rankings[player["id"]] = {
                "player_id": player["id"],
                "username": player["username"],
                "total_score": player["score"],
                "challenges_completed": player["challenges"],
                "average_time": random.randint(1200, 3600),
                "last_active": datetime.now().isoformat(),
                "join_date": (datetime.now() - timedelta(days=random.randint(1, 90))).isoformat(),
                "streak": random.randint(0, 10),
                "achievements": random.randint(1, 8)
            }
        
        # Generate mock teams
        mock_teams = [
            {"id": "team_001", "name": "Cyber Guardians", "score": 5000, "challenges": 25},
            {"id": "team_002", "name": "DeFi Defenders", "score": 4500, "challenges": 22},
            {"id": "team_003", "name": "Smart Contract Sleuths", "score": 4200, "challenges": 20},
            {"id": "team_004", "name": "Flash Loan Fighters", "score": 3800, "challenges": 18},
            {"id": "team_005", "name": "MEV Hunters", "score": 3500, "challenges": 16}
        ]
        
        for team in mock_teams:
            self.team_rankings[team["id"]] = {
                "team_id": team["id"],
                "team_name": team["name"],
                "total_score": team["score"],
                "challenges_completed": team["challenges"],
                "member_count": random.randint(3, 8),
                "tournament_wins": random.randint(0, 3),
                "last_active": datetime.now().isoformat(),
                "created_at": (datetime.now() - timedelta(days=random.randint(1, 60))).isoformat()
            }
        
        # Generate challenge-specific rankings
        challenge_types = ["smart_contract_audit", "defi_exploit", "governance_attack", "mev_extraction"]
        
        for challenge_type in challenge_types:
            self.challenge_rankings[challenge_type] = {}
            
            for player in mock_players[:5]:  # Top 5 players for each challenge type
                self.challenge_rankings[challenge_type][player["id"]] = {
                    "player_id": player["id"],
                    "username": player["username"],
                    "score": random.randint(500, 1500),
                    "completions": random.randint(1, 8),
                    "best_time": random.randint(600, 3600),
                    "completion_time": random.randint(900, 3600)
                }
        
        # Generate seasonal rankings
        current_season = "2025_season_1"
        self.seasonal_rankings[current_season] = {}
        
        for player in mock_players:
            self.seasonal_rankings[current_season][player["id"]] = {
                "player_id": player["id"],
                "username": player["username"],
                "seasonal_score": random.randint(800, 2000),
                "seasonal_challenges": random.randint(5, 15),
                "season_start": "2025-01-01T00:00:00Z"
            }
    
    async def _update_global_rankings(self):
        """Update global rankings"""
        # In production, this would recalculate rankings based on recent activity
        pass
    
    async def _update_team_rankings(self):
        """Update team rankings"""
        # In production, this would aggregate team member scores
        pass
    
    async def _update_challenge_rankings(self):
        """Update challenge-specific rankings"""
        # In production, this would update challenge leaderboards
        pass
    
    async def _update_seasonal_rankings(self):
        """Update seasonal rankings"""
        # In production, this would update seasonal leaderboards
        pass
    
    def _create_empty_player_ranking(self, player_id: str):
        """Create empty player ranking entry"""
        return {
            "player_id": player_id,
            "username": f"Player_{player_id[:8]}",
            "total_score": 0,
            "challenges_completed": 0,
            "average_time": 0,
            "last_active": datetime.now().isoformat(),
            "join_date": datetime.now().isoformat(),
            "streak": 0,
            "achievements": 0
        }
    
    def _create_empty_team_ranking(self, team_id: str):
        """Create empty team ranking entry"""
        return {
            "team_id": team_id,
            "team_name": f"Team_{team_id[:8]}",
            "total_score": 0,
            "challenges_completed": 0,
            "member_count": 1,
            "tournament_wins": 0,
            "last_active": datetime.now().isoformat(),
            "created_at": datetime.now().isoformat()
        }
    
    def _calculate_rank_change(self, player_id: str):
        """Calculate rank change for a player (mock implementation)"""
        # In production, this would compare with previous rankings
        return random.randint(-5, 5)
    
    def _calculate_team_rank_change(self, team_id: str):
        """Calculate rank change for a team (mock implementation)"""
        # In production, this would compare with previous rankings
        return random.randint(-3, 3)

# Global instance
leaderboard_system = LeaderboardSystem() 