"""
🎯 CHALLENGE MANAGER - PHASE 3
Manages cybersecurity challenges, difficulty progression, and challenge distribution
"""

import asyncio
import json
import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import random

logger = logging.getLogger(__name__)

class ChallengeManager:
    def __init__(self):
        self.is_loaded = False
        self.challenges = {}
        self.challenge_categories = {}
        self.difficulty_progression = {}
        
    async def load_challenges(self):
        """Load challenges from storage"""
        try:
            logger.info("🎯 Loading Challenge Manager...")
            
            # Generate comprehensive challenge database
            self.challenges = self._generate_challenge_database()
            self.challenge_categories = self._organize_by_categories()
            self.difficulty_progression = self._setup_difficulty_progression()
            
            self.is_loaded = True
            logger.info(f"✅ Challenge Manager loaded with {len(self.challenges)} challenges")
            
        except Exception as e:
            logger.error(f"❌ Error loading challenges: {e}")
            self.is_loaded = False
    
    async def get_challenges(self, difficulty: Optional[str] = None, 
                           challenge_type: Optional[str] = None, 
                           limit: int = 20):
        """Get challenges based on filters"""
        filtered_challenges = []
        
        for challenge in self.challenges.values():
            # Apply filters
            if difficulty and challenge["difficulty"] != difficulty:
                continue
            if challenge_type and challenge["type"] != challenge_type:
                continue
            
            filtered_challenges.append(challenge)
        
        # Sort by difficulty and creation date
        filtered_challenges.sort(key=lambda x: (
            self._get_difficulty_order(x["difficulty"]), 
            x["created_at"]
        ))
        
        return filtered_challenges[:limit]
    
    async def get_challenge_details(self, challenge_id: str):
        """Get detailed information about a specific challenge"""
        if challenge_id not in self.challenges:
            raise ValueError("Challenge not found")
        
        challenge = self.challenges[challenge_id].copy()
        
        # Add dynamic information
        challenge["statistics"] = await self._get_challenge_statistics(challenge_id)
        challenge["hints"] = await self._get_challenge_hints(challenge_id)
        challenge["leaderboard"] = await self._get_challenge_leaderboard(challenge_id)
        
        return challenge
    
    async def get_challenges_for_level(self, skill_level: str):
        """Get recommended challenges for a skill level"""
        recommended = []
        
        # Define challenge recommendations based on skill level
        level_mapping = {
            "beginner": ["beginner", "intermediate"],
            "intermediate": ["intermediate", "advanced"],
            "advanced": ["advanced", "expert"],
            "expert": ["expert", "legendary"],
            "legendary": ["legendary"]
        }
        
        target_difficulties = level_mapping.get(skill_level, ["beginner"])
        
        for difficulty in target_difficulties:
            challenges = await self.get_challenges(difficulty=difficulty, limit=10)
            recommended.extend(challenges)
        
        return recommended[:15]  # Return top 15 recommendations
    
    async def get_active_challenges_count(self):
        """Get count of active challenges"""
        return len([c for c in self.challenges.values() if c.get("status", "active") == "active"])
    
    async def create_custom_challenge(self, creator_id: str, challenge_data: Dict):
        """Create a custom challenge"""
        challenge_id = str(uuid.uuid4())
        
        challenge = {
            "id": challenge_id,
            "title": challenge_data["title"],
            "description": challenge_data["description"],
            "type": challenge_data["type"],
            "difficulty": challenge_data["difficulty"],
            "points": challenge_data.get("points", self._calculate_points(challenge_data["difficulty"])),
            "time_limit": challenge_data.get("time_limit", 3600),
            "tags": challenge_data.get("tags", []),
            "creator_id": creator_id,
            "status": "pending_review",
            "created_at": datetime.now().isoformat(),
            "test_cases": challenge_data.get("test_cases", []),
            "solution_template": challenge_data.get("solution_template", ""),
            "resources": challenge_data.get("resources", [])
        }
        
        self.challenges[challenge_id] = challenge
        
        logger.info(f"🎯 Custom challenge created: {challenge['title']} by {creator_id}")
        
        return challenge
    
    async def get_challenge_statistics(self, challenge_id: str):
        """Get statistics for a challenge"""
        return await self._get_challenge_statistics(challenge_id)
    
    async def get_trending_challenges(self, limit: int = 10):
        """Get trending challenges based on recent activity"""
        # Mock implementation - in production, this would analyze recent completions
        trending = list(self.challenges.values())
        random.shuffle(trending)
        
        for challenge in trending[:limit]:
            challenge["trend_score"] = random.uniform(0.7, 1.0)
            challenge["recent_completions"] = random.randint(5, 50)
        
        return sorted(trending[:limit], key=lambda x: x["trend_score"], reverse=True)
    
    async def get_challenge_hints(self, challenge_id: str, player_id: str):
        """Get hints for a challenge"""
        if challenge_id not in self.challenges:
            raise ValueError("Challenge not found")
        
        hints = await self._get_challenge_hints(challenge_id)
        
        # Return progressive hints based on player's attempts
        return {
            "challenge_id": challenge_id,
            "available_hints": len(hints),
            "hints": hints[:3],  # First 3 hints
            "hint_cost": 10,  # Points deducted per hint
            "player_id": player_id
        }
    
    async def submit_challenge_rating(self, challenge_id: str, player_id: str, rating: int, feedback: str):
        """Submit a rating and feedback for a challenge"""
        if challenge_id not in self.challenges:
            raise ValueError("Challenge not found")
        
        # In production, this would store in database
        rating_data = {
            "challenge_id": challenge_id,
            "player_id": player_id,
            "rating": rating,
            "feedback": feedback,
            "submitted_at": datetime.now().isoformat()
        }
        
        logger.info(f"⭐ Challenge rating submitted: {challenge_id} rated {rating}/5 by {player_id}")
        
        return {
            "success": True,
            "message": "Rating submitted successfully",
            "rating": rating_data
        }
    
    # Helper methods
    def _generate_challenge_database(self):
        """Generate comprehensive challenge database"""
        challenges = {}
        
        # Smart Contract Auditing Challenges
        sc_challenges = [
            {
                "id": "sc_audit_001",
                "title": "Reentrancy Vulnerability Hunt",
                "description": "Identify and exploit the reentrancy vulnerability in this DeFi lending protocol. The contract allows users to deposit ETH and borrow tokens, but contains a critical flaw.",
                "type": "smart_contract_audit",
                "difficulty": "intermediate",
                "points": 250,
                "time_limit": 3600,
                "tags": ["reentrancy", "defi", "solidity", "lending"],
                "created_at": datetime.now().isoformat(),
                "contract_code": "// Vulnerable lending contract code here",
                "objective": "Find the reentrancy vulnerability and write an exploit",
                "learning_objectives": ["Understanding reentrancy attacks", "Solidity security patterns", "DeFi protocol analysis"]
            },
            {
                "id": "sc_audit_002", 
                "title": "Integer Overflow Exploitation",
                "description": "This token contract has an integer overflow vulnerability. Find it and demonstrate how it can be exploited to mint unlimited tokens.",
                "type": "smart_contract_audit",
                "difficulty": "beginner",
                "points": 150,
                "time_limit": 2400,
                "tags": ["overflow", "tokens", "arithmetic"],
                "created_at": datetime.now().isoformat(),
                "contract_code": "// Token contract with overflow vulnerability",
                "objective": "Exploit integer overflow to mint tokens",
                "learning_objectives": ["Integer overflow/underflow", "SafeMath usage", "Token security"]
            },
            {
                "id": "sc_audit_003",
                "title": "Access Control Bypass",
                "description": "This governance contract has flawed access controls. Find a way to execute admin functions without proper authorization.",
                "type": "smart_contract_audit", 
                "difficulty": "advanced",
                "points": 400,
                "time_limit": 5400,
                "tags": ["access_control", "governance", "authorization"],
                "created_at": datetime.now().isoformat(),
                "contract_code": "// Governance contract with access control flaws",
                "objective": "Bypass access controls to execute admin functions",
                "learning_objectives": ["Access control patterns", "Role-based permissions", "Governance security"]
            }
        ]
        
        # DeFi Exploitation Challenges
        defi_challenges = [
            {
                "id": "defi_exploit_001",
                "title": "Flash Loan Arbitrage Attack",
                "description": "Execute a profitable flash loan attack across multiple DEXs. Identify price discrepancies and exploit them for profit.",
                "type": "defi_exploit",
                "difficulty": "advanced",
                "points": 500,
                "time_limit": 7200,
                "tags": ["flash_loan", "arbitrage", "dex", "amm"],
                "created_at": datetime.now().isoformat(),
                "scenario": "Multiple DEXs with price discrepancies",
                "objective": "Execute profitable flash loan arbitrage",
                "learning_objectives": ["Flash loan mechanics", "DEX arbitrage", "MEV extraction"]
            },
            {
                "id": "defi_exploit_002",
                "title": "Liquidity Pool Manipulation",
                "description": "Manipulate the price oracle by exploiting low liquidity pools. Demonstrate how this can affect dependent protocols.",
                "type": "defi_exploit",
                "difficulty": "expert",
                "points": 750,
                "time_limit": 9000,
                "tags": ["oracle", "manipulation", "liquidity", "price"],
                "created_at": datetime.now().isoformat(),
                "scenario": "Low liquidity AMM pools with oracle dependencies",
                "objective": "Manipulate oracle prices through liquidity attacks",
                "learning_objectives": ["Oracle manipulation", "Liquidity attacks", "Price impact"]
            }
        ]
        
        # Governance Attack Challenges
        governance_challenges = [
            {
                "id": "governance_001",
                "title": "DAO Governance Takeover",
                "description": "Execute a governance attack to pass a malicious proposal. Use flash loans to temporarily acquire voting power.",
                "type": "governance_attack",
                "difficulty": "expert",
                "points": 800,
                "time_limit": 10800,
                "tags": ["dao", "governance", "voting", "flash_loan"],
                "created_at": datetime.now().isoformat(),
                "scenario": "DAO with token-based voting and flash loan vulnerability",
                "objective": "Pass malicious proposal using flash loan governance attack",
                "learning_objectives": ["Governance attacks", "Flash loan voting", "DAO security"]
            }
        ]
        
        # Bridge Exploitation Challenges
        bridge_challenges = [
            {
                "id": "bridge_exploit_001",
                "title": "Cross-Chain Bridge Hack",
                "description": "Find and exploit vulnerabilities in this cross-chain bridge to drain funds from the bridge contract.",
                "type": "bridge_exploit",
                "difficulty": "legendary",
                "points": 1000,
                "time_limit": 14400,
                "tags": ["bridge", "cross_chain", "validation", "merkle"],
                "created_at": datetime.now().isoformat(),
                "scenario": "Cross-chain bridge with validation flaws",
                "objective": "Exploit bridge to drain funds",
                "learning_objectives": ["Bridge security", "Cross-chain validation", "Merkle proof attacks"]
            }
        ]
        
        # MEV Extraction Challenges
        mev_challenges = [
            {
                "id": "mev_extraction_001",
                "title": "Sandwich Attack Optimization",
                "description": "Optimize a sandwich attack strategy to maximize MEV extraction from large trades on Uniswap.",
                "type": "mev_extraction",
                "difficulty": "advanced",
                "points": 600,
                "time_limit": 6000,
                "tags": ["mev", "sandwich", "frontrun", "uniswap"],
                "created_at": datetime.now().isoformat(),
                "scenario": "Large pending trades on Uniswap V3",
                "objective": "Maximize MEV through optimized sandwich attacks",
                "learning_objectives": ["MEV strategies", "Sandwich attacks", "Gas optimization"]
            }
        ]
        
        # Oracle Manipulation Challenges
        oracle_challenges = [
            {
                "id": "oracle_manipulation_001",
                "title": "Chainlink Oracle Manipulation",
                "description": "Exploit a misconfigured Chainlink oracle setup to manipulate price feeds and profit from dependent protocols.",
                "type": "oracle_manipulation",
                "difficulty": "expert",
                "points": 700,
                "time_limit": 8400,
                "tags": ["oracle", "chainlink", "price_feed", "manipulation"],
                "created_at": datetime.now().isoformat(),
                "scenario": "Misconfigured Chainlink oracle with single source",
                "objective": "Manipulate oracle to profit from dependent protocols",
                "learning_objectives": ["Oracle security", "Price feed manipulation", "Oracle dependencies"]
            }
        ]
        
        # Combine all challenges
        all_challenges = (sc_challenges + defi_challenges + governance_challenges + 
                         bridge_challenges + mev_challenges + oracle_challenges)
        
        for challenge in all_challenges:
            challenges[challenge["id"]] = challenge
        
        return challenges
    
    def _organize_by_categories(self):
        """Organize challenges by categories"""
        categories = {}
        
        for challenge in self.challenges.values():
            category = challenge["type"]
            if category not in categories:
                categories[category] = []
            categories[category].append(challenge["id"])
        
        return categories
    
    def _setup_difficulty_progression(self):
        """Setup difficulty progression system"""
        return {
            "beginner": {"min_score": 0, "max_score": 500, "unlock_next": 300},
            "intermediate": {"min_score": 300, "max_score": 1500, "unlock_next": 1000},
            "advanced": {"min_score": 1000, "max_score": 5000, "unlock_next": 3000},
            "expert": {"min_score": 3000, "max_score": 15000, "unlock_next": 10000},
            "legendary": {"min_score": 10000, "max_score": float('inf'), "unlock_next": float('inf')}
        }
    
    def _get_difficulty_order(self, difficulty: str):
        """Get numeric order for difficulty sorting"""
        order = {
            "beginner": 1,
            "intermediate": 2,
            "advanced": 3,
            "expert": 4,
            "legendary": 5
        }
        return order.get(difficulty, 0)
    
    def _calculate_points(self, difficulty: str):
        """Calculate points based on difficulty"""
        points_map = {
            "beginner": 100,
            "intermediate": 250,
            "advanced": 500,
            "expert": 750,
            "legendary": 1000
        }
        return points_map.get(difficulty, 100)
    
    async def _get_challenge_statistics(self, challenge_id: str):
        """Get statistics for a challenge"""
        # Mock statistics - in production, this would query actual data
        return {
            "total_attempts": random.randint(50, 500),
            "successful_completions": random.randint(10, 100),
            "average_completion_time": random.randint(1200, 7200),
            "success_rate": random.uniform(0.15, 0.85),
            "average_rating": random.uniform(3.5, 4.8),
            "difficulty_rating": random.uniform(0.6, 0.95),
            "last_completed": datetime.now().isoformat()
        }
    
    async def _get_challenge_hints(self, challenge_id: str):
        """Get hints for a challenge"""
        # Mock hints - in production, these would be stored per challenge
        generic_hints = [
            "Look for functions that make external calls before updating state",
            "Check if the contract uses proper access modifiers",
            "Examine the order of operations in critical functions",
            "Consider how the contract handles edge cases",
            "Look for potential integer overflow/underflow vulnerabilities"
        ]
        
        return generic_hints[:3]  # Return first 3 hints
    
    async def _get_challenge_leaderboard(self, challenge_id: str):
        """Get leaderboard for a challenge"""
        # Mock leaderboard - in production, this would query actual completions
        mock_players = ["CyberNinja", "EthHacker", "DeFiExplorer", "SmartContractAuditor", "MEVBot"]
        
        leaderboard = []
        for i, player in enumerate(mock_players):
            leaderboard.append({
                "rank": i + 1,
                "username": player,
                "completion_time": random.randint(900, 3600),
                "score": random.randint(200, 1000),
                "completed_at": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat()
            })
        
        return leaderboard

# Global instance
challenge_manager = ChallengeManager() 