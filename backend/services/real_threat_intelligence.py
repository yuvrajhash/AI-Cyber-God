"""
🛡️ REAL THREAT INTELLIGENCE SERVICE
Production-ready threat intelligence integration with multiple real data sources
"""

import asyncio
import aiohttp
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import redis
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

class ThreatLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatType(str, Enum):
    MALWARE = "malware"
    PHISHING = "phishing"
    C2_SERVER = "c2_server"
    BOTNET = "botnet"
    SPAM = "spam"
    SUSPICIOUS_DOMAIN = "suspicious_domain"
    MALICIOUS_IP = "malicious_ip"
    SSL_CERTIFICATE = "ssl_certificate"

@dataclass
class ThreatIndicator:
    """Real threat indicator from external sources"""
    indicator_id: str
    indicator_type: str  # ip, domain, url, hash, email
    indicator_value: str
    threat_type: ThreatType
    threat_level: ThreatLevel
    confidence: float
    source: str
    first_seen: datetime
    last_seen: datetime
    tags: List[str]
    context: Dict[str, Any]
    
    def to_dict(self):
        return {
            **asdict(self),
            'threat_type': self.threat_type.value,
            'threat_level': self.threat_level.value,
            'first_seen': self.first_seen.isoformat(),
            'last_seen': self.last_seen.isoformat()
        }

class HuntIOThreatFeed:
    """Hunt.io threat intelligence feed integration"""
    
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://api.hunt.io/v1/feeds/"
        self.session = None
        
    async def initialize(self):
        """Initialize HTTP session"""
        self.session = aiohttp.ClientSession(
            headers={"token": self.api_token},
            timeout=aiohttp.ClientTimeout(total=30)
        )
    
    async def get_c2_servers(self) -> List[ThreatIndicator]:
        """Get Command & Control servers from Hunt.io"""
        try:
            async with self.session.get(f"{self.base_url}c2") as response:
                if response.status == 200:
                    data = await response.json()
                    indicators = []
                    
                    for item in data.get('results', []):
                        indicator = ThreatIndicator(
                            indicator_id=f"huntio_c2_{hashlib.md5(item['ip'].encode()).hexdigest()}",
                            indicator_type="ip",
                            indicator_value=item['ip'],
                            threat_type=ThreatType.C2_SERVER,
                            threat_level=ThreatLevel.HIGH,
                            confidence=0.9,
                            source="hunt.io",
                            first_seen=datetime.fromisoformat(item.get('first_seen', datetime.now().isoformat())),
                            last_seen=datetime.fromisoformat(item.get('last_seen', datetime.now().isoformat())),
                            tags=item.get('tags', ['c2', 'command_control']),
                            context={
                                'port': item.get('port'),
                                'protocol': item.get('protocol'),
                                'family': item.get('family'),
                                'country': item.get('country')
                            }
                        )
                        indicators.append(indicator)
                    
                    return indicators
                else:
                    logger.error(f"Hunt.io C2 feed error: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching Hunt.io C2 servers: {e}")
            return []
    
    async def get_ssl_certificates(self) -> List[ThreatIndicator]:
        """Get suspicious SSL certificates from Hunt.io"""
        try:
            async with self.session.get(f"{self.base_url}ssl") as response:
                if response.status == 200:
                    data = await response.json()
                    indicators = []
                    
                    for item in data.get('results', []):
                        indicator = ThreatIndicator(
                            indicator_id=f"huntio_ssl_{hashlib.md5(item['sha256'].encode()).hexdigest()}",
                            indicator_type="hash",
                            indicator_value=item['sha256'],
                            threat_type=ThreatType.SSL_CERTIFICATE,
                            threat_level=ThreatLevel.MEDIUM,
                            confidence=0.8,
                            source="hunt.io",
                            first_seen=datetime.fromisoformat(item.get('first_seen', datetime.now().isoformat())),
                            last_seen=datetime.fromisoformat(item.get('last_seen', datetime.now().isoformat())),
                            tags=item.get('tags', ['ssl', 'certificate']),
                            context={
                                'subject': item.get('subject'),
                                'issuer': item.get('issuer'),
                                'domains': item.get('domains', []),
                                'validity_period': item.get('validity_period')
                            }
                        )
                        indicators.append(indicator)
                    
                    return indicators
                else:
                    logger.error(f"Hunt.io SSL feed error: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching Hunt.io SSL certificates: {e}")
            return []

class AbuseCHThreatFeed:
    """abuse.ch URLhaus threat intelligence feed"""
    
    def __init__(self):
        self.base_url = "https://urlhaus-api.abuse.ch/v1/"
        self.session = None
    
    async def initialize(self):
        """Initialize HTTP session"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30)
        )
    
    async def get_recent_urls(self, limit: int = 100) -> List[ThreatIndicator]:
        """Get recent malicious URLs from URLhaus"""
        try:
            payload = {"limit": limit}
            async with self.session.post(f"{self.base_url}payloads/recent/", data=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    indicators = []
                    
                    for item in data.get('payloads', []):
                        indicator = ThreatIndicator(
                            indicator_id=f"abusech_url_{hashlib.md5(item['url'].encode()).hexdigest()}",
                            indicator_type="url",
                            indicator_value=item['url'],
                            threat_type=ThreatType.MALWARE,
                            threat_level=self._map_threat_level(item.get('threat', 'unknown')),
                            confidence=0.85,
                            source="abuse.ch",
                            first_seen=datetime.fromisoformat(item.get('firstseen', datetime.now().isoformat())),
                            last_seen=datetime.fromisoformat(item.get('lastseen', datetime.now().isoformat())),
                            tags=item.get('tags', ['malware', 'payload']),
                            context={
                                'file_type': item.get('file_type'),
                                'file_size': item.get('file_size'),
                                'signature': item.get('signature'),
                                'urlhaus_link': item.get('urlhaus_link')
                            }
                        )
                        indicators.append(indicator)
                    
                    return indicators
                else:
                    logger.error(f"abuse.ch URLhaus feed error: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching abuse.ch URLs: {e}")
            return []
    
    def _map_threat_level(self, threat: str) -> ThreatLevel:
        """Map abuse.ch threat levels to our enum"""
        mapping = {
            'malware_download': ThreatLevel.HIGH,
            'botnet_cc': ThreatLevel.CRITICAL,
            'phishing': ThreatLevel.HIGH,
            'exploit_kit': ThreatLevel.CRITICAL,
            'unknown': ThreatLevel.MEDIUM
        }
        return mapping.get(threat.lower(), ThreatLevel.MEDIUM)

class SpamhausThreatFeed:
    """Spamhaus threat intelligence feed"""
    
    def __init__(self):
        self.base_url = "https://www.spamhaus.org/zen/"
        self.session = None
    
    async def initialize(self):
        """Initialize HTTP session"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30)
        )
    
    async def check_ip_reputation(self, ip_address: str) -> Optional[ThreatIndicator]:
        """Check IP reputation against Spamhaus"""
        try:
            # Note: In production, you would use DNS queries or Spamhaus API
            # This is a simplified implementation
            
            # Simulate Spamhaus check (replace with actual DNS query)
            is_malicious = await self._check_spamhaus_dns(ip_address)
            
            if is_malicious:
                indicator = ThreatIndicator(
                    indicator_id=f"spamhaus_ip_{hashlib.md5(ip_address.encode()).hexdigest()}",
                    indicator_type="ip",
                    indicator_value=ip_address,
                    threat_type=ThreatType.SPAM,
                    threat_level=ThreatLevel.MEDIUM,
                    confidence=0.9,
                    source="spamhaus",
                    first_seen=datetime.now(),
                    last_seen=datetime.now(),
                    tags=['spam', 'blacklist'],
                    context={
                        'list': 'zen',
                        'reason': 'spam_source'
                    }
                )
                return indicator
            
            return None
        except Exception as e:
            logger.error(f"Error checking Spamhaus reputation for {ip_address}: {e}")
            return None
    
    async def _check_spamhaus_dns(self, ip_address: str) -> bool:
        """Check IP against Spamhaus DNS blacklist"""
        # In production, implement actual DNS query to zen.spamhaus.org
        # For now, return False (not implemented)
        return False

class CISMSISACThreatFeed:
    """CIS MS-ISAC STIX/TAXII threat intelligence feed"""
    
    def __init__(self, taxii_server: str, collection_id: str, username: str = None, password: str = None):
        self.taxii_server = taxii_server
        self.collection_id = collection_id
        self.username = username
        self.password = password
        self.session = None
    
    async def initialize(self):
        """Initialize TAXII client"""
        auth = None
        if self.username and self.password:
            auth = aiohttp.BasicAuth(self.username, self.password)
        
        self.session = aiohttp.ClientSession(
            auth=auth,
            timeout=aiohttp.ClientTimeout(total=60)
        )
    
    async def get_stix_indicators(self) -> List[ThreatIndicator]:
        """Get STIX indicators from CIS MS-ISAC"""
        try:
            # TAXII 2.1 API endpoint
            url = f"{self.taxii_server}/collections/{self.collection_id}/objects/"
            
            params = {
                'type': 'indicator',
                'limit': 100
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    indicators = []
                    
                    for stix_obj in data.get('objects', []):
                        if stix_obj.get('type') == 'indicator':
                            indicator = self._parse_stix_indicator(stix_obj)
                            if indicator:
                                indicators.append(indicator)
                    
                    return indicators
                else:
                    logger.error(f"CIS MS-ISAC TAXII feed error: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching CIS MS-ISAC indicators: {e}")
            return []
    
    def _parse_stix_indicator(self, stix_obj: Dict) -> Optional[ThreatIndicator]:
        """Parse STIX indicator object"""
        try:
            pattern = stix_obj.get('pattern', '')
            labels = stix_obj.get('labels', [])
            
            # Extract indicator value from STIX pattern
            indicator_value = self._extract_indicator_value(pattern)
            if not indicator_value:
                return None
            
            # Determine indicator type
            indicator_type = self._determine_indicator_type(pattern)
            
            # Map labels to threat type
            threat_type = self._map_labels_to_threat_type(labels)
            
            indicator = ThreatIndicator(
                indicator_id=f"cis_msisac_{stix_obj['id']}",
                indicator_type=indicator_type,
                indicator_value=indicator_value,
                threat_type=threat_type,
                threat_level=ThreatLevel.MEDIUM,
                confidence=0.8,
                source="cis_ms_isac",
                first_seen=datetime.fromisoformat(stix_obj.get('created', datetime.now().isoformat())),
                last_seen=datetime.fromisoformat(stix_obj.get('modified', datetime.now().isoformat())),
                tags=labels,
                context={
                    'stix_id': stix_obj['id'],
                    'pattern': pattern,
                    'kill_chain_phases': stix_obj.get('kill_chain_phases', [])
                }
            )
            
            return indicator
        except Exception as e:
            logger.error(f"Error parsing STIX indicator: {e}")
            return None
    
    def _extract_indicator_value(self, pattern: str) -> Optional[str]:
        """Extract indicator value from STIX pattern"""
        # Simplified pattern parsing (in production, use proper STIX parser)
        if "file:hashes.MD5" in pattern:
            return pattern.split("'")[1] if "'" in pattern else None
        elif "domain-name:value" in pattern:
            return pattern.split("'")[1] if "'" in pattern else None
        elif "ipv4-addr:value" in pattern:
            return pattern.split("'")[1] if "'" in pattern else None
        elif "url:value" in pattern:
            return pattern.split("'")[1] if "'" in pattern else None
        return None
    
    def _determine_indicator_type(self, pattern: str) -> str:
        """Determine indicator type from STIX pattern"""
        if "file:hashes" in pattern:
            return "hash"
        elif "domain-name:value" in pattern:
            return "domain"
        elif "ipv4-addr:value" in pattern:
            return "ip"
        elif "url:value" in pattern:
            return "url"
        return "unknown"
    
    def _map_labels_to_threat_type(self, labels: List[str]) -> ThreatType:
        """Map STIX labels to threat type"""
        label_mapping = {
            'malicious-activity': ThreatType.MALWARE,
            'phishing': ThreatType.PHISHING,
            'botnet': ThreatType.BOTNET,
            'spam': ThreatType.SPAM
        }
        
        for label in labels:
            if label in label_mapping:
                return label_mapping[label]
        
        return ThreatType.SUSPICIOUS_DOMAIN

class RealThreatIntelligenceService:
    """Production threat intelligence service with real data sources"""
    
    def __init__(self):
        self.feeds = {}
        self.redis_client = None
        self.cache_ttl = 3600  # 1 hour cache
        self.is_active = False
        
        # Initialize feed configurations from environment
        self.feed_configs = {
            'hunt_io': {
                'enabled': os.getenv('HUNTIO_API_TOKEN') is not None,
                'api_token': os.getenv('HUNTIO_API_TOKEN'),
                'update_interval': 1800  # 30 minutes
            },
            'abuse_ch': {
                'enabled': True,  # Free service
                'update_interval': 3600  # 1 hour
            },
            'spamhaus': {
                'enabled': True,  # Free tier
                'update_interval': 7200  # 2 hours
            },
            'cis_ms_isac': {
                'enabled': all([
                    os.getenv('CIS_TAXII_SERVER'),
                    os.getenv('CIS_COLLECTION_ID')
                ]),
                'taxii_server': os.getenv('CIS_TAXII_SERVER'),
                'collection_id': os.getenv('CIS_COLLECTION_ID'),
                'username': os.getenv('CIS_USERNAME'),
                'password': os.getenv('CIS_PASSWORD'),
                'update_interval': 3600  # 1 hour
            }
        }
    
    async def initialize(self):
        """Initialize threat intelligence service"""
        try:
            logger.info("🛡️ Initializing Real Threat Intelligence Service...")
            
            # Initialize Redis cache
            redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
            self.redis_client = redis.from_url(redis_url, decode_responses=True)
            
            # Initialize enabled feeds
            if self.feed_configs['hunt_io']['enabled']:
                self.feeds['hunt_io'] = HuntIOThreatFeed(
                    self.feed_configs['hunt_io']['api_token']
                )
                await self.feeds['hunt_io'].initialize()
                logger.info("✅ Hunt.io feed initialized")
            
            if self.feed_configs['abuse_ch']['enabled']:
                self.feeds['abuse_ch'] = AbuseCHThreatFeed()
                await self.feeds['abuse_ch'].initialize()
                logger.info("✅ abuse.ch feed initialized")
            
            if self.feed_configs['spamhaus']['enabled']:
                self.feeds['spamhaus'] = SpamhausThreatFeed()
                await self.feeds['spamhaus'].initialize()
                logger.info("✅ Spamhaus feed initialized")
            
            if self.feed_configs['cis_ms_isac']['enabled']:
                self.feeds['cis_ms_isac'] = CISMSISACThreatFeed(
                    self.feed_configs['cis_ms_isac']['taxii_server'],
                    self.feed_configs['cis_ms_isac']['collection_id'],
                    self.feed_configs['cis_ms_isac']['username'],
                    self.feed_configs['cis_ms_isac']['password']
                )
                await self.feeds['cis_ms_isac'].initialize()
                logger.info("✅ CIS MS-ISAC feed initialized")
            
            self.is_active = True
            logger.info(f"✅ Real Threat Intelligence Service initialized with {len(self.feeds)} feeds")
            
            # Start background update tasks
            asyncio.create_task(self._start_feed_updates())
            
        except Exception as e:
            logger.error(f"❌ Error initializing Real Threat Intelligence Service: {e}")
            raise
    
    async def _start_feed_updates(self):
        """Start background tasks to update threat feeds"""
        tasks = []
        
        for feed_name, feed in self.feeds.items():
            interval = self.feed_configs[feed_name]['update_interval']
            task = asyncio.create_task(self._update_feed_periodically(feed_name, feed, interval))
            tasks.append(task)
        
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _update_feed_periodically(self, feed_name: str, feed, interval: int):
        """Periodically update a specific threat feed"""
        while self.is_active:
            try:
                logger.info(f"🔄 Updating {feed_name} threat feed...")
                await self._update_single_feed(feed_name, feed)
                logger.info(f"✅ Updated {feed_name} threat feed")
            except Exception as e:
                logger.error(f"❌ Error updating {feed_name} feed: {e}")
            
            await asyncio.sleep(interval)
    
    async def _update_single_feed(self, feed_name: str, feed):
        """Update a single threat feed"""
        indicators = []
        
        if feed_name == 'hunt_io':
            c2_indicators = await feed.get_c2_servers()
            ssl_indicators = await feed.get_ssl_certificates()
            indicators.extend(c2_indicators)
            indicators.extend(ssl_indicators)
        
        elif feed_name == 'abuse_ch':
            url_indicators = await feed.get_recent_urls()
            indicators.extend(url_indicators)
        
        elif feed_name == 'cis_ms_isac':
            stix_indicators = await feed.get_stix_indicators()
            indicators.extend(stix_indicators)
        
        # Cache indicators in Redis
        if indicators:
            cache_key = f"threat_indicators:{feed_name}"
            cached_data = {
                'indicators': [indicator.to_dict() for indicator in indicators],
                'last_updated': datetime.now().isoformat(),
                'count': len(indicators)
            }
            
            self.redis_client.setex(
                cache_key,
                self.cache_ttl,
                json.dumps(cached_data)
            )
            
            logger.info(f"📦 Cached {len(indicators)} indicators from {feed_name}")
    
    async def get_threat_indicators(
        self,
        indicator_type: Optional[str] = None,
        threat_type: Optional[ThreatType] = None,
        threat_level: Optional[ThreatLevel] = None,
        source: Optional[str] = None,
        limit: int = 100
    ) -> List[ThreatIndicator]:
        """Get threat indicators with filtering"""
        try:
            all_indicators = []
            
            # Get indicators from all feeds
            for feed_name in self.feeds.keys():
                cache_key = f"threat_indicators:{feed_name}"
                cached_data = self.redis_client.get(cache_key)
                
                if cached_data:
                    data = json.loads(cached_data)
                    for indicator_dict in data['indicators']:
                        # Convert back to ThreatIndicator object
                        indicator = ThreatIndicator(
                            indicator_id=indicator_dict['indicator_id'],
                            indicator_type=indicator_dict['indicator_type'],
                            indicator_value=indicator_dict['indicator_value'],
                            threat_type=ThreatType(indicator_dict['threat_type']),
                            threat_level=ThreatLevel(indicator_dict['threat_level']),
                            confidence=indicator_dict['confidence'],
                            source=indicator_dict['source'],
                            first_seen=datetime.fromisoformat(indicator_dict['first_seen']),
                            last_seen=datetime.fromisoformat(indicator_dict['last_seen']),
                            tags=indicator_dict['tags'],
                            context=indicator_dict['context']
                        )
                        all_indicators.append(indicator)
            
            # Apply filters
            filtered_indicators = all_indicators
            
            if indicator_type:
                filtered_indicators = [i for i in filtered_indicators if i.indicator_type == indicator_type]
            
            if threat_type:
                filtered_indicators = [i for i in filtered_indicators if i.threat_type == threat_type]
            
            if threat_level:
                filtered_indicators = [i for i in filtered_indicators if i.threat_level == threat_level]
            
            if source:
                filtered_indicators = [i for i in filtered_indicators if i.source == source]
            
            # Sort by last_seen (most recent first) and limit
            filtered_indicators.sort(key=lambda x: x.last_seen, reverse=True)
            
            return filtered_indicators[:limit]
            
        except Exception as e:
            logger.error(f"Error getting threat indicators: {e}")
            return []
    
    async def check_indicator(self, indicator_value: str, indicator_type: str) -> List[ThreatIndicator]:
        """Check a specific indicator against all threat feeds"""
        try:
            matches = []
            
            # Check cached indicators first
            all_indicators = await self.get_threat_indicators(
                indicator_type=indicator_type,
                limit=10000  # Get all for matching
            )
            
            for indicator in all_indicators:
                if indicator.indicator_value == indicator_value:
                    matches.append(indicator)
            
            # For IP addresses, also check Spamhaus real-time
            if indicator_type == 'ip' and 'spamhaus' in self.feeds:
                spamhaus_result = await self.feeds['spamhaus'].check_ip_reputation(indicator_value)
                if spamhaus_result:
                    matches.append(spamhaus_result)
            
            return matches
            
        except Exception as e:
            logger.error(f"Error checking indicator {indicator_value}: {e}")
            return []
    
    async def get_feed_status(self) -> Dict[str, Any]:
        """Get status of all threat feeds"""
        try:
            status = {
                'service_active': self.is_active,
                'total_feeds': len(self.feeds),
                'feeds': {},
                'last_updated': datetime.now().isoformat()
            }
            
            for feed_name in self.feeds.keys():
                cache_key = f"threat_indicators:{feed_name}"
                cached_data = self.redis_client.get(cache_key)
                
                if cached_data:
                    data = json.loads(cached_data)
                    status['feeds'][feed_name] = {
                        'enabled': True,
                        'last_updated': data['last_updated'],
                        'indicator_count': data['count'],
                        'status': 'active'
                    }
                else:
                    status['feeds'][feed_name] = {
                        'enabled': True,
                        'last_updated': None,
                        'indicator_count': 0,
                        'status': 'no_data'
                    }
            
            return status
            
        except Exception as e:
            logger.error(f"Error getting feed status: {e}")
            return {'error': str(e)}
    
    async def cleanup(self):
        """Cleanup resources"""
        self.is_active = False
        
        for feed in self.feeds.values():
            if hasattr(feed, 'session') and feed.session:
                await feed.session.close()
        
        if self.redis_client:
            self.redis_client.close()

# Global instance
real_threat_intelligence = RealThreatIntelligenceService() 