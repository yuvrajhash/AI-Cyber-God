"""
👥 TEAM MANAGER - PHASE 3
Manages team creation, collaboration, and team-based competitions
"""

import asyncio
import json
import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import random

logger = logging.getLogger(__name__)

class TeamManager:
    def __init__(self):
        self.is_active = False
        self.teams = {}
        self.team_invitations = {}
        self.team_challenges = {}
        
    async def initialize(self):
        """Initialize the team manager"""
        try:
            logger.info("👥 Initializing Team Manager...")
            
            # Generate mock teams for demonstration
            await self._generate_mock_teams()
            
            self.is_active = True
            logger.info("✅ Team Manager initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Error initializing Team Manager: {e}")
            self.is_active = False
    
    async def create_team(self, team_name: str, description: str, creator_id: str, 
                         max_members: int = 4, is_public: bool = True):
        """Create a new team"""
        # Check if team name is already taken
        for team in self.teams.values():
            if team["team_name"].lower() == team_name.lower():
                raise ValueError("Team name already exists")
        
        team_id = str(uuid.uuid4())
        
        team = {
            "team_id": team_id,
            "team_name": team_name,
            "description": description,
            "creator_id": creator_id,
            "leader_id": creator_id,
            "max_members": max_members,
            "is_public": is_public,
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "members": [
                {
                    "player_id": creator_id,
                    "username": f"Player_{creator_id[:8]}",
                    "role": "leader",
                    "joined_at": datetime.now().isoformat(),
                    "contributions": 0,
                    "status": "active"
                }
            ],
            "statistics": {
                "total_score": 0,
                "challenges_completed": 0,
                "tournaments_participated": 0,
                "tournaments_won": 0,
                "average_member_score": 0,
                "team_rank": 0
            },
            "settings": {
                "auto_accept_invites": False,
                "allow_member_invites": True,
                "challenge_sharing": True,
                "score_sharing": True
            }
        }
        
        self.teams[team_id] = team
        
        logger.info(f"👥 Team created: {team_name} ({team_id}) by {creator_id}")
        
        return team
    
    async def join_team(self, team_id: str, player_id: str):
        """Join a team"""
        if team_id not in self.teams:
            raise ValueError("Team not found")
        
        team = self.teams[team_id]
        
        # Check if team is full
        if len(team["members"]) >= team["max_members"]:
            raise ValueError("Team is full")
        
        # Check if player is already a member
        for member in team["members"]:
            if member["player_id"] == player_id:
                raise ValueError("Player is already a team member")
        
        # Check if team is public or player has invitation
        if not team["is_public"]:
            invitation_key = f"{team_id}_{player_id}"
            if invitation_key not in self.team_invitations:
                raise ValueError("Team is private and no invitation found")
            
            # Remove invitation after joining
            del self.team_invitations[invitation_key]
        
        # Add player to team
        new_member = {
            "player_id": player_id,
            "username": f"Player_{player_id[:8]}",
            "role": "member",
            "joined_at": datetime.now().isoformat(),
            "contributions": 0,
            "status": "active"
        }
        
        team["members"].append(new_member)
        
        logger.info(f"👥 Player {player_id} joined team {team['team_name']}")
        
        return {
            "success": True,
            "message": f"Successfully joined team: {team['team_name']}",
            "team": team,
            "member_position": len(team["members"])
        }
    
    async def leave_team(self, team_id: str, player_id: str):
        """Leave a team"""
        if team_id not in self.teams:
            raise ValueError("Team not found")
        
        team = self.teams[team_id]
        
        # Find and remove member
        member_found = False
        for i, member in enumerate(team["members"]):
            if member["player_id"] == player_id:
                # Check if player is the leader
                if member["role"] == "leader":
                    if len(team["members"]) > 1:
                        # Transfer leadership to next member
                        team["members"][1]["role"] = "leader"
                        team["leader_id"] = team["members"][1]["player_id"]
                    else:
                        # Disband team if leader is the only member
                        team["status"] = "disbanded"
                
                team["members"].pop(i)
                member_found = True
                break
        
        if not member_found:
            raise ValueError("Player is not a member of this team")
        
        logger.info(f"👥 Player {player_id} left team {team['team_name']}")
        
        return {
            "success": True,
            "message": f"Successfully left team: {team['team_name']}",
            "team_status": team["status"]
        }
    
    async def invite_to_team(self, team_id: str, inviter_id: str, invitee_id: str):
        """Invite a player to join a team"""
        if team_id not in self.teams:
            raise ValueError("Team not found")
        
        team = self.teams[team_id]
        
        # Check if inviter has permission
        inviter_member = None
        for member in team["members"]:
            if member["player_id"] == inviter_id:
                inviter_member = member
                break
        
        if not inviter_member:
            raise ValueError("Inviter is not a team member")
        
        if inviter_member["role"] != "leader" and not team["settings"]["allow_member_invites"]:
            raise ValueError("Only team leaders can send invitations")
        
        # Check if team has space
        if len(team["members"]) >= team["max_members"]:
            raise ValueError("Team is full")
        
        # Create invitation
        invitation_key = f"{team_id}_{invitee_id}"
        invitation = {
            "invitation_id": str(uuid.uuid4()),
            "team_id": team_id,
            "team_name": team["team_name"],
            "inviter_id": inviter_id,
            "invitee_id": invitee_id,
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(days=7)).isoformat(),
            "status": "pending"
        }
        
        self.team_invitations[invitation_key] = invitation
        
        logger.info(f"👥 Invitation sent: {invitee_id} invited to {team['team_name']} by {inviter_id}")
        
        return invitation
    
    async def get_team_details(self, team_id: str):
        """Get detailed team information"""
        if team_id not in self.teams:
            raise ValueError("Team not found")
        
        team = self.teams[team_id].copy()
        
        # Add dynamic statistics
        team["statistics"]["current_rank"] = await self._calculate_team_rank(team_id)
        team["recent_activity"] = await self._get_team_recent_activity(team_id)
        team["member_performance"] = await self._get_member_performance(team_id)
        
        return team
    
    async def get_player_teams(self, player_id: str):
        """Get all teams a player is a member of"""
        player_teams = []
        
        for team in self.teams.values():
            for member in team["members"]:
                if member["player_id"] == player_id:
                    team_summary = {
                        "team_id": team["team_id"],
                        "team_name": team["team_name"],
                        "role": member["role"],
                        "member_count": len(team["members"]),
                        "team_score": team["statistics"]["total_score"],
                        "status": team["status"]
                    }
                    player_teams.append(team_summary)
                    break
        
        return player_teams
    
    async def get_public_teams(self, limit: int = 20):
        """Get list of public teams available to join"""
        public_teams = []
        
        for team in self.teams.values():
            if team["is_public"] and team["status"] == "active":
                if len(team["members"]) < team["max_members"]:
                    team_summary = {
                        "team_id": team["team_id"],
                        "team_name": team["team_name"],
                        "description": team["description"],
                        "member_count": len(team["members"]),
                        "max_members": team["max_members"],
                        "total_score": team["statistics"]["total_score"],
                        "created_at": team["created_at"],
                        "leader_username": next(
                            (m["username"] for m in team["members"] if m["role"] == "leader"),
                            "Unknown"
                        )
                    }
                    public_teams.append(team_summary)
        
        # Sort by score and member count
        public_teams.sort(key=lambda x: (x["total_score"], x["member_count"]), reverse=True)
        
        return public_teams[:limit]
    
    async def update_team_settings(self, team_id: str, player_id: str, settings: Dict):
        """Update team settings"""
        if team_id not in self.teams:
            raise ValueError("Team not found")
        
        team = self.teams[team_id]
        
        # Check if player is team leader
        is_leader = any(
            member["player_id"] == player_id and member["role"] == "leader"
            for member in team["members"]
        )
        
        if not is_leader:
            raise ValueError("Only team leaders can update settings")
        
        # Update settings
        team["settings"].update(settings)
        
        logger.info(f"👥 Team settings updated for {team['team_name']} by {player_id}")
        
        return {
            "success": True,
            "message": "Team settings updated successfully",
            "settings": team["settings"]
        }
    
    async def promote_member(self, team_id: str, promoter_id: str, member_id: str, new_role: str):
        """Promote or change member role"""
        if team_id not in self.teams:
            raise ValueError("Team not found")
        
        team = self.teams[team_id]
        
        # Check if promoter is team leader
        is_leader = any(
            member["player_id"] == promoter_id and member["role"] == "leader"
            for member in team["members"]
        )
        
        if not is_leader:
            raise ValueError("Only team leaders can promote members")
        
        # Find and update member
        member_found = False
        for member in team["members"]:
            if member["player_id"] == member_id:
                old_role = member["role"]
                member["role"] = new_role
                
                # If promoting to leader, demote current leader
                if new_role == "leader":
                    for other_member in team["members"]:
                        if other_member["player_id"] == promoter_id:
                            other_member["role"] = "member"
                    team["leader_id"] = member_id
                
                member_found = True
                logger.info(f"👥 Member {member_id} promoted from {old_role} to {new_role} in {team['team_name']}")
                break
        
        if not member_found:
            raise ValueError("Member not found in team")
        
        return {
            "success": True,
            "message": f"Member promoted to {new_role}",
            "team": team
        }
    
    async def get_team_invitations(self, player_id: str):
        """Get pending invitations for a player"""
        invitations = []
        
        for invitation in self.team_invitations.values():
            if invitation["invitee_id"] == player_id and invitation["status"] == "pending":
                # Check if invitation hasn't expired
                expires_at = datetime.fromisoformat(invitation["expires_at"])
                if datetime.now() < expires_at:
                    invitations.append(invitation)
                else:
                    invitation["status"] = "expired"
        
        return invitations
    
    async def respond_to_invitation(self, invitation_id: str, player_id: str, response: str):
        """Respond to a team invitation"""
        invitation = None
        invitation_key = None
        
        # Find invitation
        for key, inv in self.team_invitations.items():
            if inv["invitation_id"] == invitation_id and inv["invitee_id"] == player_id:
                invitation = inv
                invitation_key = key
                break
        
        if not invitation:
            raise ValueError("Invitation not found")
        
        if invitation["status"] != "pending":
            raise ValueError("Invitation is no longer pending")
        
        # Check if invitation hasn't expired
        expires_at = datetime.fromisoformat(invitation["expires_at"])
        if datetime.now() >= expires_at:
            invitation["status"] = "expired"
            raise ValueError("Invitation has expired")
        
        if response.lower() == "accept":
            # Join the team
            try:
                result = await self.join_team(invitation["team_id"], player_id)
                invitation["status"] = "accepted"
                return result
            except Exception as e:
                invitation["status"] = "failed"
                raise e
        elif response.lower() == "decline":
            invitation["status"] = "declined"
            return {
                "success": True,
                "message": "Invitation declined"
            }
        else:
            raise ValueError("Invalid response. Use 'accept' or 'decline'")
    
    # Helper methods
    async def _generate_mock_teams(self):
        """Generate mock teams for demonstration"""
        mock_teams = [
            {
                "team_name": "Cyber Guardians",
                "description": "Elite cybersecurity professionals defending the Web3 ecosystem",
                "creator_id": "player_001",
                "members": ["player_001", "player_002", "player_003"],
                "score": 5000
            },
            {
                "team_name": "DeFi Defenders",
                "description": "Specialists in DeFi protocol security and exploitation",
                "creator_id": "player_004",
                "members": ["player_004", "player_005"],
                "score": 4500
            },
            {
                "team_name": "Smart Contract Sleuths",
                "description": "Expert auditors hunting for smart contract vulnerabilities",
                "creator_id": "player_006",
                "members": ["player_006", "player_007", "player_008", "player_009"],
                "score": 4200
            },
            {
                "team_name": "Flash Loan Fighters",
                "description": "Masters of flash loan attacks and MEV extraction",
                "creator_id": "player_010",
                "members": ["player_010"],
                "score": 3800
            }
        ]
        
        for i, mock_team in enumerate(mock_teams):
            team_id = f"team_{str(i+1).zfill(3)}"
            
            members = []
            for j, member_id in enumerate(mock_team["members"]):
                members.append({
                    "player_id": member_id,
                    "username": f"Player_{member_id[-3:]}",
                    "role": "leader" if j == 0 else "member",
                    "joined_at": (datetime.now() - timedelta(days=random.randint(1, 60))).isoformat(),
                    "contributions": random.randint(100, 1000),
                    "status": "active"
                })
            
            team = {
                "team_id": team_id,
                "team_name": mock_team["team_name"],
                "description": mock_team["description"],
                "creator_id": mock_team["creator_id"],
                "leader_id": mock_team["creator_id"],
                "max_members": 6,
                "is_public": True,
                "status": "active",
                "created_at": (datetime.now() - timedelta(days=random.randint(1, 90))).isoformat(),
                "members": members,
                "statistics": {
                    "total_score": mock_team["score"],
                    "challenges_completed": random.randint(10, 30),
                    "tournaments_participated": random.randint(1, 5),
                    "tournaments_won": random.randint(0, 2),
                    "average_member_score": mock_team["score"] // len(members),
                    "team_rank": i + 1
                },
                "settings": {
                    "auto_accept_invites": False,
                    "allow_member_invites": True,
                    "challenge_sharing": True,
                    "score_sharing": True
                }
            }
            
            self.teams[team_id] = team
    
    async def _calculate_team_rank(self, team_id: str):
        """Calculate team's current rank"""
        if team_id not in self.teams:
            return None
        
        # Sort teams by score
        sorted_teams = sorted(
            self.teams.values(),
            key=lambda x: x["statistics"]["total_score"],
            reverse=True
        )
        
        for i, team in enumerate(sorted_teams):
            if team["team_id"] == team_id:
                return i + 1
        
        return len(sorted_teams) + 1
    
    async def _get_team_recent_activity(self, team_id: str):
        """Get recent team activity"""
        # Mock recent activity
        activities = [
            {
                "type": "challenge_completed",
                "description": "Team completed 'Smart Contract Reentrancy Hunt'",
                "timestamp": datetime.now().isoformat(),
                "points": 250,
                "member": "CyberNinja"
            },
            {
                "type": "member_joined",
                "description": "New member joined the team",
                "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
                "member": "EthHacker"
            },
            {
                "type": "tournament_participation",
                "description": "Team registered for 'Cyber Defense Championship'",
                "timestamp": (datetime.now() - timedelta(days=1)).isoformat()
            }
        ]
        
        return activities[:5]  # Return last 5 activities
    
    async def _get_member_performance(self, team_id: str):
        """Get performance statistics for team members"""
        if team_id not in self.teams:
            return []
        
        team = self.teams[team_id]
        performance = []
        
        for member in team["members"]:
            performance.append({
                "player_id": member["player_id"],
                "username": member["username"],
                "role": member["role"],
                "contributions": member["contributions"],
                "individual_score": random.randint(500, 2000),
                "challenges_completed": random.randint(3, 15),
                "average_completion_time": random.randint(1200, 3600),
                "specialties": random.sample(
                    ["smart_contract_audit", "defi_exploit", "governance_attack", "mev_extraction"],
                    random.randint(1, 3)
                )
            })
        
        return performance

# Global instance
team_manager = TeamManager() 