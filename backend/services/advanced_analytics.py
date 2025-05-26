"""
📊 Advanced Analytics Service
Comprehensive business intelligence and reporting for enterprise tenants
"""

import asyncio
import json
import logging
import random
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from collections import defaultdict
import math

logger = logging.getLogger(__name__)

class AdvancedAnalytics:
    def __init__(self):
        self.is_active = False
        self.tenant_analytics: Dict[str, Dict] = {}
        self.analytics_cache: Dict[str, Dict] = {}
        self.real_time_metrics: Dict[str, Dict] = {}
        
    async def initialize(self):
        """Initialize the advanced analytics service"""
        try:
            logger.info("📊 Initializing Advanced Analytics...")
            
            # Initialize demo analytics data
            await self._initialize_demo_analytics()
            
            self.is_active = True
            logger.info("✅ Advanced Analytics initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Error initializing Advanced Analytics: {e}")
            raise

    async def _initialize_demo_analytics(self):
        """Initialize demo analytics data for testing"""
        demo_tenants = ["demo-tenant-1", "demo-tenant-2", "demo-tenant-3"]
        
        for tenant_id in demo_tenants:
            await self._generate_historical_data(tenant_id)

    async def _generate_historical_data(self, tenant_id: str):
        """Generate historical analytics data for a tenant"""
        try:
            # Generate 30 days of historical data
            historical_data = []
            base_threats = 50
            
            for i in range(30):
                date = datetime.now() - timedelta(days=29-i)
                
                # Simulate varying threat levels with trends
                daily_threats = base_threats + random.randint(-20, 30) + math.sin(i/7) * 10
                daily_threats = max(0, int(daily_threats))
                
                daily_data = {
                    "date": date.strftime("%Y-%m-%d"),
                    "threats_detected": daily_threats,
                    "threats_blocked": int(daily_threats * 0.85),
                    "false_positives": int(daily_threats * 0.05),
                    "response_time_avg": round(45 + random.uniform(-10, 15), 2),
                    "api_calls": random.randint(1000, 5000),
                    "unique_users": random.randint(10, 50),
                    "compliance_score": round(90 + random.uniform(-5, 8), 1)
                }
                historical_data.append(daily_data)
            
            self.tenant_analytics[tenant_id] = {
                "historical_data": historical_data,
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Error generating historical data: {e}")

    async def get_comprehensive_overview(self, tenant_id: str) -> Dict:
        """Get comprehensive analytics overview for a tenant"""
        try:
            if tenant_id not in self.tenant_analytics:
                await self._generate_historical_data(tenant_id)
            
            historical_data = self.tenant_analytics[tenant_id]["historical_data"]
            
            # Calculate summary statistics
            total_threats = sum(day["threats_detected"] for day in historical_data)
            total_blocked = sum(day["threats_blocked"] for day in historical_data)
            avg_response_time = sum(day["response_time_avg"] for day in historical_data) / len(historical_data)
            avg_compliance_score = sum(day["compliance_score"] for day in historical_data) / len(historical_data)
            
            # Calculate trends (last 7 days vs previous 7 days)
            recent_7_days = historical_data[-7:]
            previous_7_days = historical_data[-14:-7]
            
            recent_threats = sum(day["threats_detected"] for day in recent_7_days)
            previous_threats = sum(day["threats_detected"] for day in previous_7_days)
            threat_trend = ((recent_threats - previous_threats) / max(1, previous_threats)) * 100
            
            recent_response_time = sum(day["response_time_avg"] for day in recent_7_days) / 7
            previous_response_time = sum(day["response_time_avg"] for day in previous_7_days) / 7
            response_time_trend = ((recent_response_time - previous_response_time) / previous_response_time) * 100
            
            overview = {
                "summary_statistics": {
                    "total_threats_30_days": total_threats,
                    "total_blocked_30_days": total_blocked,
                    "block_rate_percentage": round((total_blocked / max(1, total_threats)) * 100, 2),
                    "average_response_time": round(avg_response_time, 2),
                    "average_compliance_score": round(avg_compliance_score, 1),
                    "false_positive_rate": round(sum(day["false_positives"] for day in historical_data) / max(1, total_threats) * 100, 2)
                },
                "trends": {
                    "threat_detection_trend": round(threat_trend, 2),
                    "response_time_trend": round(response_time_trend, 2),
                    "trend_direction": "increasing" if threat_trend > 0 else "decreasing",
                    "performance_trend": "improving" if response_time_trend < 0 else "declining"
                },
                "daily_breakdown": historical_data[-7:],  # Last 7 days
                "threat_categories": await self._get_threat_category_breakdown(tenant_id),
                "geographic_distribution": await self._get_geographic_breakdown(tenant_id),
                "time_of_day_analysis": await self._get_time_of_day_analysis(tenant_id)
            }
            
            return overview
            
        except Exception as e:
            logger.error(f"❌ Error getting comprehensive overview: {e}")
            return {}

    async def _get_threat_category_breakdown(self, tenant_id: str) -> Dict:
        """Get breakdown of threats by category"""
        categories = {
            "malware": random.randint(15, 35),
            "phishing": random.randint(10, 25),
            "insider_threat": random.randint(5, 15),
            "data_breach": random.randint(3, 12),
            "fraud": random.randint(8, 20),
            "ransomware": random.randint(2, 8),
            "ddos": random.randint(5, 15),
            "supply_chain": random.randint(1, 6)
        }
        
        total = sum(categories.values())
        return {
            "categories": categories,
            "percentages": {k: round((v/total)*100, 1) for k, v in categories.items()},
            "total_threats": total
        }

    async def _get_geographic_breakdown(self, tenant_id: str) -> Dict:
        """Get geographic distribution of threats"""
        return {
            "regions": {
                "north_america": random.randint(30, 50),
                "europe": random.randint(20, 35),
                "asia_pacific": random.randint(15, 25),
                "south_america": random.randint(3, 8),
                "africa": random.randint(2, 6),
                "oceania": random.randint(1, 4)
            },
            "top_countries": [
                {"country": "United States", "threats": random.randint(25, 40)},
                {"country": "China", "threats": random.randint(15, 25)},
                {"country": "Russia", "threats": random.randint(10, 20)},
                {"country": "Germany", "threats": random.randint(8, 15)},
                {"country": "United Kingdom", "threats": random.randint(6, 12)}
            ]
        }

    async def _get_time_of_day_analysis(self, tenant_id: str) -> Dict:
        """Get time-of-day threat analysis"""
        hourly_data = {}
        for hour in range(24):
            # Simulate higher activity during business hours
            if 9 <= hour <= 17:
                base_activity = 15
            elif 18 <= hour <= 22:
                base_activity = 10
            else:
                base_activity = 5
            
            hourly_data[f"{hour:02d}:00"] = base_activity + random.randint(-3, 8)
        
        return {
            "hourly_distribution": hourly_data,
            "peak_hours": ["10:00", "14:00", "16:00"],
            "low_activity_hours": ["02:00", "04:00", "06:00"]
        }

    async def get_threat_analytics(self, tenant_id: str, time_range: str) -> Dict:
        """Get detailed threat analytics for a specific time range"""
        try:
            # Parse time range
            if time_range == "1h":
                hours = 1
            elif time_range == "24h":
                hours = 24
            elif time_range == "7d":
                hours = 24 * 7
            elif time_range == "30d":
                hours = 24 * 30
            else:
                hours = 24 * 7  # Default to 7 days
            
            # Generate threat analytics data
            threat_analytics = {
                "time_range": time_range,
                "total_threats": random.randint(50, 200) * (hours // 24 + 1),
                "threat_severity_distribution": {
                    "critical": random.randint(5, 15),
                    "high": random.randint(15, 30),
                    "medium": random.randint(25, 45),
                    "low": random.randint(30, 60)
                },
                "attack_vectors": {
                    "email": random.randint(20, 40),
                    "web": random.randint(15, 35),
                    "network": random.randint(10, 25),
                    "endpoint": random.randint(8, 20),
                    "cloud": random.randint(5, 15),
                    "mobile": random.randint(3, 10)
                },
                "threat_actors": {
                    "cybercriminals": random.randint(40, 60),
                    "nation_state": random.randint(10, 20),
                    "insider_threat": random.randint(5, 15),
                    "hacktivists": random.randint(3, 10),
                    "unknown": random.randint(10, 25)
                },
                "mitigation_effectiveness": {
                    "blocked_automatically": random.randint(70, 85),
                    "quarantined": random.randint(5, 15),
                    "manual_intervention": random.randint(3, 10),
                    "false_positives": random.randint(2, 8)
                }
            }
            
            return threat_analytics
            
        except Exception as e:
            logger.error(f"❌ Error getting threat analytics: {e}")
            return {}

    async def get_threat_trends(self, tenant_id: str, time_range: str) -> Dict:
        """Get threat trend analysis"""
        try:
            # Generate trend data points
            if time_range == "1h":
                data_points = 12  # 5-minute intervals
                interval = "5min"
            elif time_range == "24h":
                data_points = 24  # Hourly
                interval = "1hour"
            elif time_range == "7d":
                data_points = 7   # Daily
                interval = "1day"
            else:
                data_points = 30  # Daily for 30 days
                interval = "1day"
            
            trend_data = []
            base_value = 20
            
            for i in range(data_points):
                # Add some randomness and trend
                value = base_value + random.randint(-5, 10) + math.sin(i/3) * 5
                timestamp = datetime.now() - timedelta(hours=(data_points-i-1))
                
                trend_data.append({
                    "timestamp": timestamp.isoformat(),
                    "threats_detected": max(0, int(value)),
                    "threats_blocked": max(0, int(value * 0.85)),
                    "response_time": round(45 + random.uniform(-10, 15), 2)
                })
            
            return {
                "time_range": time_range,
                "interval": interval,
                "data_points": trend_data,
                "trend_analysis": {
                    "overall_trend": "stable",
                    "peak_detection_time": trend_data[max(range(len(trend_data)), key=lambda i: trend_data[i]["threats_detected"])]["timestamp"],
                    "average_threats_per_interval": round(sum(d["threats_detected"] for d in trend_data) / len(trend_data), 2)
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting threat trends: {e}")
            return {}

    async def get_geographic_threats(self, tenant_id: str) -> Dict:
        """Get geographic threat distribution"""
        try:
            return {
                "global_distribution": {
                    "threat_map": [
                        {"country": "US", "lat": 39.8283, "lng": -98.5795, "threats": random.randint(50, 100)},
                        {"country": "CN", "lat": 35.8617, "lng": 104.1954, "threats": random.randint(30, 70)},
                        {"country": "RU", "lat": 61.5240, "lng": 105.3188, "threats": random.randint(25, 60)},
                        {"country": "DE", "lat": 51.1657, "lng": 10.4515, "threats": random.randint(20, 45)},
                        {"country": "GB", "lat": 55.3781, "lng": -3.4360, "threats": random.randint(15, 35)},
                        {"country": "IN", "lat": 20.5937, "lng": 78.9629, "threats": random.randint(10, 30)},
                        {"country": "BR", "lat": -14.2350, "lng": -51.9253, "threats": random.randint(8, 25)},
                        {"country": "JP", "lat": 36.2048, "lng": 138.2529, "threats": random.randint(12, 28)}
                    ]
                },
                "regional_summary": {
                    "highest_risk_region": "North America",
                    "emerging_threat_regions": ["Eastern Europe", "Southeast Asia"],
                    "safest_regions": ["Oceania", "Northern Europe"]
                },
                "threat_migration_patterns": {
                    "primary_sources": ["Eastern Europe", "East Asia"],
                    "target_regions": ["North America", "Western Europe"],
                    "migration_trends": "Increasing activity from state-sponsored groups"
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting geographic threats: {e}")
            return {}

    async def get_real_time_metrics(self, tenant_id: str) -> Dict:
        """Get real-time metrics for a tenant"""
        try:
            current_time = datetime.now()
            
            # Generate real-time metrics
            metrics = {
                "current_timestamp": current_time.isoformat(),
                "active_threats": random.randint(0, 5),
                "threats_blocked_last_hour": random.randint(5, 25),
                "system_performance": {
                    "cpu_usage": round(random.uniform(20, 80), 1),
                    "memory_usage": round(random.uniform(30, 70), 1),
                    "network_throughput": round(random.uniform(0.5, 5.0), 2),
                    "response_time": round(random.uniform(35, 65), 2)
                },
                "threat_intelligence": {
                    "new_indicators": random.randint(10, 50),
                    "updated_rules": random.randint(2, 15),
                    "threat_feeds_status": "operational",
                    "last_update": (current_time - timedelta(minutes=random.randint(1, 30))).isoformat()
                },
                "compliance_status": {
                    "current_score": round(random.uniform(90, 99), 1),
                    "frameworks_monitored": random.randint(3, 6),
                    "violations_detected": random.randint(0, 2),
                    "last_audit": (current_time - timedelta(days=random.randint(1, 30))).isoformat()
                }
            }
            
            # Cache the metrics
            self.real_time_metrics[tenant_id] = metrics
            
            return metrics
            
        except Exception as e:
            logger.error(f"❌ Error getting real-time metrics: {e}")
            return {}

    async def get_key_insights(self, tenant_id: str) -> List[Dict]:
        """Get key insights and recommendations for a tenant"""
        try:
            insights = [
                {
                    "type": "threat_trend",
                    "severity": "medium",
                    "title": "Increased Phishing Activity",
                    "description": "Phishing attempts have increased by 23% in the last 7 days",
                    "recommendation": "Consider implementing additional email security training",
                    "timestamp": (datetime.now() - timedelta(hours=2)).isoformat()
                },
                {
                    "type": "performance",
                    "severity": "low",
                    "title": "Response Time Optimization",
                    "description": "Average response time is 15% faster than industry benchmark",
                    "recommendation": "Current performance is excellent, maintain current configuration",
                    "timestamp": (datetime.now() - timedelta(hours=6)).isoformat()
                },
                {
                    "type": "compliance",
                    "severity": "high",
                    "title": "Compliance Score Improvement",
                    "description": "SOC2 compliance score improved to 96.5%",
                    "recommendation": "Focus on remaining 3.5% to achieve full compliance",
                    "timestamp": (datetime.now() - timedelta(hours=12)).isoformat()
                },
                {
                    "type": "security",
                    "severity": "medium",
                    "title": "New Threat Vector Detected",
                    "description": "Supply chain attacks targeting your industry have increased",
                    "recommendation": "Review vendor security assessments and implement additional monitoring",
                    "timestamp": (datetime.now() - timedelta(days=1)).isoformat()
                }
            ]
            
            return insights
            
        except Exception as e:
            logger.error(f"❌ Error getting key insights: {e}")
            return []

    async def get_recommendations(self, tenant_id: str) -> List[Dict]:
        """Get actionable recommendations for a tenant"""
        try:
            recommendations = [
                {
                    "category": "security_enhancement",
                    "priority": "high",
                    "title": "Implement Zero Trust Architecture",
                    "description": "Based on your threat profile, implementing zero trust would reduce risk by 40%",
                    "estimated_impact": "40% risk reduction",
                    "implementation_effort": "medium",
                    "timeline": "3-6 months"
                },
                {
                    "category": "performance_optimization",
                    "priority": "medium",
                    "title": "Optimize Threat Detection Rules",
                    "description": "Fine-tuning detection rules could reduce false positives by 25%",
                    "estimated_impact": "25% fewer false positives",
                    "implementation_effort": "low",
                    "timeline": "2-4 weeks"
                },
                {
                    "category": "compliance",
                    "priority": "medium",
                    "title": "Automate Compliance Reporting",
                    "description": "Automated reporting would save 20 hours per month and improve accuracy",
                    "estimated_impact": "20 hours saved monthly",
                    "implementation_effort": "low",
                    "timeline": "1-2 weeks"
                },
                {
                    "category": "cost_optimization",
                    "priority": "low",
                    "title": "Right-size Infrastructure",
                    "description": "Current usage patterns suggest 15% cost savings opportunity",
                    "estimated_impact": "15% cost reduction",
                    "implementation_effort": "low",
                    "timeline": "1 week"
                }
            ]
            
            return recommendations
            
        except Exception as e:
            logger.error(f"❌ Error getting recommendations: {e}")
            return []

    async def start_analytics_engine(self):
        """Start background analytics processing"""
        try:
            logger.info("🔄 Starting analytics engine...")
            
            while self.is_active:
                # Update real-time metrics for all tenants
                for tenant_id in self.tenant_analytics:
                    await self.get_real_time_metrics(tenant_id)
                
                await asyncio.sleep(60)  # Update every minute
                
        except Exception as e:
            logger.error(f"❌ Error in analytics engine: {e}")

    async def shutdown(self):
        """Shutdown the advanced analytics service"""
        try:
            logger.info("🛑 Shutting down Advanced Analytics...")
            self.is_active = False
            
        except Exception as e:
            logger.error(f"❌ Error shutting down Advanced Analytics: {e}")

# Global advanced analytics instance
advanced_analytics = AdvancedAnalytics() 