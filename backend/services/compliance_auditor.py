"""
📋 Compliance Auditor Service
Enterprise compliance monitoring, reporting, and auditing
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

class ComplianceFramework(str, Enum):
    SOC2 = "soc2"
    ISO27001 = "iso27001"
    GDPR = "gdpr"
    HIPAA = "hipaa"
    PCI_DSS = "pci_dss"
    NIST = "nist"

class ComplianceStatus(str, Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    UNDER_REVIEW = "under_review"

class ComplianceAuditor:
    def __init__(self):
        self.is_active = False
        self.tenant_compliance: Dict[str, Dict] = {}
        self.compliance_reports: Dict[str, List[Dict]] = {}
        self.framework_requirements = {
            ComplianceFramework.SOC2: {
                "name": "SOC 2 Type II",
                "description": "Service Organization Control 2",
                "categories": [
                    "Security", "Availability", "Processing Integrity", 
                    "Confidentiality", "Privacy"
                ],
                "requirements": [
                    "Access Controls", "System Operations", "Change Management",
                    "Risk Mitigation", "Incident Response", "Monitoring",
                    "Logical Access", "System Boundaries", "Data Classification"
                ],
                "audit_frequency": "annual",
                "certification_validity": 365
            },
            ComplianceFramework.ISO27001: {
                "name": "ISO/IEC 27001",
                "description": "Information Security Management System",
                "categories": [
                    "Information Security Policies", "Organization of Information Security",
                    "Human Resource Security", "Asset Management", "Access Control"
                ],
                "requirements": [
                    "ISMS Policy", "Risk Assessment", "Security Controls",
                    "Incident Management", "Business Continuity", "Supplier Relationships"
                ],
                "audit_frequency": "annual",
                "certification_validity": 1095  # 3 years
            },
            ComplianceFramework.GDPR: {
                "name": "General Data Protection Regulation",
                "description": "EU Data Protection Regulation",
                "categories": [
                    "Lawfulness", "Data Minimization", "Accuracy",
                    "Storage Limitation", "Integrity", "Accountability"
                ],
                "requirements": [
                    "Consent Management", "Data Subject Rights", "Privacy by Design",
                    "Data Protection Impact Assessment", "Breach Notification", "DPO Appointment"
                ],
                "audit_frequency": "continuous",
                "certification_validity": 365
            },
            ComplianceFramework.HIPAA: {
                "name": "Health Insurance Portability and Accountability Act",
                "description": "Healthcare Data Protection",
                "categories": [
                    "Administrative Safeguards", "Physical Safeguards", "Technical Safeguards"
                ],
                "requirements": [
                    "Access Management", "Workforce Training", "Information Access Management",
                    "Audit Controls", "Integrity", "Person Authentication", "Transmission Security"
                ],
                "audit_frequency": "annual",
                "certification_validity": 365
            },
            ComplianceFramework.PCI_DSS: {
                "name": "Payment Card Industry Data Security Standard",
                "description": "Payment Card Data Protection",
                "categories": [
                    "Network Security", "Data Protection", "Vulnerability Management",
                    "Access Control", "Monitoring", "Information Security Policy"
                ],
                "requirements": [
                    "Firewall Configuration", "Default Passwords", "Cardholder Data Protection",
                    "Encrypted Transmission", "Antivirus Software", "Secure Systems"
                ],
                "audit_frequency": "annual",
                "certification_validity": 365
            },
            ComplianceFramework.NIST: {
                "name": "NIST Cybersecurity Framework",
                "description": "National Institute of Standards and Technology",
                "categories": [
                    "Identify", "Protect", "Detect", "Respond", "Recover"
                ],
                "requirements": [
                    "Asset Management", "Business Environment", "Governance",
                    "Risk Assessment", "Access Control", "Data Security", "Protective Technology"
                ],
                "audit_frequency": "annual",
                "certification_validity": 365
            }
        }

    async def initialize(self):
        """Initialize the compliance auditor"""
        try:
            logger.info("📋 Initializing Compliance Auditor...")
            
            # Initialize demo compliance data
            await self._initialize_demo_compliance()
            
            self.is_active = True
            logger.info("✅ Compliance Auditor initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Error initializing Compliance Auditor: {e}")
            raise

    async def _initialize_demo_compliance(self):
        """Initialize demo compliance data for testing"""
        demo_tenants = [
            {
                "tenant_id": "demo-tenant-1",
                "frameworks": [ComplianceFramework.SOC2, ComplianceFramework.ISO27001]
            },
            {
                "tenant_id": "demo-tenant-2", 
                "frameworks": [ComplianceFramework.HIPAA, ComplianceFramework.SOC2]
            },
            {
                "tenant_id": "demo-tenant-3",
                "frameworks": [ComplianceFramework.PCI_DSS, ComplianceFramework.GDPR]
            }
        ]
        
        for tenant in demo_tenants:
            await self._initialize_tenant_compliance(tenant["tenant_id"], tenant["frameworks"])

    async def _initialize_tenant_compliance(self, tenant_id: str, frameworks: List[ComplianceFramework]):
        """Initialize compliance tracking for a tenant"""
        try:
            self.tenant_compliance[tenant_id] = {
                "frameworks": {},
                "overall_score": 0.0,
                "last_assessment": datetime.now().isoformat(),
                "next_audit": (datetime.now() + timedelta(days=90)).isoformat()
            }
            
            self.compliance_reports[tenant_id] = []
            
            for framework in frameworks:
                await self._setup_framework_compliance(tenant_id, framework)
            
            # Calculate overall score
            await self._calculate_overall_score(tenant_id)
            
        except Exception as e:
            logger.error(f"❌ Error initializing tenant compliance: {e}")

    async def _setup_framework_compliance(self, tenant_id: str, framework: ComplianceFramework):
        """Setup compliance tracking for a specific framework"""
        try:
            framework_info = self.framework_requirements[framework]
            
            # Generate compliance status for each requirement
            requirements_status = {}
            total_score = 0
            
            for requirement in framework_info["requirements"]:
                # Simulate compliance status
                score = random.uniform(0.7, 1.0)  # Most requirements are compliant
                status = ComplianceStatus.COMPLIANT if score >= 0.9 else (
                    ComplianceStatus.PARTIALLY_COMPLIANT if score >= 0.7 else ComplianceStatus.NON_COMPLIANT
                )
                
                requirements_status[requirement] = {
                    "status": status,
                    "score": round(score, 2),
                    "last_assessed": datetime.now().isoformat(),
                    "evidence_count": random.randint(3, 15),
                    "findings": random.randint(0, 3) if status != ComplianceStatus.COMPLIANT else 0
                }
                total_score += score
            
            framework_score = (total_score / len(framework_info["requirements"])) * 100
            
            self.tenant_compliance[tenant_id]["frameworks"][framework] = {
                "framework_info": framework_info,
                "overall_score": round(framework_score, 1),
                "status": ComplianceStatus.COMPLIANT if framework_score >= 90 else (
                    ComplianceStatus.PARTIALLY_COMPLIANT if framework_score >= 70 else ComplianceStatus.NON_COMPLIANT
                ),
                "requirements": requirements_status,
                "last_audit": (datetime.now() - timedelta(days=random.randint(30, 180))).isoformat(),
                "next_audit": (datetime.now() + timedelta(days=random.randint(60, 180))).isoformat(),
                "certification_expiry": (datetime.now() + timedelta(days=framework_info["certification_validity"])).isoformat(),
                "findings_count": sum(req["findings"] for req in requirements_status.values()),
                "evidence_artifacts": random.randint(50, 200)
            }
            
        except Exception as e:
            logger.error(f"❌ Error setting up framework compliance: {e}")

    async def _calculate_overall_score(self, tenant_id: str):
        """Calculate overall compliance score for a tenant"""
        try:
            if tenant_id not in self.tenant_compliance:
                return
            
            frameworks = self.tenant_compliance[tenant_id]["frameworks"]
            if not frameworks:
                return
            
            total_score = sum(fw["overall_score"] for fw in frameworks.values())
            overall_score = total_score / len(frameworks)
            
            self.tenant_compliance[tenant_id]["overall_score"] = round(overall_score, 1)
            
        except Exception as e:
            logger.error(f"❌ Error calculating overall score: {e}")

    async def get_compliance_status(self, tenant_id: str) -> Dict:
        """Get current compliance status for a tenant"""
        try:
            if tenant_id not in self.tenant_compliance:
                return {"error": "Tenant compliance data not found"}
            
            compliance_data = self.tenant_compliance[tenant_id]
            
            return {
                "tenant_id": tenant_id,
                "overall_score": compliance_data["overall_score"],
                "frameworks_count": len(compliance_data["frameworks"]),
                "last_assessment": compliance_data["last_assessment"],
                "next_audit": compliance_data["next_audit"],
                "status_summary": {
                    "compliant_frameworks": sum(1 for fw in compliance_data["frameworks"].values() 
                                               if fw["status"] == ComplianceStatus.COMPLIANT),
                    "partially_compliant": sum(1 for fw in compliance_data["frameworks"].values() 
                                             if fw["status"] == ComplianceStatus.PARTIALLY_COMPLIANT),
                    "non_compliant": sum(1 for fw in compliance_data["frameworks"].values() 
                                       if fw["status"] == ComplianceStatus.NON_COMPLIANT)
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting compliance status: {e}")
            return {"error": str(e)}

    async def get_detailed_status(self, tenant_id: str) -> Dict:
        """Get detailed compliance status for a tenant"""
        try:
            if tenant_id not in self.tenant_compliance:
                return {"error": "Tenant compliance data not found"}
            
            compliance_data = self.tenant_compliance[tenant_id]
            
            detailed_status = {
                "tenant_id": tenant_id,
                "overall_compliance": {
                    "score": compliance_data["overall_score"],
                    "status": "Excellent" if compliance_data["overall_score"] >= 95 else (
                        "Good" if compliance_data["overall_score"] >= 85 else (
                            "Needs Improvement" if compliance_data["overall_score"] >= 70 else "Critical"
                        )
                    ),
                    "last_assessment": compliance_data["last_assessment"],
                    "next_audit": compliance_data["next_audit"]
                },
                "frameworks": {},
                "risk_assessment": await self._generate_risk_assessment(tenant_id),
                "improvement_recommendations": await self._generate_improvement_recommendations(tenant_id)
            }
            
            # Add detailed framework information
            for framework, data in compliance_data["frameworks"].items():
                detailed_status["frameworks"][framework] = {
                    "name": data["framework_info"]["name"],
                    "score": data["overall_score"],
                    "status": data["status"],
                    "last_audit": data["last_audit"],
                    "next_audit": data["next_audit"],
                    "certification_expiry": data["certification_expiry"],
                    "findings_count": data["findings_count"],
                    "evidence_artifacts": data["evidence_artifacts"],
                    "requirements_summary": {
                        "total": len(data["requirements"]),
                        "compliant": sum(1 for req in data["requirements"].values() 
                                       if req["status"] == ComplianceStatus.COMPLIANT),
                        "partially_compliant": sum(1 for req in data["requirements"].values() 
                                                 if req["status"] == ComplianceStatus.PARTIALLY_COMPLIANT),
                        "non_compliant": sum(1 for req in data["requirements"].values() 
                                           if req["status"] == ComplianceStatus.NON_COMPLIANT)
                    }
                }
            
            return detailed_status
            
        except Exception as e:
            logger.error(f"❌ Error getting detailed status: {e}")
            return {"error": str(e)}

    async def _generate_risk_assessment(self, tenant_id: str) -> Dict:
        """Generate risk assessment based on compliance status"""
        try:
            compliance_data = self.tenant_compliance[tenant_id]
            overall_score = compliance_data["overall_score"]
            
            # Calculate risk level based on compliance score
            if overall_score >= 95:
                risk_level = "Low"
                risk_score = random.uniform(1, 3)
            elif overall_score >= 85:
                risk_level = "Medium"
                risk_score = random.uniform(3, 6)
            elif overall_score >= 70:
                risk_level = "High"
                risk_score = random.uniform(6, 8)
            else:
                risk_level = "Critical"
                risk_score = random.uniform(8, 10)
            
            return {
                "overall_risk_level": risk_level,
                "risk_score": round(risk_score, 1),
                "risk_factors": [
                    {
                        "factor": "Data Breach Risk",
                        "level": risk_level,
                        "impact": "High" if risk_score > 6 else "Medium",
                        "likelihood": "Medium" if risk_score > 5 else "Low"
                    },
                    {
                        "factor": "Regulatory Penalties",
                        "level": risk_level,
                        "impact": "High" if risk_score > 7 else "Medium",
                        "likelihood": "High" if risk_score > 6 else "Low"
                    },
                    {
                        "factor": "Operational Disruption",
                        "level": risk_level,
                        "impact": "Medium",
                        "likelihood": "Medium" if risk_score > 5 else "Low"
                    }
                ],
                "mitigation_priority": "Immediate" if risk_score > 7 else (
                    "High" if risk_score > 5 else "Medium"
                )
            }
            
        except Exception as e:
            logger.error(f"❌ Error generating risk assessment: {e}")
            return {}

    async def _generate_improvement_recommendations(self, tenant_id: str) -> List[Dict]:
        """Generate improvement recommendations based on compliance gaps"""
        try:
            recommendations = [
                {
                    "priority": "High",
                    "category": "Access Control",
                    "title": "Implement Multi-Factor Authentication",
                    "description": "Deploy MFA for all administrative accounts to enhance security",
                    "estimated_effort": "2-4 weeks",
                    "compliance_impact": "Improves SOC2 and ISO27001 scores by 5-8%"
                },
                {
                    "priority": "Medium",
                    "category": "Documentation",
                    "title": "Update Security Policies",
                    "description": "Review and update information security policies annually",
                    "estimated_effort": "1-2 weeks",
                    "compliance_impact": "Maintains current compliance levels"
                },
                {
                    "priority": "Medium",
                    "category": "Monitoring",
                    "title": "Enhanced Audit Logging",
                    "description": "Implement comprehensive audit logging for all systems",
                    "estimated_effort": "3-6 weeks",
                    "compliance_impact": "Improves multiple framework scores by 3-5%"
                },
                {
                    "priority": "Low",
                    "category": "Training",
                    "title": "Security Awareness Training",
                    "description": "Conduct quarterly security awareness training for all staff",
                    "estimated_effort": "Ongoing",
                    "compliance_impact": "Supports human resource security requirements"
                }
            ]
            
            return recommendations
            
        except Exception as e:
            logger.error(f"❌ Error generating improvement recommendations: {e}")
            return []

    async def get_framework_status(self, tenant_id: str) -> Dict:
        """Get status for all frameworks for a tenant"""
        try:
            if tenant_id not in self.tenant_compliance:
                return {"error": "Tenant compliance data not found"}
            
            frameworks_status = {}
            compliance_data = self.tenant_compliance[tenant_id]
            
            for framework, data in compliance_data["frameworks"].items():
                frameworks_status[framework] = {
                    "name": data["framework_info"]["name"],
                    "score": data["overall_score"],
                    "status": data["status"],
                    "last_audit": data["last_audit"],
                    "next_audit": data["next_audit"],
                    "findings": data["findings_count"],
                    "certification_expiry": data["certification_expiry"]
                }
            
            return frameworks_status
            
        except Exception as e:
            logger.error(f"❌ Error getting framework status: {e}")
            return {"error": str(e)}

    async def get_recent_audits(self, tenant_id: str) -> List[Dict]:
        """Get recent audit activities for a tenant"""
        try:
            recent_audits = []
            
            # Generate mock recent audit data
            for i in range(5):
                audit_date = datetime.now() - timedelta(days=random.randint(1, 90))
                frameworks = list(self.tenant_compliance.get(tenant_id, {}).get("frameworks", {}).keys())
                
                if frameworks:
                    framework = random.choice(frameworks)
                    recent_audits.append({
                        "audit_id": str(uuid.uuid4()),
                        "framework": framework,
                        "audit_type": random.choice(["Internal", "External", "Self-Assessment"]),
                        "date": audit_date.isoformat(),
                        "auditor": f"Auditor {random.randint(1, 10)}",
                        "status": random.choice(["Completed", "In Progress", "Scheduled"]),
                        "findings": random.randint(0, 5),
                        "score": round(random.uniform(85, 98), 1)
                    })
            
            return sorted(recent_audits, key=lambda x: x["date"], reverse=True)
            
        except Exception as e:
            logger.error(f"❌ Error getting recent audits: {e}")
            return []

    async def get_upcoming_requirements(self, tenant_id: str) -> List[Dict]:
        """Get upcoming compliance requirements and deadlines"""
        try:
            upcoming_requirements = []
            
            if tenant_id in self.tenant_compliance:
                frameworks = self.tenant_compliance[tenant_id]["frameworks"]
                
                for framework, data in frameworks.items():
                    # Next audit
                    next_audit = datetime.fromisoformat(data["next_audit"])
                    days_until_audit = (next_audit - datetime.now()).days
                    
                    upcoming_requirements.append({
                        "type": "audit",
                        "framework": framework,
                        "title": f"{data['framework_info']['name']} Audit",
                        "due_date": data["next_audit"],
                        "days_remaining": days_until_audit,
                        "priority": "High" if days_until_audit < 30 else "Medium",
                        "description": f"Annual compliance audit for {framework}"
                    })
                    
                    # Certification expiry
                    cert_expiry = datetime.fromisoformat(data["certification_expiry"])
                    days_until_expiry = (cert_expiry - datetime.now()).days
                    
                    if days_until_expiry < 90:  # Only show if expiring within 90 days
                        upcoming_requirements.append({
                            "type": "certification_renewal",
                            "framework": framework,
                            "title": f"{data['framework_info']['name']} Certification Renewal",
                            "due_date": data["certification_expiry"],
                            "days_remaining": days_until_expiry,
                            "priority": "Critical" if days_until_expiry < 30 else "High",
                            "description": f"Certification renewal required for {framework}"
                        })
            
            return sorted(upcoming_requirements, key=lambda x: x["days_remaining"])
            
        except Exception as e:
            logger.error(f"❌ Error getting upcoming requirements: {e}")
            return []

    async def generate_report(
        self,
        tenant_id: str,
        framework: ComplianceFramework,
        report_period: str,
        include_recommendations: bool = True,
        detailed_findings: bool = False
    ) -> Dict:
        """Generate a compliance report"""
        try:
            report_id = str(uuid.uuid4())
            
            if tenant_id not in self.tenant_compliance:
                raise ValueError("Tenant compliance data not found")
            
            if framework not in self.tenant_compliance[tenant_id]["frameworks"]:
                raise ValueError(f"Framework {framework} not configured for tenant")
            
            framework_data = self.tenant_compliance[tenant_id]["frameworks"][framework]
            
            report = {
                "report_id": report_id,
                "tenant_id": tenant_id,
                "framework": framework,
                "framework_name": framework_data["framework_info"]["name"],
                "report_period": report_period,
                "generated_at": datetime.now().isoformat(),
                "summary": {
                    "overall_score": framework_data["overall_score"],
                    "status": framework_data["status"],
                    "total_requirements": len(framework_data["requirements"]),
                    "compliant_requirements": sum(1 for req in framework_data["requirements"].values() 
                                                if req["status"] == ComplianceStatus.COMPLIANT),
                    "findings_count": framework_data["findings_count"],
                    "evidence_artifacts": framework_data["evidence_artifacts"]
                },
                "requirements_breakdown": {},
                "risk_assessment": await self._generate_risk_assessment(tenant_id)
            }
            
            # Add requirements breakdown
            for req_name, req_data in framework_data["requirements"].items():
                report["requirements_breakdown"][req_name] = {
                    "status": req_data["status"],
                    "score": req_data["score"],
                    "findings": req_data["findings"],
                    "evidence_count": req_data["evidence_count"]
                }
                
                if detailed_findings and req_data["findings"] > 0:
                    report["requirements_breakdown"][req_name]["detailed_findings"] = [
                        f"Finding {i+1}: Sample compliance gap identified"
                        for i in range(req_data["findings"])
                    ]
            
            # Add recommendations if requested
            if include_recommendations:
                report["recommendations"] = await self._generate_improvement_recommendations(tenant_id)
            
            # Store the report
            if tenant_id not in self.compliance_reports:
                self.compliance_reports[tenant_id] = []
            
            self.compliance_reports[tenant_id].append(report)
            
            logger.info(f"✅ Generated compliance report {report_id} for tenant {tenant_id}")
            
            return report
            
        except Exception as e:
            logger.error(f"❌ Error generating compliance report: {e}")
            raise

    async def get_supported_frameworks(self) -> List[Dict]:
        """Get list of supported compliance frameworks"""
        try:
            return [
                {
                    "framework": framework,
                    "name": info["name"],
                    "description": info["description"],
                    "categories": info["categories"],
                    "requirements_count": len(info["requirements"]),
                    "audit_frequency": info["audit_frequency"]
                }
                for framework, info in self.framework_requirements.items()
            ]
        except Exception as e:
            logger.error(f"❌ Error getting supported frameworks: {e}")
            return []

    async def start_compliance_monitoring(self):
        """Start background compliance monitoring"""
        try:
            logger.info("🔍 Starting compliance monitoring...")
            
            while self.is_active:
                # Update compliance scores for all tenants
                for tenant_id in self.tenant_compliance:
                    await self._update_compliance_scores(tenant_id)
                
                await asyncio.sleep(3600)  # Update every hour
                
        except Exception as e:
            logger.error(f"❌ Error in compliance monitoring: {e}")

    async def _update_compliance_scores(self, tenant_id: str):
        """Update compliance scores for a tenant"""
        try:
            if tenant_id in self.tenant_compliance:
                # Simulate minor score fluctuations
                for framework_data in self.tenant_compliance[tenant_id]["frameworks"].values():
                    current_score = framework_data["overall_score"]
                    # Small random fluctuation
                    fluctuation = random.uniform(-0.5, 0.5)
                    new_score = max(0, min(100, current_score + fluctuation))
                    framework_data["overall_score"] = round(new_score, 1)
                
                # Recalculate overall score
                await self._calculate_overall_score(tenant_id)
                
        except Exception as e:
            logger.error(f"❌ Error updating compliance scores: {e}")

    async def shutdown(self):
        """Shutdown the compliance auditor"""
        try:
            logger.info("🛑 Shutting down Compliance Auditor...")
            self.is_active = False
            
        except Exception as e:
            logger.error(f"❌ Error shutting down Compliance Auditor: {e}")

# Global compliance auditor instance
compliance_auditor = ComplianceAuditor() 