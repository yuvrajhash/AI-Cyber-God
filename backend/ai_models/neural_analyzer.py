"""
Neural Smart Contract Analyzer
Advanced deep learning model for smart contract vulnerability detection
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
import re
import hashlib
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class AttentionLayer(nn.Module):
    """
    Multi-head attention layer for contract analysis
    """
    def __init__(self, embed_dim: int, num_heads: int = 8):
        super(AttentionLayer, self).__init__()
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads
        
        assert self.head_dim * num_heads == embed_dim, "embed_dim must be divisible by num_heads"
        
        self.query = nn.Linear(embed_dim, embed_dim)
        self.key = nn.Linear(embed_dim, embed_dim)
        self.value = nn.Linear(embed_dim, embed_dim)
        self.out = nn.Linear(embed_dim, embed_dim)
        
    def forward(self, x):
        batch_size, seq_len, embed_dim = x.size()
        
        # Generate Q, K, V
        Q = self.query(x).view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        K = self.key(x).view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        V = self.value(x).view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        
        # Attention scores
        scores = torch.matmul(Q, K.transpose(-2, -1)) / np.sqrt(self.head_dim)
        attention_weights = F.softmax(scores, dim=-1)
        
        # Apply attention
        attended = torch.matmul(attention_weights, V)
        attended = attended.transpose(1, 2).contiguous().view(batch_size, seq_len, embed_dim)
        
        return self.out(attended)

class ContractEncoder(nn.Module):
    """
    Transformer-based encoder for smart contract code
    """
    def __init__(self, vocab_size: int, embed_dim: int = 256, num_layers: int = 6):
        super(ContractEncoder, self).__init__()
        self.embed_dim = embed_dim
        
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.positional_encoding = nn.Parameter(torch.randn(1000, embed_dim))
        
        self.layers = nn.ModuleList([
            nn.ModuleDict({
                'attention': AttentionLayer(embed_dim),
                'norm1': nn.LayerNorm(embed_dim),
                'ffn': nn.Sequential(
                    nn.Linear(embed_dim, embed_dim * 4),
                    nn.ReLU(),
                    nn.Dropout(0.1),
                    nn.Linear(embed_dim * 4, embed_dim)
                ),
                'norm2': nn.LayerNorm(embed_dim)
            }) for _ in range(num_layers)
        ])
        
    def forward(self, x):
        seq_len = x.size(1)
        
        # Embedding + positional encoding
        x = self.embedding(x) + self.positional_encoding[:seq_len].unsqueeze(0)
        
        # Transformer layers
        for layer in self.layers:
            # Self-attention
            attended = layer['attention'](x)
            x = layer['norm1'](x + attended)
            
            # Feed-forward
            ffn_out = layer['ffn'](x)
            x = layer['norm2'](x + ffn_out)
        
        return x

class VulnerabilityDetector(nn.Module):
    """
    Multi-task vulnerability detection head
    """
    def __init__(self, input_dim: int, num_vulnerability_types: int = 15):
        super(VulnerabilityDetector, self).__init__()
        
        self.global_pool = nn.AdaptiveAvgPool1d(1)
        
        # Vulnerability-specific heads
        self.vulnerability_heads = nn.ModuleDict({
            'reentrancy': nn.Sequential(
                nn.Linear(input_dim, 128),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(128, 2)  # Binary classification
            ),
            'integer_overflow': nn.Sequential(
                nn.Linear(input_dim, 128),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(128, 2)
            ),
            'access_control': nn.Sequential(
                nn.Linear(input_dim, 128),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(128, 2)
            ),
            'timestamp_dependency': nn.Sequential(
                nn.Linear(input_dim, 128),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(128, 2)
            ),
            'unchecked_calls': nn.Sequential(
                nn.Linear(input_dim, 128),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(128, 2)
            )
        })
        
        # Overall risk assessment
        self.risk_head = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )
        
        # Confidence estimation
        self.confidence_head = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )
    
    def forward(self, x):
        # Global pooling
        pooled = self.global_pool(x.transpose(1, 2)).squeeze(-1)
        
        # Vulnerability predictions
        vulnerability_outputs = {}
        for vuln_type, head in self.vulnerability_heads.items():
            vulnerability_outputs[vuln_type] = head(pooled)
        
        # Risk and confidence
        risk_score = self.risk_head(pooled)
        confidence = self.confidence_head(pooled)
        
        return vulnerability_outputs, risk_score, confidence

class NeuralContractAnalyzer(nn.Module):
    """
    Complete neural network for smart contract analysis
    """
    def __init__(self, vocab_size: int = 10000, embed_dim: int = 256):
        super(NeuralContractAnalyzer, self).__init__()
        
        self.encoder = ContractEncoder(vocab_size, embed_dim)
        self.detector = VulnerabilityDetector(embed_dim)
        
    def forward(self, x):
        encoded = self.encoder(x)
        vulnerabilities, risk, confidence = self.detector(encoded)
        
        return vulnerabilities, risk, confidence

class ContractAnalysisEngine:
    """
    Complete smart contract analysis system
    """
    
    VULNERABILITY_TYPES = [
        'reentrancy',
        'integer_overflow',
        'access_control',
        'timestamp_dependency',
        'unchecked_calls',
        'denial_of_service',
        'front_running',
        'short_address',
        'uninitialized_storage',
        'delegatecall_injection',
        'tx_origin_authentication',
        'floating_pragma',
        'outdated_compiler',
        'unsafe_type_inference',
        'unprotected_ether_withdrawal'
    ]
    
    VULNERABILITY_DESCRIPTIONS = {
        'reentrancy': 'Function can be called recursively before state changes are finalized',
        'integer_overflow': 'Arithmetic operations may overflow or underflow',
        'access_control': 'Missing or insufficient access control mechanisms',
        'timestamp_dependency': 'Logic depends on block timestamp which can be manipulated',
        'unchecked_calls': 'External calls without proper error handling',
        'denial_of_service': 'Contract can be made unusable by malicious actors',
        'front_running': 'Transactions can be front-run for profit',
        'short_address': 'Vulnerable to short address attacks',
        'uninitialized_storage': 'Storage variables not properly initialized',
        'delegatecall_injection': 'Unsafe use of delegatecall',
        'tx_origin_authentication': 'Using tx.origin for authentication',
        'floating_pragma': 'Pragma version not fixed',
        'outdated_compiler': 'Using outdated Solidity compiler',
        'unsafe_type_inference': 'Relying on unsafe type inference',
        'unprotected_ether_withdrawal': 'Ether withdrawal without proper protection'
    }
    
    def __init__(self, model_path: str = "models/neural_analyzer.pth"):
        self.model_path = model_path
        self.model = None
        self.vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1, 3))
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.is_trained = False
        self.vocab_size = 10000
        
        # Contract patterns for vulnerability detection
        self.vulnerability_patterns = {
            'reentrancy': [
                r'\.call\s*\(',
                r'\.send\s*\(',
                r'\.transfer\s*\(',
                r'external.*payable',
                r'msg\.value'
            ],
            'integer_overflow': [
                r'\+\+',
                r'--',
                r'\+=',
                r'-=',
                r'\*=',
                r'SafeMath'
            ],
            'access_control': [
                r'onlyOwner',
                r'require\s*\(',
                r'modifier',
                r'msg\.sender',
                r'owner'
            ],
            'timestamp_dependency': [
                r'block\.timestamp',
                r'now',
                r'block\.number'
            ],
            'unchecked_calls': [
                r'\.call\s*\(',
                r'\.delegatecall\s*\(',
                r'\.staticcall\s*\('
            ]
        }
        
        logger.info(f"Initialized NeuralContractAnalyzer on device: {self.device}")
    
    def preprocess_contract(self, contract_code: str) -> Dict:
        """
        Preprocess smart contract code for analysis
        """
        # Clean and normalize code
        cleaned_code = re.sub(r'//.*?\n', '\n', contract_code)  # Remove comments
        cleaned_code = re.sub(r'/\*.*?\*/', '', cleaned_code, flags=re.DOTALL)  # Remove block comments
        cleaned_code = re.sub(r'\s+', ' ', cleaned_code)  # Normalize whitespace
        
        # Extract features
        features = {
            'code_length': len(cleaned_code),
            'function_count': len(re.findall(r'function\s+\w+', cleaned_code)),
            'modifier_count': len(re.findall(r'modifier\s+\w+', cleaned_code)),
            'event_count': len(re.findall(r'event\s+\w+', cleaned_code)),
            'external_calls': len(re.findall(r'\.call\s*\(', cleaned_code)),
            'payable_functions': len(re.findall(r'payable', cleaned_code)),
            'require_statements': len(re.findall(r'require\s*\(', cleaned_code)),
            'assert_statements': len(re.findall(r'assert\s*\(', cleaned_code))
        }
        
        # Pattern-based vulnerability indicators
        vulnerability_indicators = {}
        for vuln_type, patterns in self.vulnerability_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, cleaned_code, re.IGNORECASE))
                score += matches
            vulnerability_indicators[vuln_type] = min(score / 10.0, 1.0)  # Normalize to [0, 1]
        
        return {
            'cleaned_code': cleaned_code,
            'features': features,
            'vulnerability_indicators': vulnerability_indicators
        }
    
    def generate_synthetic_contracts(self, num_samples: int = 5000) -> List[Dict]:
        """
        Generate synthetic smart contract data for training
        """
        logger.info(f"Generating {num_samples} synthetic contract samples...")
        
        contracts = []
        
        # Template contracts with known vulnerabilities
        templates = {
            'reentrancy': '''
                contract ReentrancyVulnerable {
                    mapping(address => uint) public balances;
                    
                    function withdraw() public {
                        uint amount = balances[msg.sender];
                        msg.sender.call{value: amount}("");
                        balances[msg.sender] = 0;
                    }
                }
            ''',
            'integer_overflow': '''
                contract OverflowVulnerable {
                    uint public total;
                    
                    function add(uint value) public {
                        total += value;
                    }
                }
            ''',
            'access_control': '''
                contract AccessVulnerable {
                    address public owner;
                    
                    function withdraw() public {
                        payable(msg.sender).transfer(address(this).balance);
                    }
                }
            '''
        }
        
        for i in range(num_samples):
            # Randomly select vulnerability type
            vuln_type = np.random.choice(list(templates.keys()) + ['safe'])
            
            if vuln_type == 'safe':
                # Generate safe contract
                contract_code = '''
                    contract SafeContract {
                        address public owner;
                        mapping(address => uint) public balances;
                        
                        modifier onlyOwner() {
                            require(msg.sender == owner, "Not owner");
                            _;
                        }
                        
                        function withdraw() public onlyOwner {
                            require(balances[msg.sender] > 0, "No balance");
                            uint amount = balances[msg.sender];
                            balances[msg.sender] = 0;
                            payable(msg.sender).transfer(amount);
                        }
                    }
                '''
                vulnerabilities = {vuln: False for vuln in self.VULNERABILITY_TYPES[:5]}
            else:
                contract_code = templates[vuln_type]
                vulnerabilities = {vuln: vuln == vuln_type for vuln in self.VULNERABILITY_TYPES[:5]}
            
            # Add noise and variations
            contract_code += f"\n// Contract {i}\n"
            
            contracts.append({
                'code': contract_code,
                'vulnerabilities': vulnerabilities,
                'risk_score': np.random.uniform(0.1, 0.9) if vuln_type != 'safe' else np.random.uniform(0.0, 0.3)
            })
        
        return contracts
    
    def train_model(self, epochs: int = 50, batch_size: int = 32):
        """
        Train the neural contract analyzer
        """
        logger.info("Starting neural contract analyzer training...")
        
        # Generate training data
        contracts = self.generate_synthetic_contracts(5000)
        
        # Preprocess contracts
        processed_data = []
        for contract in contracts:
            processed = self.preprocess_contract(contract['code'])
            processed_data.append({
                'features': processed['vulnerability_indicators'],
                'vulnerabilities': contract['vulnerabilities'],
                'risk_score': contract['risk_score']
            })
        
        # Convert to tensors (simplified for demonstration)
        X = np.array([[data['features'][vuln] for vuln in self.VULNERABILITY_TYPES[:5]] 
                      for data in processed_data])
        
        y_vulnerabilities = {}
        for vuln in self.VULNERABILITY_TYPES[:5]:
            y_vulnerabilities[vuln] = np.array([data['vulnerabilities'][vuln] 
                                               for data in processed_data])
        
        y_risk = np.array([data['risk_score'] for data in processed_data])
        
        # Simple neural network for demonstration
        self.model = nn.Sequential(
            nn.Linear(5, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, len(self.VULNERABILITY_TYPES[:5]) + 1)  # +1 for risk score
        ).to(self.device)
        
        # Training setup
        criterion = nn.BCEWithLogitsLoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        
        X_tensor = torch.FloatTensor(X).to(self.device)
        
        # Combine all targets
        y_combined = np.column_stack([
            y_vulnerabilities[vuln].astype(float) for vuln in self.VULNERABILITY_TYPES[:5]
        ] + [y_risk])
        y_tensor = torch.FloatTensor(y_combined).to(self.device)
        
        # Training loop
        self.model.train()
        for epoch in range(epochs):
            optimizer.zero_grad()
            
            outputs = self.model(X_tensor)
            loss = criterion(outputs, y_tensor)
            
            loss.backward()
            optimizer.step()
            
            if epoch % 10 == 0:
                logger.info(f"Epoch {epoch}/{epochs} - Loss: {loss.item():.4f}")
        
        self.is_trained = True
        self.save_model()
        logger.info("Neural contract analyzer training completed!")
    
    def analyze_contract(self, contract_code: str) -> Dict:
        """
        Analyze a smart contract for vulnerabilities
        """
        if not self.is_trained and self.model is None:
            self.load_model()
        
        # Preprocess contract
        processed = self.preprocess_contract(contract_code)
        
        if self.model is None:
            # Fallback to pattern-based analysis
            return self._pattern_based_analysis(processed)
        
        # Neural network analysis
        features = np.array([[processed['vulnerability_indicators'][vuln] 
                             for vuln in self.VULNERABILITY_TYPES[:5]]])
        features_tensor = torch.FloatTensor(features).to(self.device)
        
        self.model.eval()
        with torch.no_grad():
            outputs = self.model(features_tensor)
            predictions = torch.sigmoid(outputs).cpu().numpy()[0]
        
        # Parse predictions
        vulnerabilities = []
        for i, vuln_type in enumerate(self.VULNERABILITY_TYPES[:5]):
            if predictions[i] > 0.5:
                vulnerabilities.append({
                    'type': vuln_type,
                    'severity': 'high' if predictions[i] > 0.8 else 'medium' if predictions[i] > 0.6 else 'low',
                    'confidence': float(predictions[i]),
                    'description': self.VULNERABILITY_DESCRIPTIONS.get(vuln_type, 'Unknown vulnerability'),
                    'line_numbers': self._find_vulnerability_lines(contract_code, vuln_type)
                })
        
        risk_score = float(predictions[-1])
        
        # Generate recommendations
        recommendations = self._generate_recommendations(vulnerabilities)
        
        return {
            'contract_hash': hashlib.md5(contract_code.encode()).hexdigest(),
            'analysis_timestamp': datetime.utcnow().isoformat(),
            'vulnerabilities': vulnerabilities,
            'risk_score': risk_score,
            'risk_level': self._get_risk_level(risk_score),
            'recommendations': recommendations,
            'contract_stats': processed['features'],
            'analyzer_version': '2.0.0'
        }
    
    def _pattern_based_analysis(self, processed: Dict) -> Dict:
        """
        Fallback pattern-based analysis when neural model is not available
        """
        vulnerabilities = []
        
        for vuln_type, score in processed['vulnerability_indicators'].items():
            if score > 0.3:  # Threshold for detection
                vulnerabilities.append({
                    'type': vuln_type,
                    'severity': 'high' if score > 0.7 else 'medium' if score > 0.5 else 'low',
                    'confidence': float(score),
                    'description': self.VULNERABILITY_DESCRIPTIONS.get(vuln_type, 'Unknown vulnerability'),
                    'line_numbers': []
                })
        
        risk_score = np.mean(list(processed['vulnerability_indicators'].values()))
        
        return {
            'contract_hash': hashlib.md5(processed['cleaned_code'].encode()).hexdigest(),
            'analysis_timestamp': datetime.utcnow().isoformat(),
            'vulnerabilities': vulnerabilities,
            'risk_score': float(risk_score),
            'risk_level': self._get_risk_level(risk_score),
            'recommendations': self._generate_recommendations(vulnerabilities),
            'contract_stats': processed['features'],
            'analyzer_version': '2.0.0-fallback'
        }
    
    def _find_vulnerability_lines(self, contract_code: str, vuln_type: str) -> List[int]:
        """
        Find line numbers where vulnerabilities might exist
        """
        lines = contract_code.split('\n')
        vulnerable_lines = []
        
        patterns = self.vulnerability_patterns.get(vuln_type, [])
        for i, line in enumerate(lines, 1):
            for pattern in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    vulnerable_lines.append(i)
                    break
        
        return vulnerable_lines
    
    def _get_risk_level(self, risk_score: float) -> str:
        """
        Convert risk score to risk level
        """
        if risk_score >= 0.8:
            return 'critical'
        elif risk_score >= 0.6:
            return 'high'
        elif risk_score >= 0.4:
            return 'medium'
        elif risk_score >= 0.2:
            return 'low'
        else:
            return 'minimal'
    
    def _generate_recommendations(self, vulnerabilities: List[Dict]) -> List[str]:
        """
        Generate security recommendations based on detected vulnerabilities
        """
        recommendations = []
        
        vuln_types = [v['type'] for v in vulnerabilities]
        
        if 'reentrancy' in vuln_types:
            recommendations.append("Implement checks-effects-interactions pattern")
            recommendations.append("Use ReentrancyGuard from OpenZeppelin")
        
        if 'integer_overflow' in vuln_types:
            recommendations.append("Use SafeMath library for arithmetic operations")
            recommendations.append("Upgrade to Solidity 0.8+ for built-in overflow protection")
        
        if 'access_control' in vuln_types:
            recommendations.append("Implement proper access control modifiers")
            recommendations.append("Use OpenZeppelin's AccessControl contract")
        
        if 'timestamp_dependency' in vuln_types:
            recommendations.append("Avoid using block.timestamp for critical logic")
            recommendations.append("Use block numbers or external oracles for timing")
        
        if 'unchecked_calls' in vuln_types:
            recommendations.append("Always check return values of external calls")
            recommendations.append("Use try-catch for external contract calls")
        
        if not recommendations:
            recommendations.append("Contract appears secure, but consider professional audit")
        
        return recommendations
    
    def save_model(self):
        """
        Save the trained model
        """
        import os
        os.makedirs("models", exist_ok=True)
        
        if self.model is not None:
            torch.save({
                'model_state_dict': self.model.state_dict(),
                'vulnerability_types': self.VULNERABILITY_TYPES,
                'is_trained': self.is_trained
            }, self.model_path)
            
            logger.info(f"Neural analyzer model saved to {self.model_path}")
    
    def load_model(self):
        """
        Load a pre-trained model
        """
        try:
            checkpoint = torch.load(self.model_path, map_location=self.device)
            
            # Recreate model architecture
            self.model = nn.Sequential(
                nn.Linear(5, 64),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(64, 128),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(128, 64),
                nn.ReLU(),
                nn.Linear(64, 6)  # 5 vulnerabilities + 1 risk score
            ).to(self.device)
            
            self.model.load_state_dict(checkpoint['model_state_dict'])
            self.is_trained = checkpoint['is_trained']
            
            logger.info(f"Neural analyzer model loaded from {self.model_path}")
            
        except FileNotFoundError:
            logger.warning(f"Model file not found at {self.model_path}. Training new model...")
            self.train_model()
        except Exception as e:
            logger.error(f"Error loading neural analyzer model: {e}")
            self.model = None 