"""
Reinforcement Learning Cyber Defense Agent
Advanced RL agent for automated threat response and defense strategy optimization
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from collections import deque, namedtuple
import random
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
import logging

logger = logging.getLogger(__name__)

# Experience tuple for replay buffer
Experience = namedtuple('Experience', ['state', 'action', 'reward', 'next_state', 'done'])

class DQNNetwork(nn.Module):
    """
    Deep Q-Network for cyber defense action selection
    """
    def __init__(self, state_dim: int, action_dim: int, hidden_dims: List[int] = [512, 256, 128]):
        super(DQNNetwork, self).__init__()
        
        layers = []
        input_dim = state_dim
        
        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(input_dim, hidden_dim),
                nn.ReLU(),
                nn.Dropout(0.3)
            ])
            input_dim = hidden_dim
        
        # Output layer for Q-values
        layers.append(nn.Linear(input_dim, action_dim))
        
        self.network = nn.Sequential(*layers)
        
        # Dueling DQN architecture
        self.value_head = nn.Sequential(
            nn.Linear(hidden_dims[-1], 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )
        
        self.advantage_head = nn.Sequential(
            nn.Linear(hidden_dims[-1], 64),
            nn.ReLU(),
            nn.Linear(64, action_dim)
        )
        
    def forward(self, x):
        # Extract features
        features = x
        for i, layer in enumerate(self.network[:-1]):
            features = layer(features)
            if i == len(self.network) - 4:  # Before last linear layer
                shared_features = features
        
        # Dueling architecture
        value = self.value_head(shared_features)
        advantage = self.advantage_head(shared_features)
        
        # Combine value and advantage
        q_values = value + (advantage - advantage.mean(dim=1, keepdim=True))
        
        return q_values

class PolicyNetwork(nn.Module):
    """
    Policy network for continuous action spaces
    """
    def __init__(self, state_dim: int, action_dim: int, hidden_dims: List[int] = [256, 128]):
        super(PolicyNetwork, self).__init__()
        
        layers = []
        input_dim = state_dim
        
        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(input_dim, hidden_dim),
                nn.ReLU(),
                nn.Dropout(0.2)
            ])
            input_dim = hidden_dim
        
        self.shared_layers = nn.Sequential(*layers)
        
        # Mean and std for Gaussian policy
        self.mean_head = nn.Linear(input_dim, action_dim)
        self.log_std_head = nn.Linear(input_dim, action_dim)
        
    def forward(self, x):
        shared = self.shared_layers(x)
        mean = torch.tanh(self.mean_head(shared))  # Bounded actions
        log_std = torch.clamp(self.log_std_head(shared), -20, 2)
        
        return mean, log_std
    
    def sample_action(self, state):
        mean, log_std = self.forward(state)
        std = torch.exp(log_std)
        
        # Sample from Gaussian distribution
        normal = torch.distributions.Normal(mean, std)
        action = normal.sample()
        log_prob = normal.log_prob(action).sum(dim=-1)
        
        return action, log_prob

class CyberEnvironment:
    """
    Simulated cyber security environment for RL training
    """
    
    def __init__(self):
        # State space: [threat_level, system_health, active_defenses, resource_usage, time_of_day, ...]
        self.state_dim = 20
        
        # Action space: [firewall_level, monitoring_intensity, patch_priority, isolation_level, ...]
        self.action_dim = 8
        
        # Environment state
        self.current_state = None
        self.step_count = 0
        self.max_steps = 1000
        
        # Threat simulation parameters
        self.threat_intensity = 0.5
        self.system_health = 1.0
        self.defense_effectiveness = 0.8
        
        self.reset()
    
    def reset(self) -> np.ndarray:
        """Reset environment to initial state"""
        self.step_count = 0
        self.threat_intensity = np.random.uniform(0.3, 0.7)
        self.system_health = 1.0
        self.defense_effectiveness = 0.8
        
        self.current_state = self._generate_state()
        return self.current_state
    
    def step(self, action: np.ndarray) -> Tuple[np.ndarray, float, bool, Dict]:
        """Execute action and return next state, reward, done, info"""
        self.step_count += 1
        
        # Normalize action to [0, 1] range
        action = np.clip(action, -1, 1)
        action = (action + 1) / 2
        
        # Apply action effects
        self._apply_action(action)
        
        # Simulate threat evolution
        self._simulate_threats()
        
        # Calculate reward
        reward = self._calculate_reward(action)
        
        # Update state
        self.current_state = self._generate_state()
        
        # Check if episode is done
        done = (self.step_count >= self.max_steps or 
                self.system_health <= 0.1 or 
                self.threat_intensity >= 0.95)
        
        info = {
            'threat_intensity': self.threat_intensity,
            'system_health': self.system_health,
            'defense_effectiveness': self.defense_effectiveness,
            'step_count': self.step_count
        }
        
        return self.current_state, reward, done, info
    
    def _generate_state(self) -> np.ndarray:
        """Generate current state vector"""
        # Time-based features
        hour = (datetime.now().hour / 24.0)
        day_of_week = (datetime.now().weekday() / 7.0)
        
        state = np.array([
            self.threat_intensity,
            self.system_health,
            self.defense_effectiveness,
            np.random.uniform(0.4, 0.9),  # CPU usage
            np.random.uniform(0.3, 0.8),  # Memory usage
            np.random.uniform(0.2, 0.7),  # Network usage
            hour,
            day_of_week,
            np.random.uniform(0, 1),  # Active connections
            np.random.uniform(0, 1),  # Firewall status
            np.random.uniform(0, 1),  # IDS alerts
            np.random.uniform(0, 1),  # Patch level
            np.random.uniform(0, 1),  # Backup status
            np.random.uniform(0, 1),  # Monitoring coverage
            np.random.uniform(0, 1),  # Incident response readiness
            np.random.uniform(0, 1),  # User activity
            np.random.uniform(0, 1),  # External threat intel
            np.random.uniform(0, 1),  # Vulnerability score
            np.random.uniform(0, 1),  # Compliance status
            np.random.uniform(0, 1)   # Security training level
        ])
        
        return state.astype(np.float32)
    
    def _apply_action(self, action: np.ndarray):
        """Apply defense actions to the environment"""
        # Action components:
        # 0: Firewall strictness
        # 1: Monitoring intensity
        # 2: Patch deployment speed
        # 3: Network isolation level
        # 4: Incident response activation
        # 5: User access restrictions
        # 6: Backup frequency
        # 7: Threat hunting intensity
        
        firewall_level = action[0]
        monitoring_intensity = action[1]
        patch_speed = action[2]
        isolation_level = action[3]
        
        # Update defense effectiveness based on actions
        defense_boost = (
            firewall_level * 0.2 +
            monitoring_intensity * 0.15 +
            patch_speed * 0.25 +
            isolation_level * 0.1
        )
        
        self.defense_effectiveness = np.clip(
            self.defense_effectiveness + defense_boost * 0.1 - 0.02,  # Natural decay
            0.0, 1.0
        )
    
    def _simulate_threats(self):
        """Simulate threat evolution and system impact"""
        # Random threat events
        if np.random.random() < 0.1:  # 10% chance of new threat
            self.threat_intensity += np.random.uniform(0.1, 0.3)
        
        # Threat mitigation by defenses
        mitigation = self.defense_effectiveness * 0.1
        self.threat_intensity = np.clip(
            self.threat_intensity - mitigation + np.random.normal(0, 0.02),
            0.0, 1.0
        )
        
        # System health impact
        damage = self.threat_intensity * (1 - self.defense_effectiveness) * 0.05
        self.system_health = np.clip(self.system_health - damage, 0.0, 1.0)
        
        # Recovery
        if self.threat_intensity < 0.3:
            self.system_health = np.clip(self.system_health + 0.01, 0.0, 1.0)
    
    def _calculate_reward(self, action: np.ndarray) -> float:
        """Calculate reward for the current state and action"""
        # Reward components
        
        # 1. System health reward (most important)
        health_reward = self.system_health * 10
        
        # 2. Threat mitigation reward
        threat_penalty = -self.threat_intensity * 5
        
        # 3. Defense effectiveness reward
        defense_reward = self.defense_effectiveness * 3
        
        # 4. Action efficiency penalty (avoid overreacting)
        action_penalty = -np.sum(action ** 2) * 0.5
        
        # 5. Stability bonus (reward consistent performance)
        stability_bonus = 2 if self.system_health > 0.8 and self.threat_intensity < 0.4 else 0
        
        # 6. Critical state penalty
        critical_penalty = -20 if self.system_health < 0.3 or self.threat_intensity > 0.8 else 0
        
        total_reward = (health_reward + threat_penalty + defense_reward + 
                       action_penalty + stability_bonus + critical_penalty)
        
        return float(total_reward)

class ReplayBuffer:
    """Experience replay buffer for DQN training"""
    
    def __init__(self, capacity: int = 100000):
        self.buffer = deque(maxlen=capacity)
    
    def push(self, state, action, reward, next_state, done):
        """Add experience to buffer"""
        experience = Experience(state, action, reward, next_state, done)
        self.buffer.append(experience)
    
    def sample(self, batch_size: int) -> List[Experience]:
        """Sample batch of experiences"""
        return random.sample(self.buffer, batch_size)
    
    def __len__(self):
        return len(self.buffer)

class CyberDefenseAgent:
    """
    Complete reinforcement learning agent for cyber defense
    """
    
    def __init__(self, state_dim: int = 20, action_dim: int = 8, model_path: str = "models/rl_agent.pth"):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.model_path = model_path
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Networks
        self.q_network = DQNNetwork(state_dim, action_dim).to(self.device)
        self.target_network = DQNNetwork(state_dim, action_dim).to(self.device)
        self.policy_network = PolicyNetwork(state_dim, action_dim).to(self.device)
        
        # Training parameters
        self.learning_rate = 0.001
        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.target_update_freq = 100
        self.batch_size = 64
        
        # Optimizers
        self.q_optimizer = torch.optim.Adam(self.q_network.parameters(), lr=self.learning_rate)
        self.policy_optimizer = torch.optim.Adam(self.policy_network.parameters(), lr=self.learning_rate)
        
        # Experience replay
        self.replay_buffer = ReplayBuffer(100000)
        
        # Training state
        self.is_trained = False
        self.training_step = 0
        
        # Environment
        self.env = CyberEnvironment()
        
        # Performance tracking
        self.episode_rewards = []
        self.episode_lengths = []
        
        logger.info(f"Initialized CyberDefenseAgent on device: {self.device}")
    
    def select_action(self, state: np.ndarray, training: bool = False) -> np.ndarray:
        """Select action using epsilon-greedy policy or trained policy"""
        state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        
        if training and np.random.random() < self.epsilon:
            # Random action for exploration
            return np.random.uniform(-1, 1, self.action_dim)
        
        if self.is_trained:
            # Use policy network for continuous actions
            self.policy_network.eval()
            with torch.no_grad():
                action, _ = self.policy_network.sample_action(state_tensor)
                return action.cpu().numpy()[0]
        else:
            # Use Q-network for discrete actions (converted to continuous)
            self.q_network.eval()
            with torch.no_grad():
                q_values = self.q_network(state_tensor)
                action_idx = q_values.argmax().item()
                
                # Convert discrete action to continuous
                action = np.zeros(self.action_dim)
                action[action_idx % self.action_dim] = 1.0
                return action
    
    def train_dqn(self, episodes: int = 1000):
        """Train the DQN agent"""
        logger.info(f"Starting DQN training for {episodes} episodes...")
        
        for episode in range(episodes):
            state = self.env.reset()
            episode_reward = 0
            episode_length = 0
            
            while True:
                # Select action
                action = self.select_action(state, training=True)
                
                # Take step in environment
                next_state, reward, done, info = self.env.step(action)
                
                # Store experience
                self.replay_buffer.push(state, action, reward, next_state, done)
                
                episode_reward += reward
                episode_length += 1
                state = next_state
                
                # Train if enough experiences
                if len(self.replay_buffer) > self.batch_size:
                    self._train_step()
                
                if done:
                    break
            
            # Update target network
            if episode % self.target_update_freq == 0:
                self.target_network.load_state_dict(self.q_network.state_dict())
            
            # Decay epsilon
            self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
            
            # Track performance
            self.episode_rewards.append(episode_reward)
            self.episode_lengths.append(episode_length)
            
            if episode % 100 == 0:
                avg_reward = np.mean(self.episode_rewards[-100:])
                logger.info(f"Episode {episode}, Avg Reward: {avg_reward:.2f}, Epsilon: {self.epsilon:.3f}")
        
        self.is_trained = True
        self.save_model()
        logger.info("DQN training completed!")
    
    def train_policy(self, episodes: int = 500):
        """Train the policy network using policy gradients"""
        logger.info(f"Starting policy gradient training for {episodes} episodes...")
        
        for episode in range(episodes):
            state = self.env.reset()
            episode_rewards = []
            episode_log_probs = []
            
            while True:
                state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
                
                # Sample action from policy
                action, log_prob = self.policy_network.sample_action(state_tensor)
                action_np = action.cpu().numpy()[0]
                
                # Take step
                next_state, reward, done, info = self.env.step(action_np)
                
                episode_rewards.append(reward)
                episode_log_probs.append(log_prob)
                
                state = next_state
                
                if done:
                    break
            
            # Calculate returns
            returns = []
            G = 0
            for reward in reversed(episode_rewards):
                G = reward + self.gamma * G
                returns.insert(0, G)
            
            returns = torch.FloatTensor(returns).to(self.device)
            returns = (returns - returns.mean()) / (returns.std() + 1e-8)  # Normalize
            
            # Policy gradient update
            policy_loss = 0
            for log_prob, G in zip(episode_log_probs, returns):
                policy_loss += -log_prob * G
            
            self.policy_optimizer.zero_grad()
            policy_loss.backward()
            self.policy_optimizer.step()
            
            if episode % 50 == 0:
                avg_reward = np.mean(episode_rewards)
                logger.info(f"Policy Episode {episode}, Avg Reward: {avg_reward:.2f}")
        
        logger.info("Policy gradient training completed!")
    
    def _train_step(self):
        """Single training step for DQN"""
        if len(self.replay_buffer) < self.batch_size:
            return
        
        # Sample batch
        experiences = self.replay_buffer.sample(self.batch_size)
        batch = Experience(*zip(*experiences))
        
        # Convert to tensors
        state_batch = torch.FloatTensor(batch.state).to(self.device)
        action_batch = torch.LongTensor([np.argmax(a) for a in batch.action]).to(self.device)
        reward_batch = torch.FloatTensor(batch.reward).to(self.device)
        next_state_batch = torch.FloatTensor(batch.next_state).to(self.device)
        done_batch = torch.BoolTensor(batch.done).to(self.device)
        
        # Current Q values
        current_q_values = self.q_network(state_batch).gather(1, action_batch.unsqueeze(1))
        
        # Next Q values from target network
        next_q_values = self.target_network(next_state_batch).max(1)[0].detach()
        target_q_values = reward_batch + (self.gamma * next_q_values * ~done_batch)
        
        # Compute loss
        loss = F.mse_loss(current_q_values.squeeze(), target_q_values)
        
        # Optimize
        self.q_optimizer.zero_grad()
        loss.backward()
        self.q_optimizer.step()
        
        self.training_step += 1
    
    def get_defense_recommendation(self, threat_state: Dict) -> Dict:
        """Get defense recommendations based on current threat state"""
        # Convert threat state to environment state
        state = self._threat_state_to_env_state(threat_state)
        
        # Get action from trained agent
        action = self.select_action(state)
        
        # Convert action to human-readable recommendations
        recommendations = self._action_to_recommendations(action)
        
        # Calculate confidence based on Q-values
        state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        
        if self.is_trained:
            self.q_network.eval()
            with torch.no_grad():
                q_values = self.q_network(state_tensor)
                confidence = torch.softmax(q_values, dim=1).max().item()
        else:
            confidence = 0.6  # Default confidence
        
        return {
            'recommendations': recommendations,
            'confidence': float(confidence),
            'action_values': action.tolist(),
            'threat_assessment': self._assess_threat_level(state),
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _threat_state_to_env_state(self, threat_state: Dict) -> np.ndarray:
        """Convert threat intelligence to environment state"""
        # Extract relevant features from threat state
        threat_count = threat_state.get('active_threats', 10)
        avg_severity = threat_state.get('avg_severity', 0.5)
        system_health = threat_state.get('system_health', 0.8)
        
        # Normalize threat count
        threat_intensity = min(threat_count / 50.0, 1.0)
        
        # Create state vector
        state = np.array([
            threat_intensity,
            system_health,
            0.8,  # defense_effectiveness (default)
            np.random.uniform(0.4, 0.9),  # CPU usage
            np.random.uniform(0.3, 0.8),  # Memory usage
            np.random.uniform(0.2, 0.7),  # Network usage
            datetime.now().hour / 24.0,   # Hour
            datetime.now().weekday() / 7.0,  # Day of week
            # Fill remaining with defaults or extract from threat_state
            *np.random.uniform(0, 1, 12)
        ])
        
        return state.astype(np.float32)
    
    def _action_to_recommendations(self, action: np.ndarray) -> List[Dict]:
        """Convert action vector to human-readable recommendations"""
        action_names = [
            'Firewall Configuration',
            'Monitoring Intensity',
            'Patch Deployment',
            'Network Isolation',
            'Incident Response',
            'Access Control',
            'Backup Operations',
            'Threat Hunting'
        ]
        
        recommendations = []
        
        for i, (name, value) in enumerate(zip(action_names, action)):
            # Convert to 0-1 range
            normalized_value = (value + 1) / 2
            
            if normalized_value > 0.7:
                priority = 'high'
                action_desc = f"Increase {name.lower()} to maximum level"
            elif normalized_value > 0.4:
                priority = 'medium'
                action_desc = f"Moderate adjustment to {name.lower()}"
            else:
                priority = 'low'
                action_desc = f"Minimal changes to {name.lower()}"
            
            recommendations.append({
                'action': name,
                'priority': priority,
                'description': action_desc,
                'value': float(normalized_value)
            })
        
        return recommendations
    
    def _assess_threat_level(self, state: np.ndarray) -> str:
        """Assess overall threat level from state"""
        threat_intensity = state[0]
        system_health = state[1]
        
        if threat_intensity > 0.8 or system_health < 0.3:
            return 'critical'
        elif threat_intensity > 0.6 or system_health < 0.5:
            return 'high'
        elif threat_intensity > 0.4 or system_health < 0.7:
            return 'medium'
        else:
            return 'low'
    
    def save_model(self):
        """Save the trained models"""
        import os
        os.makedirs("models", exist_ok=True)
        
        torch.save({
            'q_network_state_dict': self.q_network.state_dict(),
            'target_network_state_dict': self.target_network.state_dict(),
            'policy_network_state_dict': self.policy_network.state_dict(),
            'q_optimizer_state_dict': self.q_optimizer.state_dict(),
            'policy_optimizer_state_dict': self.policy_optimizer.state_dict(),
            'epsilon': self.epsilon,
            'training_step': self.training_step,
            'is_trained': self.is_trained,
            'episode_rewards': self.episode_rewards,
            'episode_lengths': self.episode_lengths
        }, self.model_path)
        
        logger.info(f"RL agent models saved to {self.model_path}")
    
    def load_model(self):
        """Load pre-trained models"""
        try:
            checkpoint = torch.load(self.model_path, map_location=self.device)
            
            self.q_network.load_state_dict(checkpoint['q_network_state_dict'])
            self.target_network.load_state_dict(checkpoint['target_network_state_dict'])
            self.policy_network.load_state_dict(checkpoint['policy_network_state_dict'])
            self.q_optimizer.load_state_dict(checkpoint['q_optimizer_state_dict'])
            self.policy_optimizer.load_state_dict(checkpoint['policy_optimizer_state_dict'])
            
            self.epsilon = checkpoint['epsilon']
            self.training_step = checkpoint['training_step']
            self.is_trained = checkpoint['is_trained']
            self.episode_rewards = checkpoint['episode_rewards']
            self.episode_lengths = checkpoint['episode_lengths']
            
            logger.info(f"RL agent models loaded from {self.model_path}")
            
        except FileNotFoundError:
            logger.warning(f"Model file not found at {self.model_path}. Training new models...")
            self.train_dqn(500)  # Quick training
            self.train_policy(200)
        except Exception as e:
            logger.error(f"Error loading RL agent models: {e}")
    
    def get_training_stats(self) -> Dict:
        """Get training statistics"""
        if not self.episode_rewards:
            return {'status': 'not_trained'}
        
        return {
            'total_episodes': len(self.episode_rewards),
            'avg_reward': float(np.mean(self.episode_rewards[-100:])),
            'best_reward': float(np.max(self.episode_rewards)),
            'avg_episode_length': float(np.mean(self.episode_lengths[-100:])),
            'current_epsilon': float(self.epsilon),
            'training_steps': self.training_step,
            'is_trained': self.is_trained
        } 