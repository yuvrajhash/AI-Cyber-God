"""
📊 QUANTUM-AI CYBER GOD - REAL-TIME ANALYTICS
Advanced analytics and visualization service for blockchain security
"""

import asyncio
import json
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from collections import defaultdict, deque
import statistics
import numpy as np
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class ThreatLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class AnalyticsMetric:
    """Analytics metric data structure"""
    metric_id: str
    name: str
    value: float
    unit: str
    timestamp: datetime
    trend: str  # "up", "down", "stable"
    change_percent: float
    
    def to_dict(self):
        return {
            **asdict(self),
            'timestamp': self.timestamp.isoformat()
        }

@dataclass
class ThreatAlert:
    """Threat alert data structure"""
    alert_id: str
    threat_type: str
    severity: ThreatLevel
    chain_id: int
    affected_addresses: List[str]
    description: str
    timestamp: datetime
    confidence: float
    mitigation_steps: List[str]
    
    def to_dict(self):
        return {
            **asdict(self),
            'severity': self.severity.value,
            'timestamp': self.timestamp.isoformat()
        }

class RealTimeAnalytics:
    """Advanced real-time analytics engine"""
    
    def __init__(self):
        self.metrics_history = defaultdict(lambda: deque(maxlen=1000))
        self.threat_alerts = deque(maxlen=500)
        self.chain_stats = defaultdict(dict)
        self.active_threats = {}
        self.analytics_active = False
        self.update_interval = 5  # seconds
        
        # Initialize metric tracking
        self.tracked_metrics = {
            "total_transactions": 0,
            "high_risk_transactions": 0,
            "failed_transactions": 0,
            "contract_deployments": 0,
            "mev_opportunities": 0,
            "gas_price_avg": 0.0,
            "block_time_avg": 0.0,
            "network_congestion": 0.0,
            "threat_score": 0.0,
            "defense_effectiveness": 95.0
        }
        
        # Time series data for charts
        self.time_series_data = {
            "transaction_volume": deque(maxlen=100),
            "threat_levels": deque(maxlen=100),
            "gas_prices": deque(maxlen=100),
            "block_times": deque(maxlen=100),
            "risk_scores": deque(maxlen=100)
        }
        
        # Pattern detection
        self.attack_patterns = {
            "flash_loan_attacks": [],
            "reentrancy_attempts": [],
            "front_running": [],
            "sandwich_attacks": [],
            "rugpulls": []
        }
    
    async def start_analytics(self):
        """Start real-time analytics processing"""
        self.analytics_active = True
        logger.info("Starting real-time analytics engine...")
        
        # Start analytics tasks
        tasks = [
            asyncio.create_task(self._update_metrics()),
            asyncio.create_task(self._detect_patterns()),
            asyncio.create_task(self._generate_insights()),
            asyncio.create_task(self._monitor_network_health())
        ]
        
        await asyncio.gather(*tasks)
    
    async def _update_metrics(self):
        """Update real-time metrics"""
        while self.analytics_active:
            try:
                current_time = datetime.now()
                
                # Update core metrics
                for metric_name, value in self.tracked_metrics.items():
                    # Add some realistic variation
                    if metric_name == "defense_effectiveness":
                        variation = np.random.normal(0, 0.5)
                        new_value = max(85.0, min(99.9, value + variation))
                    elif metric_name == "threat_score":
                        variation = np.random.normal(0, 2.0)
                        new_value = max(0.0, min(100.0, value + variation))
                    elif metric_name == "gas_price_avg":
                        variation = np.random.normal(0, 5.0)
                        new_value = max(10.0, value + variation)
                    else:
                        variation = np.random.normal(0, 1.0)
                        new_value = max(0, value + variation)
                    
                    self.tracked_metrics[metric_name] = new_value
                    
                    # Store in history
                    self.metrics_history[metric_name].append({
                        "timestamp": current_time,
                        "value": new_value
                    })
                
                # Update time series data
                self._update_time_series(current_time)
                
                await asyncio.sleep(self.update_interval)
                
            except Exception as e:
                logger.error(f"Error updating metrics: {e}")
                await asyncio.sleep(5)
    
    def _update_time_series(self, timestamp: datetime):
        """Update time series data for charts"""
        # Transaction volume (simulated)
        volume = max(0, np.random.poisson(50) + np.random.normal(0, 10))
        self.time_series_data["transaction_volume"].append({
            "timestamp": timestamp.isoformat(),
            "value": volume
        })
        
        # Threat levels
        threat_level = max(0, min(100, self.tracked_metrics["threat_score"]))
        self.time_series_data["threat_levels"].append({
            "timestamp": timestamp.isoformat(),
            "value": threat_level
        })
        
        # Gas prices
        gas_price = self.tracked_metrics["gas_price_avg"]
        self.time_series_data["gas_prices"].append({
            "timestamp": timestamp.isoformat(),
            "value": gas_price
        })
        
        # Block times (simulated)
        block_time = max(1, np.random.normal(12, 2))  # ~12 second average
        self.time_series_data["block_times"].append({
            "timestamp": timestamp.isoformat(),
            "value": block_time
        })
        
        # Risk scores
        risk_score = np.random.beta(2, 5) * 100  # Skewed towards lower risk
        self.time_series_data["risk_scores"].append({
            "timestamp": timestamp.isoformat(),
            "value": risk_score
        })
    
    async def _detect_patterns(self):
        """Detect attack patterns and anomalies"""
        while self.analytics_active:
            try:
                current_time = datetime.now()
                
                # Simulate pattern detection
                if np.random.random() < 0.1:  # 10% chance of detecting something
                    await self._generate_threat_alert(current_time)
                
                # Check for coordinated attacks
                await self._check_coordinated_attacks()
                
                # Analyze transaction patterns
                await self._analyze_transaction_patterns()
                
                await asyncio.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                logger.error(f"Error in pattern detection: {e}")
                await asyncio.sleep(5)
    
    async def _generate_threat_alert(self, timestamp: datetime):
        """Generate a threat alert"""
        threat_types = [
            "Flash Loan Attack",
            "Reentrancy Attempt",
            "Front Running",
            "Sandwich Attack",
            "Suspicious Contract",
            "MEV Bot Activity",
            "Phishing Contract",
            "Rugpull Indicator"
        ]
        
        threat_type = np.random.choice(threat_types)
        severity = np.random.choice(list(ThreatLevel), p=[0.4, 0.3, 0.2, 0.1])
        
        alert = ThreatAlert(
            alert_id=f"alert_{int(timestamp.timestamp())}",
            threat_type=threat_type,
            severity=severity,
            chain_id=np.random.choice([1, 137, 56]),
            affected_addresses=[f"0x{''.join(np.random.choice(list('0123456789abcdef'), 40))}"],
            description=f"Detected {threat_type.lower()} with {severity.value} severity",
            timestamp=timestamp,
            confidence=np.random.uniform(0.7, 0.99),
            mitigation_steps=self._get_mitigation_steps(threat_type)
        )
        
        self.threat_alerts.append(alert)
        logger.warning(f"Threat alert generated: {threat_type} ({severity.value})")
    
    def _get_mitigation_steps(self, threat_type: str) -> List[str]:
        """Get mitigation steps for threat type"""
        mitigation_map = {
            "Flash Loan Attack": [
                "Monitor flash loan protocols",
                "Implement price oracle checks",
                "Add time delays for large transactions"
            ],
            "Reentrancy Attempt": [
                "Use reentrancy guards",
                "Follow checks-effects-interactions pattern",
                "Audit contract code"
            ],
            "Front Running": [
                "Use commit-reveal schemes",
                "Implement private mempools",
                "Add randomization delays"
            ],
            "Sandwich Attack": [
                "Monitor DEX activity",
                "Use MEV protection services",
                "Implement slippage protection"
            ]
        }
        
        return mitigation_map.get(threat_type, ["Monitor situation", "Review security measures"])
    
    async def _check_coordinated_attacks(self):
        """Check for coordinated attack patterns"""
        # Simulate coordinated attack detection
        if len(self.threat_alerts) >= 3:
            recent_alerts = list(self.threat_alerts)[-3:]
            time_window = timedelta(minutes=5)
            
            if all(alert.timestamp > datetime.now() - time_window for alert in recent_alerts):
                logger.critical("COORDINATED ATTACK DETECTED - Multiple threats in short timeframe")
                self.tracked_metrics["threat_score"] = min(100, self.tracked_metrics["threat_score"] + 20)
    
    async def _analyze_transaction_patterns(self):
        """Analyze transaction patterns for anomalies"""
        # Simulate transaction pattern analysis
        patterns = {
            "unusual_gas_prices": np.random.random() < 0.05,
            "high_value_transfers": np.random.random() < 0.03,
            "contract_creation_spike": np.random.random() < 0.02,
            "failed_transaction_cluster": np.random.random() < 0.04
        }
        
        for pattern, detected in patterns.items():
            if detected:
                logger.info(f"Pattern detected: {pattern}")
    
    async def _generate_insights(self):
        """Generate AI-powered insights"""
        while self.analytics_active:
            try:
                # Generate insights based on current data
                insights = await self._analyze_trends()
                
                # Update defense effectiveness based on threat levels
                threat_score = self.tracked_metrics["threat_score"]
                if threat_score > 80:
                    self.tracked_metrics["defense_effectiveness"] = max(70, 
                        self.tracked_metrics["defense_effectiveness"] - 1)
                elif threat_score < 20:
                    self.tracked_metrics["defense_effectiveness"] = min(99, 
                        self.tracked_metrics["defense_effectiveness"] + 0.5)
                
                await asyncio.sleep(30)  # Generate insights every 30 seconds
                
            except Exception as e:
                logger.error(f"Error generating insights: {e}")
                await asyncio.sleep(10)
    
    async def _analyze_trends(self) -> List[str]:
        """Analyze trends and generate insights"""
        insights = []
        
        # Analyze threat score trend
        if len(self.metrics_history["threat_score"]) >= 10:
            recent_scores = [item["value"] for item in list(self.metrics_history["threat_score"])[-10:]]
            trend = np.polyfit(range(len(recent_scores)), recent_scores, 1)[0]
            
            if trend > 2:
                insights.append("Threat levels are increasing - enhanced monitoring recommended")
            elif trend < -2:
                insights.append("Threat levels are decreasing - security measures are effective")
        
        # Analyze gas price trends
        if len(self.metrics_history["gas_price_avg"]) >= 10:
            recent_gas = [item["value"] for item in list(self.metrics_history["gas_price_avg"])[-10:]]
            if statistics.mean(recent_gas) > 100:
                insights.append("High gas prices detected - potential network congestion")
        
        return insights
    
    async def _monitor_network_health(self):
        """Monitor overall network health"""
        while self.analytics_active:
            try:
                # Calculate network congestion
                gas_price = self.tracked_metrics["gas_price_avg"]
                congestion = min(100, max(0, (gas_price - 20) / 80 * 100))
                self.tracked_metrics["network_congestion"] = congestion
                
                # Update block time average
                if self.time_series_data["block_times"]:
                    recent_times = [item["value"] for item in list(self.time_series_data["block_times"])[-10:]]
                    self.tracked_metrics["block_time_avg"] = statistics.mean(recent_times)
                
                await asyncio.sleep(15)
                
            except Exception as e:
                logger.error(f"Error monitoring network health: {e}")
                await asyncio.sleep(10)
    
    def process_blockchain_event(self, event_data: Dict[str, Any]):
        """Process incoming blockchain event"""
        try:
            # Update relevant metrics
            self.tracked_metrics["total_transactions"] += 1
            
            if event_data.get("risk_score", 0) > 0.7:
                self.tracked_metrics["high_risk_transactions"] += 1
            
            if event_data.get("event_type") == "FAILED_TRANSACTION":
                self.tracked_metrics["failed_transactions"] += 1
            elif event_data.get("event_type") == "CONTRACT_DEPLOYMENT":
                self.tracked_metrics["contract_deployments"] += 1
            elif event_data.get("event_type") == "MEV_OPPORTUNITY":
                self.tracked_metrics["mev_opportunities"] += 1
            
            # Update threat score based on event
            risk_impact = event_data.get("risk_score", 0) * 10
            self.tracked_metrics["threat_score"] = min(100, 
                self.tracked_metrics["threat_score"] + risk_impact * 0.1)
            
        except Exception as e:
            logger.error(f"Error processing blockchain event: {e}")
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive dashboard data"""
        current_time = datetime.now()
        
        # Calculate trends
        metrics_with_trends = {}
        for metric_name, value in self.tracked_metrics.items():
            trend = self._calculate_trend(metric_name)
            metrics_with_trends[metric_name] = {
                "value": value,
                "trend": trend["direction"],
                "change_percent": trend["change_percent"]
            }
        
        return {
            "timestamp": current_time.isoformat(),
            "metrics": metrics_with_trends,
            "time_series": dict(self.time_series_data),
            "recent_alerts": [alert.to_dict() for alert in list(self.threat_alerts)[-10:]],
            "chain_stats": dict(self.chain_stats),
            "network_health": {
                "overall_score": self._calculate_network_health_score(),
                "congestion_level": self.tracked_metrics["network_congestion"],
                "average_block_time": self.tracked_metrics["block_time_avg"],
                "defense_effectiveness": self.tracked_metrics["defense_effectiveness"]
            },
            "threat_summary": {
                "current_threat_level": self._get_threat_level(),
                "active_threats": len([a for a in self.threat_alerts if a.timestamp > current_time - timedelta(hours=1)]),
                "critical_alerts": len([a for a in self.threat_alerts if a.severity == ThreatLevel.CRITICAL]),
                "mitigation_success_rate": self.tracked_metrics["defense_effectiveness"]
            }
        }
    
    def _calculate_trend(self, metric_name: str) -> Dict[str, Any]:
        """Calculate trend for a metric"""
        if metric_name not in self.metrics_history or len(self.metrics_history[metric_name]) < 2:
            return {"direction": "stable", "change_percent": 0.0}
        
        history = list(self.metrics_history[metric_name])
        if len(history) >= 10:
            recent_values = [item["value"] for item in history[-10:]]
            older_values = [item["value"] for item in history[-20:-10]] if len(history) >= 20 else recent_values
        else:
            recent_values = [item["value"] for item in history[-len(history)//2:]]
            older_values = [item["value"] for item in history[:len(history)//2]]
        
        if not older_values:
            return {"direction": "stable", "change_percent": 0.0}
        
        recent_avg = statistics.mean(recent_values)
        older_avg = statistics.mean(older_values)
        
        if older_avg == 0:
            change_percent = 0.0
        else:
            change_percent = ((recent_avg - older_avg) / older_avg) * 100
        
        if abs(change_percent) < 1:
            direction = "stable"
        elif change_percent > 0:
            direction = "up"
        else:
            direction = "down"
        
        return {"direction": direction, "change_percent": change_percent}
    
    def _calculate_network_health_score(self) -> float:
        """Calculate overall network health score"""
        factors = {
            "defense_effectiveness": self.tracked_metrics["defense_effectiveness"] / 100,
            "low_threat_score": max(0, (100 - self.tracked_metrics["threat_score"]) / 100),
            "low_congestion": max(0, (100 - self.tracked_metrics["network_congestion"]) / 100),
            "stable_block_times": 1.0 if 10 <= self.tracked_metrics["block_time_avg"] <= 15 else 0.7
        }
        
        weights = {
            "defense_effectiveness": 0.4,
            "low_threat_score": 0.3,
            "low_congestion": 0.2,
            "stable_block_times": 0.1
        }
        
        score = sum(factors[key] * weights[key] for key in factors.keys())
        return round(score * 100, 1)
    
    def _get_threat_level(self) -> str:
        """Get current threat level"""
        threat_score = self.tracked_metrics["threat_score"]
        
        if threat_score >= 80:
            return "CRITICAL"
        elif threat_score >= 60:
            return "HIGH"
        elif threat_score >= 30:
            return "MEDIUM"
        else:
            return "LOW"
    
    def get_historical_data(self, metric_name: str, hours: int = 24) -> List[Dict[str, Any]]:
        """Get historical data for a specific metric"""
        if metric_name not in self.metrics_history:
            return []
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        history = list(self.metrics_history[metric_name])
        
        return [
            item for item in history 
            if item["timestamp"] > cutoff_time
        ]
    
    async def stop_analytics(self):
        """Stop analytics processing"""
        self.analytics_active = False
        logger.info("Real-time analytics stopped")

# Global analytics instance
realtime_analytics = RealTimeAnalytics() 