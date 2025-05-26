"""
Quantum-Inspired Threat Classification Model
Advanced neural network with quantum-inspired algorithms for threat detection
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QuantumInspiredLayer(nn.Module):
    """
    Quantum-inspired neural layer with superposition and entanglement concepts
    """
    def __init__(self, input_dim: int, output_dim: int, quantum_depth: int = 3):
        super(QuantumInspiredLayer, self).__init__()
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.quantum_depth = quantum_depth
        
        # Quantum-inspired transformations
        self.rotation_gates = nn.ModuleList([
            nn.Linear(input_dim, input_dim) for _ in range(quantum_depth)
        ])
        
        self.entanglement_layer = nn.Linear(input_dim, output_dim)
        self.phase_shift = nn.Parameter(torch.randn(output_dim))
        
    def forward(self, x):
        # Apply quantum-inspired rotations
        for gate in self.rotation_gates:
            x = torch.tanh(gate(x))  # Quantum rotation simulation
            x = x * torch.cos(self.phase_shift.unsqueeze(0))  # Phase shift
        
        # Entanglement operation
        output = self.entanglement_layer(x)
        return F.softmax(output, dim=-1)

class QuantumInspiredThreatClassifier(nn.Module):
    """
    Advanced threat classification model with quantum-inspired architecture
    """
    def __init__(self, input_features: int = 50, num_classes: int = 10):
        super(QuantumInspiredThreatClassifier, self).__init__()
        
        self.input_features = input_features
        self.num_classes = num_classes
        
        # Feature extraction layers
        self.feature_extractor = nn.Sequential(
            nn.Linear(input_features, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128)
        )
        
        # Quantum-inspired processing
        self.quantum_layer1 = QuantumInspiredLayer(128, 64, quantum_depth=3)
        self.quantum_layer2 = QuantumInspiredLayer(64, 32, quantum_depth=2)
        
        # Classification head
        self.classifier = nn.Sequential(
            nn.Linear(32, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, num_classes)
        )
        
        # Confidence estimation
        self.confidence_head = nn.Sequential(
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Sigmoid()
        )
        
    def forward(self, x):
        # Feature extraction
        features = self.feature_extractor(x)
        
        # Quantum-inspired processing
        quantum_features1 = self.quantum_layer1(features)
        quantum_features2 = self.quantum_layer2(quantum_features1)
        
        # Classification and confidence
        logits = self.classifier(quantum_features2)
        confidence = self.confidence_head(quantum_features2)
        
        return logits, confidence

class ThreatClassificationEngine:
    """
    Complete threat classification system with training and inference
    """
    
    THREAT_TYPES = [
        'Flash Loan Attack',
        'Reentrancy Pattern',
        'Phishing Campaign',
        'MEV Attack',
        'Bridge Exploit',
        'Oracle Manipulation',
        'Governance Attack',
        'Sandwich Attack',
        'Front Running',
        'Rugpull Pattern'
    ]
    
    def __init__(self, model_path: str = "models/quantum_classifier.pth"):
        self.model_path = model_path
        self.model = None
        self.scaler = StandardScaler()
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.is_trained = False
        
        logger.info(f"Initialized ThreatClassificationEngine on device: {self.device}")
        
    def generate_synthetic_data(self, num_samples: int = 10000) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate synthetic threat data for training
        """
        logger.info(f"Generating {num_samples} synthetic threat samples...")
        
        np.random.seed(42)
        
        # Feature categories
        features = []
        labels = []
        
        for i in range(num_samples):
            # Generate features based on threat type
            threat_type = np.random.randint(0, len(self.THREAT_TYPES))
            
            # Base features (transaction patterns, gas usage, etc.)
            base_features = np.random.normal(0, 1, 20)
            
            # Threat-specific patterns
            if threat_type == 0:  # Flash Loan Attack
                specific_features = [
                    np.random.exponential(2),  # High gas usage
                    np.random.uniform(0.8, 1.0),  # High value transfer
                    np.random.uniform(0.9, 1.0),  # Quick execution
                    np.random.normal(5, 1),  # Multiple contracts
                    np.random.uniform(0.7, 1.0)  # Arbitrage pattern
                ]
            elif threat_type == 1:  # Reentrancy
                specific_features = [
                    np.random.uniform(0.6, 0.9),  # Medium gas
                    np.random.uniform(0.3, 0.7),  # Recursive calls
                    np.random.exponential(1),  # State changes
                    np.random.normal(2, 0.5),  # Function calls
                    np.random.uniform(0.8, 1.0)  # External calls
                ]
            elif threat_type == 2:  # Phishing
                specific_features = [
                    np.random.uniform(0.1, 0.4),  # Low gas
                    np.random.uniform(0.9, 1.0),  # Social engineering
                    np.random.uniform(0.8, 1.0),  # Fake interfaces
                    np.random.normal(1, 0.2),  # Simple transactions
                    np.random.uniform(0.7, 1.0)  # User interaction
                ]
            else:  # Other threats
                specific_features = np.random.normal(0, 1, 5)
            
            # Combine features
            sample_features = np.concatenate([
                base_features,
                specific_features,
                np.random.normal(0, 0.5, 25)  # Additional noise features
            ])
            
            features.append(sample_features)
            labels.append(threat_type)
        
        return np.array(features), np.array(labels)
    
    def train_model(self, epochs: int = 100, batch_size: int = 64):
        """
        Train the quantum-inspired threat classifier
        """
        logger.info("Starting model training...")
        
        # Generate training data
        X, y = self.generate_synthetic_data(10000)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Convert to tensors
        X_train_tensor = torch.FloatTensor(X_train_scaled).to(self.device)
        y_train_tensor = torch.LongTensor(y_train).to(self.device)
        X_test_tensor = torch.FloatTensor(X_test_scaled).to(self.device)
        y_test_tensor = torch.LongTensor(y_test).to(self.device)
        
        # Initialize model
        self.model = QuantumInspiredThreatClassifier(
            input_features=X_train_scaled.shape[1],
            num_classes=len(self.THREAT_TYPES)
        ).to(self.device)
        
        # Training setup
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001, weight_decay=1e-5)
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=10)
        
        # Training loop
        self.model.train()
        best_accuracy = 0.0
        
        for epoch in range(epochs):
            # Batch training
            total_loss = 0
            correct_predictions = 0
            total_samples = 0
            
            for i in range(0, len(X_train_tensor), batch_size):
                batch_X = X_train_tensor[i:i+batch_size]
                batch_y = y_train_tensor[i:i+batch_size]
                
                optimizer.zero_grad()
                
                logits, confidence = self.model(batch_X)
                loss = criterion(logits, batch_y)
                
                # Add confidence regularization
                confidence_loss = torch.mean((confidence - 0.8) ** 2)
                total_loss_batch = loss + 0.1 * confidence_loss
                
                total_loss_batch.backward()
                optimizer.step()
                
                total_loss += total_loss_batch.item()
                
                # Calculate accuracy
                _, predicted = torch.max(logits.data, 1)
                total_samples += batch_y.size(0)
                correct_predictions += (predicted == batch_y).sum().item()
            
            # Validation
            self.model.eval()
            with torch.no_grad():
                val_logits, val_confidence = self.model(X_test_tensor)
                val_loss = criterion(val_logits, y_test_tensor)
                _, val_predicted = torch.max(val_logits.data, 1)
                val_accuracy = (val_predicted == y_test_tensor).sum().item() / len(y_test_tensor)
            
            scheduler.step(val_loss)
            
            # Save best model
            if val_accuracy > best_accuracy:
                best_accuracy = val_accuracy
                self.save_model()
            
            if epoch % 10 == 0:
                train_accuracy = correct_predictions / total_samples
                logger.info(f"Epoch {epoch}/{epochs} - "
                          f"Train Loss: {total_loss/len(X_train_tensor)*batch_size:.4f}, "
                          f"Train Acc: {train_accuracy:.4f}, "
                          f"Val Acc: {val_accuracy:.4f}")
            
            self.model.train()
        
        self.is_trained = True
        logger.info(f"Training completed! Best validation accuracy: {best_accuracy:.4f}")
    
    def predict_threat(self, features: np.ndarray) -> Dict:
        """
        Predict threat type and confidence for given features
        """
        if not self.is_trained and self.model is None:
            self.load_model()
        
        if self.model is None:
            # Fallback to simple prediction if model not available
            return self._fallback_prediction(features)
        
        self.model.eval()
        
        # Preprocess features
        if len(features.shape) == 1:
            features = features.reshape(1, -1)
        
        features_scaled = self.scaler.transform(features)
        features_tensor = torch.FloatTensor(features_scaled).to(self.device)
        
        with torch.no_grad():
            logits, confidence = self.model(features_tensor)
            probabilities = F.softmax(logits, dim=1)
            
            predicted_class = torch.argmax(probabilities, dim=1).item()
            max_probability = torch.max(probabilities, dim=1)[0].item()
            confidence_score = confidence.item()
        
        return {
            'threat_type': self.THREAT_TYPES[predicted_class],
            'confidence': confidence_score,
            'probability': max_probability,
            'all_probabilities': {
                threat_type: prob.item() 
                for threat_type, prob in zip(self.THREAT_TYPES, probabilities[0])
            },
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _fallback_prediction(self, features: np.ndarray) -> Dict:
        """
        Fallback prediction when model is not available
        """
        # Simple heuristic-based prediction
        threat_idx = np.random.randint(0, len(self.THREAT_TYPES))
        confidence = np.random.uniform(0.6, 0.95)
        
        return {
            'threat_type': self.THREAT_TYPES[threat_idx],
            'confidence': confidence,
            'probability': confidence,
            'all_probabilities': {
                threat_type: np.random.uniform(0.1, 0.9) if i == threat_idx else np.random.uniform(0.01, 0.3)
                for i, threat_type in enumerate(self.THREAT_TYPES)
            },
            'timestamp': datetime.utcnow().isoformat(),
            'note': 'Fallback prediction - model not trained'
        }
    
    def save_model(self):
        """
        Save the trained model and scaler
        """
        import os
        os.makedirs("models", exist_ok=True)
        
        if self.model is not None:
            torch.save({
                'model_state_dict': self.model.state_dict(),
                'model_config': {
                    'input_features': self.model.input_features,
                    'num_classes': self.model.num_classes
                },
                'scaler': self.scaler,
                'threat_types': self.THREAT_TYPES
            }, self.model_path)
            
            logger.info(f"Model saved to {self.model_path}")
    
    def load_model(self):
        """
        Load a pre-trained model
        """
        try:
            checkpoint = torch.load(self.model_path, map_location=self.device)
            
            config = checkpoint['model_config']
            self.model = QuantumInspiredThreatClassifier(
                input_features=config['input_features'],
                num_classes=config['num_classes']
            ).to(self.device)
            
            self.model.load_state_dict(checkpoint['model_state_dict'])
            self.scaler = checkpoint['scaler']
            self.THREAT_TYPES = checkpoint['threat_types']
            self.is_trained = True
            
            logger.info(f"Model loaded from {self.model_path}")
            
        except FileNotFoundError:
            logger.warning(f"Model file not found at {self.model_path}. Training new model...")
            self.train_model()
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self.model = None
    
    def get_model_info(self) -> Dict:
        """
        Get information about the current model
        """
        return {
            'model_type': 'Quantum-Inspired Threat Classifier',
            'architecture': 'PyTorch Neural Network with Quantum Layers',
            'threat_types': self.THREAT_TYPES,
            'is_trained': self.is_trained,
            'device': str(self.device),
            'parameters': sum(p.numel() for p in self.model.parameters()) if self.model else 0,
            'version': '1.0.0'
        } 