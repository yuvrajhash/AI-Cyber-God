"""
🧠 Custom Threat Models Service
Handles industry-specific AI threat detection models for enterprise tenants
"""

import asyncio
import json
import logging
import uuid
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from enum import Enum

logger = logging.getLogger(__name__)

class ThreatModelType(str, Enum):
    FINANCIAL_SERVICES = "financial_services"
    HEALTHCARE = "healthcare"
    GOVERNMENT = "government"
    MANUFACTURING = "manufacturing"
    RETAIL = "retail"
    CUSTOM = "custom"

class ComplianceFramework(str, Enum):
    SOC2 = "soc2"
    ISO27001 = "iso27001"
    GDPR = "gdpr"
    HIPAA = "hipaa"
    PCI_DSS = "pci_dss"
    NIST = "nist"

class CustomThreatModels:
    def __init__(self):
        self.is_active = False
        self.tenant_models: Dict[str, List[Dict]] = {}
        self.model_performance: Dict[str, Dict] = {}
        self.industry_templates = {
            ThreatModelType.FINANCIAL_SERVICES: {
                "threat_vectors": [
                    "payment_fraud", "account_takeover", "insider_trading",
                    "money_laundering", "credit_card_fraud", "wire_fraud"
                ],
                "compliance_frameworks": [ComplianceFramework.PCI_DSS, ComplianceFramework.SOC2],
                "sensitivity_level": 0.9,
                "custom_rules": {
                    "transaction_threshold": 10000,
                    "velocity_checks": True,
                    "geo_blocking": True
                }
            },
            ThreatModelType.HEALTHCARE: {
                "threat_vectors": [
                    "phi_breach", "ransomware", "medical_device_hack",
                    "insider_threat", "data_exfiltration", "identity_theft"
                ],
                "compliance_frameworks": [ComplianceFramework.HIPAA, ComplianceFramework.SOC2],
                "sensitivity_level": 0.95,
                "custom_rules": {
                    "phi_detection": True,
                    "device_monitoring": True,
                    "access_controls": "strict"
                }
            },
            ThreatModelType.GOVERNMENT: {
                "threat_vectors": [
                    "nation_state_attacks", "espionage", "data_breach",
                    "supply_chain_attack", "insider_threat", "cyber_warfare"
                ],
                "compliance_frameworks": [ComplianceFramework.NIST, ComplianceFramework.ISO27001],
                "sensitivity_level": 0.98,
                "custom_rules": {
                    "classification_levels": True,
                    "zero_trust": True,
                    "continuous_monitoring": True
                }
            },
            ThreatModelType.MANUFACTURING: {
                "threat_vectors": [
                    "iot_compromise", "scada_attack", "supply_chain_attack",
                    "intellectual_property_theft", "operational_disruption"
                ],
                "compliance_frameworks": [ComplianceFramework.ISO27001, ComplianceFramework.NIST],
                "sensitivity_level": 0.85,
                "custom_rules": {
                    "ot_monitoring": True,
                    "asset_tracking": True,
                    "anomaly_detection": True
                }
            },
            ThreatModelType.RETAIL: {
                "threat_vectors": [
                    "pos_malware", "customer_data_breach", "payment_fraud",
                    "inventory_theft", "supply_chain_attack"
                ],
                "compliance_frameworks": [ComplianceFramework.PCI_DSS, ComplianceFramework.GDPR],
                "sensitivity_level": 0.8,
                "custom_rules": {
                    "pos_monitoring": True,
                    "customer_data_protection": True,
                    "fraud_detection": True
                }
            }
        }

    async def initialize(self):
        """Initialize the custom threat models service"""
        try:
            logger.info("🧠 Initializing Custom Threat Models...")
            
            # Initialize demo models for testing
            await self._create_demo_models()
            
            self.is_active = True
            logger.info("✅ Custom Threat Models initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Error initializing Custom Threat Models: {e}")
            raise

    async def _create_demo_models(self):
        """Create demo threat models for testing"""
        demo_models = [
            {
                "tenant_id": "demo-tenant-1",
                "model_name": "FinTech Security Model",
                "model_type": ThreatModelType.FINANCIAL_SERVICES,
                "industry_focus": "Digital Banking",
                "threat_vectors": ["payment_fraud", "account_takeover", "api_abuse"],
                "sensitivity_level": 0.9,
                "compliance_mapping": [ComplianceFramework.PCI_DSS, ComplianceFramework.SOC2]
            },
            {
                "tenant_id": "demo-tenant-2",
                "model_name": "Healthcare Threat Detection",
                "model_type": ThreatModelType.HEALTHCARE,
                "industry_focus": "Electronic Health Records",
                "threat_vectors": ["phi_breach", "ransomware", "insider_threat"],
                "sensitivity_level": 0.95,
                "compliance_mapping": [ComplianceFramework.HIPAA]
            }
        ]
        
        for model_data in demo_models:
            await self.create_model(**model_data)

    async def create_model(
        self,
        tenant_id: str,
        model_name: str,
        model_type: ThreatModelType,
        industry_focus: str,
        threat_vectors: List[str],
        sensitivity_level: float,
        custom_rules: Dict[str, Any] = None,
        compliance_mapping: List[ComplianceFramework] = None
    ) -> Dict:
        """Create a new custom threat model"""
        try:
            model_id = str(uuid.uuid4())
            
            # Get industry template if available
            template = self.industry_templates.get(model_type, {})
            
            # Merge custom rules with template
            if custom_rules is None:
                custom_rules = template.get("custom_rules", {})
            else:
                custom_rules = {**template.get("custom_rules", {}), **custom_rules}
            
            # Set compliance mapping
            if compliance_mapping is None:
                compliance_mapping = template.get("compliance_frameworks", [])
            
            model = {
                "model_id": model_id,
                "tenant_id": tenant_id,
                "model_name": model_name,
                "model_type": model_type,
                "industry_focus": industry_focus,
                "threat_vectors": threat_vectors,
                "sensitivity_level": sensitivity_level,
                "custom_rules": custom_rules,
                "compliance_mapping": compliance_mapping,
                "created_at": datetime.now().isoformat(),
                "status": "training",
                "version": "1.0.0",
                "training_progress": 0,
                "accuracy": 0.0,
                "false_positive_rate": 0.0,
                "last_updated": datetime.now().isoformat(),
                "deployment_status": "pending"
            }
            
            # Initialize tenant models list if needed
            if tenant_id not in self.tenant_models:
                self.tenant_models[tenant_id] = []
            
            self.tenant_models[tenant_id].append(model)
            
            # Initialize performance tracking
            self.model_performance[model_id] = {
                "threats_detected": 0,
                "false_positives": 0,
                "true_positives": 0,
                "response_time_avg": 0.0,
                "accuracy_trend": [],
                "deployment_health": "healthy"
            }
            
            # Start model training simulation
            asyncio.create_task(self._simulate_model_training(model_id))
            
            logger.info(f"✅ Created custom threat model: {model_name} ({model_id})")
            return model
            
        except Exception as e:
            logger.error(f"❌ Error creating custom threat model: {e}")
            raise

    async def _simulate_model_training(self, model_id: str):
        """Simulate AI model training process"""
        try:
            # Find the model
            model = None
            for tenant_models in self.tenant_models.values():
                for m in tenant_models:
                    if m["model_id"] == model_id:
                        model = m
                        break
                if model:
                    break
            
            if not model:
                return
            
            # Simulate training progress
            training_steps = 20
            for step in range(training_steps + 1):
                progress = (step / training_steps) * 100
                model["training_progress"] = progress
                
                # Simulate improving accuracy
                base_accuracy = 0.7 + (model["sensitivity_level"] * 0.2)
                model["accuracy"] = min(0.99, base_accuracy + (progress / 100) * 0.25)
                model["false_positive_rate"] = max(0.01, 0.1 - (progress / 100) * 0.08)
                
                if progress == 100:
                    model["status"] = "trained"
                    model["deployment_status"] = "ready"
                    logger.info(f"✅ Model training completed: {model['model_name']}")
                
                await asyncio.sleep(2)  # 2 seconds per step = 40 seconds total
                
        except Exception as e:
            logger.error(f"❌ Error in model training simulation: {e}")

    async def get_tenant_models(self, tenant_id: str) -> List[Dict]:
        """Get all threat models for a tenant"""
        try:
            return self.tenant_models.get(tenant_id, [])
        except Exception as e:
            logger.error(f"❌ Error getting tenant models: {e}")
            return []

    async def get_models_performance(self, tenant_id: str) -> Dict:
        """Get performance metrics for tenant's models"""
        try:
            tenant_models = self.tenant_models.get(tenant_id, [])
            performance_summary = {
                "total_models": len(tenant_models),
                "active_models": sum(1 for m in tenant_models if m["status"] == "deployed"),
                "average_accuracy": 0.0,
                "total_threats_detected": 0,
                "models_performance": {}
            }
            
            if tenant_models:
                total_accuracy = sum(m["accuracy"] for m in tenant_models)
                performance_summary["average_accuracy"] = total_accuracy / len(tenant_models)
                
                for model in tenant_models:
                    model_id = model["model_id"]
                    if model_id in self.model_performance:
                        perf = self.model_performance[model_id]
                        performance_summary["total_threats_detected"] += perf["threats_detected"]
                        performance_summary["models_performance"][model_id] = {
                            "model_name": model["model_name"],
                            "accuracy": model["accuracy"],
                            "threats_detected": perf["threats_detected"],
                            "false_positive_rate": model["false_positive_rate"],
                            "status": model["status"]
                        }
            
            return performance_summary
            
        except Exception as e:
            logger.error(f"❌ Error getting models performance: {e}")
            return {}

    async def get_threat_summary(self, tenant_id: str) -> Dict:
        """Get threat detection summary for a tenant"""
        try:
            tenant_models = self.tenant_models.get(tenant_id, [])
            
            threat_summary = {
                "total_threats_detected": 0,
                "threats_by_category": {},
                "threat_trends": [],
                "model_effectiveness": {},
                "recent_detections": []
            }
            
            # Simulate threat detection data
            threat_categories = [
                "malware", "phishing", "insider_threat", "data_breach",
                "fraud", "ransomware", "ddos", "supply_chain"
            ]
            
            for category in threat_categories:
                count = random.randint(1, 15)
                threat_summary["threats_by_category"][category] = count
                threat_summary["total_threats_detected"] += count
            
            # Generate recent detections
            for i in range(5):
                detection_time = datetime.now() - timedelta(minutes=random.randint(5, 120))
                threat_summary["recent_detections"].append({
                    "timestamp": detection_time.isoformat(),
                    "threat_type": random.choice(threat_categories),
                    "severity": random.choice(["low", "medium", "high", "critical"]),
                    "model_id": random.choice([m["model_id"] for m in tenant_models]) if tenant_models else "default",
                    "confidence": round(random.uniform(0.7, 0.99), 2)
                })
            
            return threat_summary
            
        except Exception as e:
            logger.error(f"❌ Error getting threat summary: {e}")
            return {}

    async def get_active_models_count(self) -> int:
        """Get total count of active threat models across all tenants"""
        try:
            total_active = 0
            for tenant_models in self.tenant_models.values():
                total_active += sum(1 for m in tenant_models if m["status"] in ["trained", "deployed"])
            return total_active
        except Exception as e:
            logger.error(f"❌ Error getting active models count: {e}")
            return 0

    async def update_model_performance(self, model_id: str, threats_detected: int = 1):
        """Update performance metrics for a model"""
        try:
            if model_id in self.model_performance:
                perf = self.model_performance[model_id]
                perf["threats_detected"] += threats_detected
                perf["true_positives"] += threats_detected
                
                # Update accuracy trend
                current_accuracy = random.uniform(0.85, 0.98)
                perf["accuracy_trend"].append({
                    "timestamp": datetime.now().isoformat(),
                    "accuracy": current_accuracy
                })
                
                # Keep only last 24 hours of data
                cutoff_time = datetime.now() - timedelta(hours=24)
                perf["accuracy_trend"] = [
                    entry for entry in perf["accuracy_trend"]
                    if datetime.fromisoformat(entry["timestamp"]) > cutoff_time
                ]
                
        except Exception as e:
            logger.error(f"❌ Error updating model performance: {e}")

    async def get_industry_templates(self) -> Dict:
        """Get available industry-specific threat model templates"""
        try:
            return {
                model_type.value: {
                    "name": model_type.value.replace("_", " ").title(),
                    "description": f"Pre-configured threat model for {model_type.value.replace('_', ' ')} industry",
                    "threat_vectors": template["threat_vectors"],
                    "compliance_frameworks": [f.value for f in template["compliance_frameworks"]],
                    "recommended_sensitivity": template["sensitivity_level"]
                }
                for model_type, template in self.industry_templates.items()
            }
        except Exception as e:
            logger.error(f"❌ Error getting industry templates: {e}")
            return {}

    async def deploy_model(self, model_id: str) -> Dict:
        """Deploy a trained model to production"""
        try:
            # Find the model
            model = None
            for tenant_models in self.tenant_models.values():
                for m in tenant_models:
                    if m["model_id"] == model_id:
                        model = m
                        break
                if model:
                    break
            
            if not model:
                raise ValueError(f"Model {model_id} not found")
            
            if model["status"] != "trained":
                raise ValueError(f"Model {model_id} is not ready for deployment")
            
            model["status"] = "deployed"
            model["deployment_status"] = "active"
            model["last_updated"] = datetime.now().isoformat()
            
            logger.info(f"✅ Deployed model: {model['model_name']} ({model_id})")
            
            return {
                "success": True,
                "model_id": model_id,
                "deployment_time": datetime.now().isoformat(),
                "status": "deployed"
            }
            
        except Exception as e:
            logger.error(f"❌ Error deploying model: {e}")
            raise

    async def shutdown(self):
        """Shutdown the custom threat models service"""
        try:
            logger.info("🛑 Shutting down Custom Threat Models...")
            self.is_active = False
            
        except Exception as e:
            logger.error(f"❌ Error shutting down Custom Threat Models: {e}")

# Global custom threat models instance
custom_threat_models = CustomThreatModels() 