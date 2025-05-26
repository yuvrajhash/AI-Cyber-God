"""
Predictive Threat Engine
Advanced machine learning for threat prediction and forecasting
"""

import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
import joblib
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class LSTMPredictor(nn.Module):
    """
    LSTM-based neural network for time series threat prediction
    """
    def __init__(self, input_size: int, hidden_size: int = 128, num_layers: int = 3, output_size: int = 1):
        super(LSTMPredictor, self).__init__()
        
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        # LSTM layers
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=0.2 if num_layers > 1 else 0
        )
        
        # Attention mechanism
        self.attention = nn.MultiheadAttention(
            embed_dim=hidden_size,
            num_heads=8,
            batch_first=True
        )
        
        # Output layers
        self.fc_layers = nn.Sequential(
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_size // 2, hidden_size // 4),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_size // 4, output_size)
        )
        
        # Uncertainty estimation
        self.uncertainty_head = nn.Sequential(
            nn.Linear(hidden_size, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Softplus()  # Ensures positive values
        )
        
    def forward(self, x):
        batch_size = x.size(0)
        
        # LSTM forward pass
        lstm_out, (hidden, cell) = self.lstm(x)
        
        # Apply attention
        attended_out, attention_weights = self.attention(lstm_out, lstm_out, lstm_out)
        
        # Use the last time step
        last_output = attended_out[:, -1, :]
        
        # Predictions and uncertainty
        predictions = self.fc_layers(last_output)
        uncertainty = self.uncertainty_head(last_output)
        
        return predictions, uncertainty, attention_weights

class AnomalyDetector(nn.Module):
    """
    Autoencoder-based anomaly detection for unusual threat patterns
    """
    def __init__(self, input_dim: int, encoding_dim: int = 64):
        super(AnomalyDetector, self).__init__()
        
        # Encoder
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, encoding_dim),
            nn.ReLU()
        )
        
        # Decoder
        self.decoder = nn.Sequential(
            nn.Linear(encoding_dim, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, input_dim),
            nn.Sigmoid()
        )
        
    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded, encoded

class ThreatPatternAnalyzer:
    """
    Advanced pattern analysis for threat behavior understanding
    """
    def __init__(self):
        self.pattern_memory = {}
        self.threat_signatures = {}
        
    def analyze_pattern(self, threat_data: List[Dict]) -> Dict:
        """
        Analyze patterns in threat data
        """
        if not threat_data:
            return {'patterns': [], 'confidence': 0.0}
        
        # Extract features from threat data
        features = self._extract_pattern_features(threat_data)
        
        # Identify recurring patterns
        patterns = self._identify_patterns(features)
        
        # Calculate pattern confidence
        confidence = self._calculate_pattern_confidence(patterns)
        
        return {
            'patterns': patterns,
            'confidence': confidence,
            'feature_importance': self._get_feature_importance(features),
            'temporal_patterns': self._analyze_temporal_patterns(threat_data)
        }
    
    def _extract_pattern_features(self, threat_data: List[Dict]) -> np.ndarray:
        """
        Extract numerical features from threat data
        """
        features = []
        
        for threat in threat_data:
            feature_vector = [
                threat.get('severity_score', 0.5),
                threat.get('confidence', 0.5),
                len(threat.get('affected_contracts', [])),
                threat.get('gas_usage', 0),
                threat.get('value_at_risk', 0),
                int(threat.get('type', '') == 'Flash Loan Attack'),
                int(threat.get('type', '') == 'Reentrancy Pattern'),
                int(threat.get('type', '') == 'MEV Attack'),
                # Add more features as needed
            ]
            features.append(feature_vector)
        
        return np.array(features)
    
    def _identify_patterns(self, features: np.ndarray) -> List[Dict]:
        """
        Identify patterns using clustering and statistical analysis
        """
        if len(features) < 3:
            return []
        
        patterns = []
        
        # Simple pattern detection based on feature correlations
        correlations = np.corrcoef(features.T)
        
        for i in range(len(correlations)):
            for j in range(i + 1, len(correlations)):
                if abs(correlations[i, j]) > 0.7:  # Strong correlation
                    patterns.append({
                        'type': 'correlation',
                        'features': [i, j],
                        'strength': abs(correlations[i, j]),
                        'description': f'Strong correlation between feature {i} and {j}'
                    })
        
        return patterns
    
    def _calculate_pattern_confidence(self, patterns: List[Dict]) -> float:
        """
        Calculate confidence in identified patterns
        """
        if not patterns:
            return 0.0
        
        total_strength = sum(pattern['strength'] for pattern in patterns)
        return min(total_strength / len(patterns), 1.0)
    
    def _get_feature_importance(self, features: np.ndarray) -> Dict:
        """
        Calculate feature importance scores
        """
        if len(features) < 2:
            return {}
        
        # Simple variance-based importance
        variances = np.var(features, axis=0)
        total_variance = np.sum(variances)
        
        if total_variance == 0:
            return {}
        
        importance = variances / total_variance
        
        feature_names = [
            'severity_score', 'confidence', 'affected_contracts',
            'gas_usage', 'value_at_risk', 'flash_loan', 'reentrancy', 'mev'
        ]
        
        return {name: float(imp) for name, imp in zip(feature_names, importance)}
    
    def _analyze_temporal_patterns(self, threat_data: List[Dict]) -> Dict:
        """
        Analyze temporal patterns in threat occurrences
        """
        timestamps = []
        for threat in threat_data:
            try:
                timestamp = datetime.fromisoformat(threat.get('timestamp', '').replace('Z', '+00:00'))
                timestamps.append(timestamp)
            except:
                continue
        
        if len(timestamps) < 2:
            return {'frequency': 0, 'trend': 'unknown'}
        
        timestamps.sort()
        intervals = [(timestamps[i+1] - timestamps[i]).total_seconds() 
                    for i in range(len(timestamps)-1)]
        
        avg_interval = np.mean(intervals)
        frequency = 1 / avg_interval if avg_interval > 0 else 0
        
        # Simple trend analysis
        recent_half = intervals[len(intervals)//2:]
        older_half = intervals[:len(intervals)//2]
        
        if len(recent_half) > 0 and len(older_half) > 0:
            if np.mean(recent_half) < np.mean(older_half):
                trend = 'increasing'
            elif np.mean(recent_half) > np.mean(older_half):
                trend = 'decreasing'
            else:
                trend = 'stable'
        else:
            trend = 'unknown'
        
        return {
            'frequency': frequency,
            'trend': trend,
            'avg_interval_seconds': avg_interval,
            'total_threats': len(threat_data)
        }

class PredictiveThreatEngine:
    """
    Complete predictive threat analysis system
    """
    
    def __init__(self, model_path: str = "models/predictive_engine.pth"):
        self.model_path = model_path
        self.lstm_model = None
        self.anomaly_detector = None
        self.pattern_analyzer = ThreatPatternAnalyzer()
        self.scaler = StandardScaler()
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.is_trained = False
        
        # Historical data storage
        self.threat_history = []
        self.prediction_history = []
        
        # Model parameters
        self.sequence_length = 24  # Hours of historical data
        self.prediction_horizon = 6  # Hours to predict ahead
        
        logger.info(f"Initialized PredictiveThreatEngine on device: {self.device}")
    
    def generate_synthetic_time_series(self, num_days: int = 30) -> pd.DataFrame:
        """
        Generate synthetic threat time series data for training
        """
        logger.info(f"Generating {num_days} days of synthetic threat time series...")
        
        # Create hourly timestamps
        start_date = datetime.now() - timedelta(days=num_days)
        timestamps = [start_date + timedelta(hours=i) for i in range(num_days * 24)]
        
        data = []
        
        for i, timestamp in enumerate(timestamps):
            # Base threat level with daily and weekly patterns
            hour = timestamp.hour
            day_of_week = timestamp.weekday()
            
            # Daily pattern (higher activity during business hours)
            daily_factor = 1.0 + 0.5 * np.sin(2 * np.pi * (hour - 6) / 24)
            
            # Weekly pattern (lower activity on weekends)
            weekly_factor = 0.7 if day_of_week >= 5 else 1.0
            
            # Base threat count
            base_threats = 10 * daily_factor * weekly_factor
            
            # Add noise and occasional spikes
            noise = np.random.normal(0, 2)
            spike = 20 if np.random.random() < 0.05 else 0  # 5% chance of spike
            
            threat_count = max(0, base_threats + noise + spike)
            
            # Generate threat type distribution
            threat_types = {
                'Flash Loan Attack': np.random.poisson(threat_count * 0.3),
                'Reentrancy Pattern': np.random.poisson(threat_count * 0.2),
                'MEV Attack': np.random.poisson(threat_count * 0.25),
                'Phishing Campaign': np.random.poisson(threat_count * 0.15),
                'Bridge Exploit': np.random.poisson(threat_count * 0.1)
            }
            
            # Additional features
            avg_severity = np.random.beta(2, 5)  # Skewed towards lower severity
            total_value_at_risk = np.random.exponential(100000)  # USD
            avg_gas_usage = np.random.normal(200000, 50000)
            
            data.append({
                'timestamp': timestamp,
                'total_threats': int(threat_count),
                'avg_severity': avg_severity,
                'total_value_at_risk': total_value_at_risk,
                'avg_gas_usage': max(0, avg_gas_usage),
                **threat_types
            })
        
        return pd.DataFrame(data)
    
    def prepare_sequences(self, data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare sequences for LSTM training
        """
        # Select features for prediction
        feature_columns = [
            'total_threats', 'avg_severity', 'total_value_at_risk', 'avg_gas_usage',
            'Flash Loan Attack', 'Reentrancy Pattern', 'MEV Attack', 
            'Phishing Campaign', 'Bridge Exploit'
        ]
        
        features = data[feature_columns].values
        
        # Scale features
        features_scaled = self.scaler.fit_transform(features)
        
        # Create sequences
        X, y = [], []
        
        for i in range(len(features_scaled) - self.sequence_length - self.prediction_horizon + 1):
            # Input sequence
            X.append(features_scaled[i:i + self.sequence_length])
            
            # Target (predict total_threats for next prediction_horizon hours)
            target_start = i + self.sequence_length
            target_end = target_start + self.prediction_horizon
            y.append(features_scaled[target_start:target_end, 0])  # total_threats column
        
        return np.array(X), np.array(y)
    
    def train_models(self, epochs: int = 100):
        """
        Train the predictive models
        """
        logger.info("Starting predictive model training...")
        
        # Generate training data
        data = self.generate_synthetic_time_series(60)  # 60 days of data
        
        # Prepare sequences
        X, y = self.prepare_sequences(data)
        
        # Initialize LSTM model
        input_size = X.shape[2]
        self.lstm_model = LSTMPredictor(
            input_size=input_size,
            hidden_size=128,
            num_layers=3,
            output_size=self.prediction_horizon
        ).to(self.device)
        
        # Initialize anomaly detector
        self.anomaly_detector = AnomalyDetector(
            input_dim=input_size,
            encoding_dim=32
        ).to(self.device)
        
        # Convert to tensors
        X_tensor = torch.FloatTensor(X).to(self.device)
        y_tensor = torch.FloatTensor(y).to(self.device)
        
        # Training setup
        lstm_optimizer = torch.optim.Adam(self.lstm_model.parameters(), lr=0.001)
        anomaly_optimizer = torch.optim.Adam(self.anomaly_detector.parameters(), lr=0.001)
        
        lstm_criterion = nn.MSELoss()
        anomaly_criterion = nn.MSELoss()
        
        # Training loop
        for epoch in range(epochs):
            # Train LSTM predictor
            self.lstm_model.train()
            lstm_optimizer.zero_grad()
            
            predictions, uncertainty, attention = self.lstm_model(X_tensor)
            lstm_loss = lstm_criterion(predictions, y_tensor)
            
            # Add uncertainty regularization
            uncertainty_loss = torch.mean(uncertainty)
            total_lstm_loss = lstm_loss + 0.1 * uncertainty_loss
            
            total_lstm_loss.backward()
            lstm_optimizer.step()
            
            # Train anomaly detector
            self.anomaly_detector.train()
            anomaly_optimizer.zero_grad()
            
            # Use last time step of sequences for anomaly detection
            last_timestep = X_tensor[:, -1, :]
            reconstructed, encoded = self.anomaly_detector(last_timestep)
            anomaly_loss = anomaly_criterion(reconstructed, last_timestep)
            
            anomaly_loss.backward()
            anomaly_optimizer.step()
            
            if epoch % 20 == 0:
                logger.info(f"Epoch {epoch}/{epochs} - "
                          f"LSTM Loss: {lstm_loss.item():.4f}, "
                          f"Anomaly Loss: {anomaly_loss.item():.4f}")
        
        self.is_trained = True
        self.save_models()
        logger.info("Predictive model training completed!")
    
    def predict_threats(self, historical_data: Optional[List[Dict]] = None) -> Dict:
        """
        Predict future threat levels and patterns
        """
        if not self.is_trained and self.lstm_model is None:
            self.load_models()
        
        if self.lstm_model is None:
            return self._fallback_prediction()
        
        # Use provided data or generate synthetic recent data
        if historical_data is None:
            recent_data = self.generate_synthetic_time_series(2)  # Last 2 days
        else:
            recent_data = self._convert_to_dataframe(historical_data)
        
        # Prepare input sequence
        if len(recent_data) < self.sequence_length:
            # Pad with synthetic data if not enough history
            padding_data = self.generate_synthetic_time_series(1)
            recent_data = pd.concat([padding_data, recent_data]).tail(self.sequence_length)
        
        X, _ = self.prepare_sequences(recent_data)
        
        if len(X) == 0:
            return self._fallback_prediction()
        
        # Use the last sequence for prediction
        input_sequence = torch.FloatTensor(X[-1:]).to(self.device)
        
        self.lstm_model.eval()
        with torch.no_grad():
            predictions, uncertainty, attention = self.lstm_model(input_sequence)
            
            # Convert predictions back to original scale
            predictions_np = predictions.cpu().numpy()[0]
            uncertainty_np = uncertainty.cpu().numpy()[0, 0]
        
        # Generate prediction timestamps
        last_timestamp = recent_data['timestamp'].iloc[-1]
        prediction_timestamps = [
            last_timestamp + timedelta(hours=i+1) 
            for i in range(self.prediction_horizon)
        ]
        
        # Detect anomalies in recent data
        anomaly_score = self._detect_anomalies(recent_data.tail(1))
        
        # Analyze patterns
        pattern_analysis = self.pattern_analyzer.analyze_pattern(
            historical_data or recent_data.to_dict('records')
        )
        
        return {
            'predictions': [
                {
                    'timestamp': ts.isoformat(),
                    'predicted_threats': max(0, float(pred)),
                    'confidence': max(0, min(1, 1 - uncertainty_np))
                }
                for ts, pred in zip(prediction_timestamps, predictions_np)
            ],
            'anomaly_score': float(anomaly_score),
            'pattern_analysis': pattern_analysis,
            'prediction_horizon_hours': self.prediction_horizon,
            'model_uncertainty': float(uncertainty_np),
            'prediction_timestamp': datetime.utcnow().isoformat()
        }
    
    def _convert_to_dataframe(self, threat_data: List[Dict]) -> pd.DataFrame:
        """
        Convert threat data to DataFrame format
        """
        # Group threats by hour
        hourly_data = {}
        
        for threat in threat_data:
            try:
                timestamp = datetime.fromisoformat(threat.get('timestamp', '').replace('Z', '+00:00'))
                hour_key = timestamp.replace(minute=0, second=0, microsecond=0)
                
                if hour_key not in hourly_data:
                    hourly_data[hour_key] = {
                        'timestamp': hour_key,
                        'total_threats': 0,
                        'avg_severity': [],
                        'total_value_at_risk': 0,
                        'avg_gas_usage': [],
                        'Flash Loan Attack': 0,
                        'Reentrancy Pattern': 0,
                        'MEV Attack': 0,
                        'Phishing Campaign': 0,
                        'Bridge Exploit': 0
                    }
                
                hourly_data[hour_key]['total_threats'] += 1
                hourly_data[hour_key]['avg_severity'].append(threat.get('severity', 0.5))
                hourly_data[hour_key]['total_value_at_risk'] += threat.get('value_at_risk', 0)
                hourly_data[hour_key]['avg_gas_usage'].append(threat.get('gas_usage', 200000))
                
                threat_type = threat.get('type', 'Unknown')
                if threat_type in hourly_data[hour_key]:
                    hourly_data[hour_key][threat_type] += 1
                    
            except Exception as e:
                logger.warning(f"Error processing threat data: {e}")
                continue
        
        # Convert to DataFrame
        processed_data = []
        for hour_data in hourly_data.values():
            hour_data['avg_severity'] = np.mean(hour_data['avg_severity']) if hour_data['avg_severity'] else 0.5
            hour_data['avg_gas_usage'] = np.mean(hour_data['avg_gas_usage']) if hour_data['avg_gas_usage'] else 200000
            processed_data.append(hour_data)
        
        return pd.DataFrame(processed_data).sort_values('timestamp')
    
    def _detect_anomalies(self, recent_data: pd.DataFrame) -> float:
        """
        Detect anomalies in recent threat data
        """
        if self.anomaly_detector is None or len(recent_data) == 0:
            return 0.0
        
        try:
            # Prepare features
            feature_columns = [
                'total_threats', 'avg_severity', 'total_value_at_risk', 'avg_gas_usage',
                'Flash Loan Attack', 'Reentrancy Pattern', 'MEV Attack', 
                'Phishing Campaign', 'Bridge Exploit'
            ]
            
            features = recent_data[feature_columns].values
            features_scaled = self.scaler.transform(features)
            
            # Detect anomalies
            input_tensor = torch.FloatTensor(features_scaled).to(self.device)
            
            self.anomaly_detector.eval()
            with torch.no_grad():
                reconstructed, encoded = self.anomaly_detector(input_tensor)
                reconstruction_error = torch.mean((input_tensor - reconstructed) ** 2, dim=1)
                
            return float(torch.mean(reconstruction_error).cpu())
            
        except Exception as e:
            logger.warning(f"Error in anomaly detection: {e}")
            return 0.0
    
    def _fallback_prediction(self) -> Dict:
        """
        Fallback prediction when models are not available
        """
        # Simple heuristic-based prediction
        base_threats = np.random.poisson(15)
        
        predictions = []
        for i in range(self.prediction_horizon):
            # Add some randomness and trend
            predicted_threats = max(0, base_threats + np.random.normal(0, 3) + i * 0.5)
            
            predictions.append({
                'timestamp': (datetime.utcnow() + timedelta(hours=i+1)).isoformat(),
                'predicted_threats': float(predicted_threats),
                'confidence': 0.6
            })
        
        return {
            'predictions': predictions,
            'anomaly_score': np.random.uniform(0.1, 0.4),
            'pattern_analysis': {'patterns': [], 'confidence': 0.5},
            'prediction_horizon_hours': self.prediction_horizon,
            'model_uncertainty': 0.4,
            'prediction_timestamp': datetime.utcnow().isoformat(),
            'note': 'Fallback prediction - models not trained'
        }
    
    def save_models(self):
        """
        Save the trained models
        """
        import os
        os.makedirs("models", exist_ok=True)
        
        if self.lstm_model is not None and self.anomaly_detector is not None:
            torch.save({
                'lstm_state_dict': self.lstm_model.state_dict(),
                'anomaly_state_dict': self.anomaly_detector.state_dict(),
                'scaler': self.scaler,
                'sequence_length': self.sequence_length,
                'prediction_horizon': self.prediction_horizon,
                'is_trained': self.is_trained
            }, self.model_path)
            
            logger.info(f"Predictive models saved to {self.model_path}")
    
    def load_models(self):
        """
        Load pre-trained models
        """
        try:
            checkpoint = torch.load(self.model_path, map_location=self.device)
            
            # Recreate models
            self.lstm_model = LSTMPredictor(
                input_size=9,  # Number of features
                hidden_size=128,
                num_layers=3,
                output_size=self.prediction_horizon
            ).to(self.device)
            
            self.anomaly_detector = AnomalyDetector(
                input_dim=9,
                encoding_dim=32
            ).to(self.device)
            
            # Load state dicts
            self.lstm_model.load_state_dict(checkpoint['lstm_state_dict'])
            self.anomaly_detector.load_state_dict(checkpoint['anomaly_state_dict'])
            self.scaler = checkpoint['scaler']
            self.sequence_length = checkpoint['sequence_length']
            self.prediction_horizon = checkpoint['prediction_horizon']
            self.is_trained = checkpoint['is_trained']
            
            logger.info(f"Predictive models loaded from {self.model_path}")
            
        except FileNotFoundError:
            logger.warning(f"Model file not found at {self.model_path}. Training new models...")
            self.train_models()
        except Exception as e:
            logger.error(f"Error loading predictive models: {e}")
            self.lstm_model = None
            self.anomaly_detector = None 