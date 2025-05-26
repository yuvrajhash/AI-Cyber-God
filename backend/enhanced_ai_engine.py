"""
Enhanced AI Engine - Phase 1 Implementation
Integrates all advanced AI models for comprehensive cyber threat analysis
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import numpy as np
import torch

# Import our enhanced AI models
from ai_models.quantum_classifier import ThreatClassificationEngine
from ai_models.neural_analyzer import ContractAnalysisEngine
from ai_models.predictive_engine import PredictiveThreatEngine
from ai_models.reinforcement_agent import CyberDefenseAgent

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedAIEngine:
    """
    Enhanced AI Engine with real machine learning capabilities
    Combines quantum-inspired algorithms, neural networks, and reinforcement learning
    """
    
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logger.info(f"Enhanced AI Engine initializing on device: {self.device}")
        
        # Initialize AI models
        self.threat_classifier = ThreatClassificationEngine()
        self.contract_analyzer = ContractAnalysisEngine()
        self.predictive_engine = PredictiveThreatEngine()
        self.defense_agent = CyberDefenseAgent()
        
        # System state
        self.is_initialized = False
        self.last_training_time = None
        self.threat_history = []
        self.analysis_cache = {}
        
        # Performance metrics
        self.metrics = {
            'total_threats_analyzed': 0,
            'contracts_scanned': 0,
            'predictions_made': 0,
            'defense_actions_recommended': 0,
            'accuracy_scores': [],
            'response_times': []
        }
        
        logger.info("Enhanced AI Engine initialized successfully!")
    
    async def initialize_models(self, quick_training: bool = True):
        """
        Initialize and train all AI models
        """
        logger.info("Starting AI model initialization and training...")
        
        try:
            # Train models in parallel for efficiency
            training_tasks = []
            
            if quick_training:
                # Quick training for demonstration
                training_tasks.extend([
                    self._train_threat_classifier(epochs=50),
                    self._train_contract_analyzer(epochs=30),
                    self._train_predictive_engine(epochs=50),
                    self._train_defense_agent(episodes=200)
                ])
            else:
                # Full training
                training_tasks.extend([
                    self._train_threat_classifier(epochs=100),
                    self._train_contract_analyzer(epochs=50),
                    self._train_predictive_engine(epochs=100),
                    self._train_defense_agent(episodes=500)
                ])
            
            # Execute training tasks
            await asyncio.gather(*training_tasks)
            
            self.is_initialized = True
            self.last_training_time = datetime.utcnow()
            
            logger.info("All AI models trained and initialized successfully!")
            
        except Exception as e:
            logger.error(f"Error during model initialization: {e}")
            self.is_initialized = False
    
    async def _train_threat_classifier(self, epochs: int = 100):
        """Train the quantum-inspired threat classifier"""
        logger.info(f"Training threat classifier for {epochs} epochs...")
        
        def train_sync():
            self.threat_classifier.train_model(epochs=epochs)
        
        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, train_sync)
        
        logger.info("Threat classifier training completed!")
    
    async def _train_contract_analyzer(self, epochs: int = 50):
        """Train the neural contract analyzer"""
        logger.info(f"Training contract analyzer for {epochs} epochs...")
        
        def train_sync():
            self.contract_analyzer.train_model(epochs=epochs)
        
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, train_sync)
        
        logger.info("Contract analyzer training completed!")
    
    async def _train_predictive_engine(self, epochs: int = 100):
        """Train the predictive threat engine"""
        logger.info(f"Training predictive engine for {epochs} epochs...")
        
        def train_sync():
            self.predictive_engine.train_models(epochs=epochs)
        
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, train_sync)
        
        logger.info("Predictive engine training completed!")
    
    async def _train_defense_agent(self, episodes: int = 500):
        """Train the reinforcement learning defense agent"""
        logger.info(f"Training defense agent for {episodes} episodes...")
        
        def train_sync():
            # Train both DQN and policy networks
            self.defense_agent.train_dqn(episodes=episodes//2)
            self.defense_agent.train_policy(episodes=episodes//2)
        
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, train_sync)
        
        logger.info("Defense agent training completed!")
    
    async def analyze_threat(self, threat_data: Dict) -> Dict:
        """
        Comprehensive threat analysis using all AI models
        """
        start_time = datetime.utcnow()
        
        try:
            # Extract features for analysis
            features = self._extract_threat_features(threat_data)
            
            # Quantum-inspired threat classification
            classification_result = await self._classify_threat(features)
            
            # Pattern analysis and prediction
            prediction_result = await self._predict_threat_evolution(threat_data)
            
            # Defense recommendation
            defense_result = await self._recommend_defense_actions(threat_data)
            
            # Combine results
            analysis_result = {
                'threat_id': threat_data.get('id', f"threat_{len(self.threat_history)}"),
                'timestamp': datetime.utcnow().isoformat(),
                'classification': classification_result,
                'prediction': prediction_result,
                'defense_recommendations': defense_result,
                'confidence_score': self._calculate_overall_confidence([
                    classification_result, prediction_result, defense_result
                ]),
                'processing_time_ms': (datetime.utcnow() - start_time).total_seconds() * 1000
            }
            
            # Update metrics and history
            self.metrics['total_threats_analyzed'] += 1
            self.metrics['response_times'].append(analysis_result['processing_time_ms'])
            self.threat_history.append(analysis_result)
            
            # Keep only recent history
            if len(self.threat_history) > 1000:
                self.threat_history = self.threat_history[-1000:]
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error in threat analysis: {e}")
            return {
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat(),
                'status': 'failed'
            }
    
    async def analyze_smart_contract(self, contract_code: str) -> Dict:
        """
        Advanced smart contract vulnerability analysis
        """
        start_time = datetime.utcnow()
        
        try:
            # Neural network-based analysis
            def analyze_sync():
                return self.contract_analyzer.analyze_contract(contract_code)
            
            loop = asyncio.get_event_loop()
            analysis_result = await loop.run_in_executor(None, analyze_sync)
            
            # Add enhanced features
            analysis_result.update({
                'ai_engine_version': '2.0.0',
                'analysis_method': 'neural_network',
                'processing_time_ms': (datetime.utcnow() - start_time).total_seconds() * 1000
            })
            
            self.metrics['contracts_scanned'] += 1
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error in contract analysis: {e}")
            return {
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat(),
                'status': 'failed'
            }
    
    async def predict_future_threats(self, time_horizon_hours: int = 6) -> Dict:
        """
        Predict future threat patterns using LSTM and pattern analysis
        """
        try:
            # Use historical data for prediction
            historical_data = self.threat_history[-100:] if self.threat_history else None
            
            def predict_sync():
                return self.predictive_engine.predict_threats(historical_data)
            
            loop = asyncio.get_event_loop()
            prediction_result = await loop.run_in_executor(None, predict_sync)
            
            # Add metadata
            prediction_result.update({
                'time_horizon_hours': time_horizon_hours,
                'historical_data_points': len(self.threat_history),
                'ai_engine_version': '2.0.0'
            })
            
            self.metrics['predictions_made'] += 1
            
            return prediction_result
            
        except Exception as e:
            logger.error(f"Error in threat prediction: {e}")
            return {
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat(),
                'status': 'failed'
            }
    
    async def get_defense_strategy(self, current_threat_state: Dict) -> Dict:
        """
        Get AI-powered defense strategy recommendations
        """
        try:
            def get_strategy_sync():
                return self.defense_agent.get_defense_recommendation(current_threat_state)
            
            loop = asyncio.get_event_loop()
            strategy_result = await loop.run_in_executor(None, get_strategy_sync)
            
            # Add training statistics
            training_stats = self.defense_agent.get_training_stats()
            strategy_result.update({
                'training_stats': training_stats,
                'ai_engine_version': '2.0.0'
            })
            
            self.metrics['defense_actions_recommended'] += 1
            
            return strategy_result
            
        except Exception as e:
            logger.error(f"Error in defense strategy generation: {e}")
            return {
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat(),
                'status': 'failed'
            }
    
    async def _classify_threat(self, features: np.ndarray) -> Dict:
        """Classify threat using quantum-inspired classifier"""
        def classify_sync():
            return self.threat_classifier.predict_threat(features)
        
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, classify_sync)
    
    async def _predict_threat_evolution(self, threat_data: Dict) -> Dict:
        """Predict how threat might evolve"""
        # Convert threat data to time series format
        historical_threats = [threat_data] + self.threat_history[-10:]
        
        def predict_sync():
            return self.predictive_engine.predict_threats(historical_threats)
        
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, predict_sync)
    
    async def _recommend_defense_actions(self, threat_data: Dict) -> Dict:
        """Get defense recommendations from RL agent"""
        threat_state = {
            'active_threats': 1,
            'avg_severity': threat_data.get('severity', 0.5),
            'system_health': 0.8  # Default system health
        }
        
        def recommend_sync():
            return self.defense_agent.get_defense_recommendation(threat_state)
        
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, recommend_sync)
    
    def _extract_threat_features(self, threat_data: Dict) -> np.ndarray:
        """Extract numerical features from threat data for ML models"""
        # Create feature vector from threat data
        features = [
            threat_data.get('severity', 0.5),
            threat_data.get('confidence', 0.5),
            len(threat_data.get('affected_systems', [])),
            threat_data.get('impact_score', 0.5),
            int(threat_data.get('type', '') == 'Flash Loan Attack'),
            int(threat_data.get('type', '') == 'Reentrancy Pattern'),
            int(threat_data.get('type', '') == 'MEV Attack'),
            int(threat_data.get('type', '') == 'Phishing Campaign'),
            # Add more features as needed
        ]
        
        # Pad to required length (50 features for quantum classifier)
        while len(features) < 50:
            features.append(np.random.normal(0, 0.1))
        
        return np.array(features[:50], dtype=np.float32)
    
    def _calculate_overall_confidence(self, results: List[Dict]) -> float:
        """Calculate overall confidence from multiple AI model results"""
        confidences = []
        
        for result in results:
            if isinstance(result, dict):
                confidence = result.get('confidence', 0.5)
                if isinstance(confidence, (int, float)):
                    confidences.append(float(confidence))
        
        if not confidences:
            return 0.5
        
        # Weighted average with higher weight for more confident predictions
        weights = [c ** 2 for c in confidences]  # Square to emphasize high confidence
        weighted_sum = sum(c * w for c, w in zip(confidences, weights))
        weight_sum = sum(weights)
        
        return weighted_sum / weight_sum if weight_sum > 0 else 0.5
    
    def get_system_status(self) -> Dict:
        """Get comprehensive system status and metrics"""
        return {
            'status': 'operational' if self.is_initialized else 'initializing',
            'device': str(self.device),
            'models_trained': self.is_initialized,
            'last_training': self.last_training_time.isoformat() if self.last_training_time else None,
            'metrics': {
                **self.metrics,
                'avg_response_time_ms': np.mean(self.metrics['response_times']) if self.metrics['response_times'] else 0,
                'threat_history_size': len(self.threat_history)
            },
            'model_info': {
                'threat_classifier': self.threat_classifier.get_model_info() if hasattr(self.threat_classifier, 'get_model_info') else {},
                'defense_agent': self.defense_agent.get_training_stats()
            },
            'capabilities': [
                'Quantum-Inspired Threat Classification',
                'Neural Contract Analysis',
                'LSTM-based Threat Prediction',
                'Reinforcement Learning Defense',
                'Real-time Pattern Recognition',
                'Anomaly Detection',
                'Automated Response Recommendations'
            ],
            'version': '2.0.0',
            'timestamp': datetime.utcnow().isoformat()
        }
    
    async def retrain_models(self, model_type: Optional[str] = None):
        """Retrain specific models or all models"""
        logger.info(f"Starting model retraining: {model_type or 'all models'}")
        
        try:
            if model_type == 'classifier' or model_type is None:
                await self._train_threat_classifier(epochs=50)
            
            if model_type == 'analyzer' or model_type is None:
                await self._train_contract_analyzer(epochs=30)
            
            if model_type == 'predictor' or model_type is None:
                await self._train_predictive_engine(epochs=50)
            
            if model_type == 'agent' or model_type is None:
                await self._train_defense_agent(episodes=200)
            
            self.last_training_time = datetime.utcnow()
            logger.info("Model retraining completed successfully!")
            
        except Exception as e:
            logger.error(f"Error during model retraining: {e}")
            raise
    
    def clear_cache(self):
        """Clear analysis cache and old history"""
        self.analysis_cache.clear()
        
        # Keep only recent threat history
        if len(self.threat_history) > 500:
            self.threat_history = self.threat_history[-500:]
        
        logger.info("Cache and old history cleared")

# Global instance
enhanced_ai_engine = EnhancedAIEngine()

# Async initialization function
async def initialize_ai_engine(quick_training: bool = True):
    """Initialize the enhanced AI engine"""
    await enhanced_ai_engine.initialize_models(quick_training=quick_training)
    return enhanced_ai_engine

# Convenience functions for API endpoints
async def analyze_threat_enhanced(threat_data: Dict) -> Dict:
    """Enhanced threat analysis endpoint"""
    return await enhanced_ai_engine.analyze_threat(threat_data)

async def analyze_contract_enhanced(contract_code: str) -> Dict:
    """Enhanced contract analysis endpoint"""
    return await enhanced_ai_engine.analyze_smart_contract(contract_code)

async def predict_threats_enhanced(hours: int = 6) -> Dict:
    """Enhanced threat prediction endpoint"""
    return await enhanced_ai_engine.predict_future_threats(hours)

async def get_defense_strategy_enhanced(threat_state: Dict) -> Dict:
    """Enhanced defense strategy endpoint"""
    return await enhanced_ai_engine.get_defense_strategy(threat_state)

def get_ai_status() -> Dict:
    """Get AI engine status"""
    return enhanced_ai_engine.get_system_status() 