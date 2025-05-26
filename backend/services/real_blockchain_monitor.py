"""
⛓️ REAL BLOCKCHAIN MONITORING SERVICE
Production-ready blockchain monitoring with real network integrations including Hathor Network
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
from web3 import Web3
from web3.middleware import geth_poa_middleware
import websockets

logger = logging.getLogger(__name__)

class BlockchainNetwork(str, Enum):
    ETHEREUM = "ethereum"
    POLYGON = "polygon"
    BSC = "bsc"
    ARBITRUM = "arbitrum"
    OPTIMISM = "optimism"
    HATHOR = "hathor"

class TransactionRisk(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class BlockchainTransaction:
    """Real blockchain transaction data"""
    tx_hash: str
    block_number: int
    network: BlockchainNetwork
    from_address: str
    to_address: Optional[str]
    value: str
    gas_used: int
    gas_price: str
    timestamp: datetime
    risk_level: TransactionRisk
    risk_score: float
    threat_indicators: List[str]
    contract_interaction: bool
    token_transfers: List[Dict[str, Any]]
    
    def to_dict(self):
        return {
            **asdict(self),
            'network': self.network.value,
            'risk_level': self.risk_level.value,
            'timestamp': self.timestamp.isoformat()
        }

@dataclass
class SmartContractVulnerability:
    """Smart contract vulnerability detection result"""
    contract_address: str
    network: BlockchainNetwork
    vulnerability_type: str
    severity: str
    confidence: float
    description: str
    code_snippet: Optional[str]
    remediation: str
    detected_at: datetime
    
    def to_dict(self):
        return {
            **asdict(self),
            'network': self.network.value,
            'detected_at': self.detected_at.isoformat()
        }

class HathorNetworkMonitor:
    """Hathor Network blockchain monitoring integration"""
    
    def __init__(self, node_url: str = "https://node1.mainnet.hathor.network/v1a/"):
        self.node_url = node_url
        self.session = None
        self.websocket = None
        
    async def initialize(self):
        """Initialize Hathor Network connection"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30)
        )
        
        # Test connection
        try:
            async with self.session.get(f"{self.node_url}status") as response:
                if response.status == 200:
                    status = await response.json()
                    logger.info(f"✅ Connected to Hathor Network: {status.get('network', 'unknown')}")
                    return True
                else:
                    logger.error(f"❌ Failed to connect to Hathor Network: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Hathor Network connection error: {e}")
            return False
    
    async def get_latest_transactions(self, limit: int = 50) -> List[BlockchainTransaction]:
        """Get latest transactions from Hathor Network"""
        try:
            async with self.session.get(f"{self.node_url}transaction", params={"count": limit}) as response:
                if response.status == 200:
                    data = await response.json()
                    transactions = []
                    
                    for tx_data in data.get('transactions', []):
                        # Analyze transaction for risks
                        risk_score, risk_level, indicators = await self._analyze_hathor_transaction(tx_data)
                        
                        transaction = BlockchainTransaction(
                            tx_hash=tx_data['tx_id'],
                            block_number=tx_data.get('height', 0),
                            network=BlockchainNetwork.HATHOR,
                            from_address=tx_data.get('inputs', [{}])[0].get('tx_id', 'unknown'),
                            to_address=tx_data.get('outputs', [{}])[0].get('script', 'unknown'),
                            value=str(sum(output.get('value', 0) for output in tx_data.get('outputs', []))),
                            gas_used=0,  # Hathor is feeless
                            gas_price="0",
                            timestamp=datetime.fromtimestamp(tx_data.get('timestamp', 0)),
                            risk_level=risk_level,
                            risk_score=risk_score,
                            threat_indicators=indicators,
                            contract_interaction=False,  # Hathor doesn't have smart contracts yet
                            token_transfers=self._extract_hathor_token_transfers(tx_data)
                        )
                        transactions.append(transaction)
                    
                    return transactions
                else:
                    logger.error(f"Hathor API error: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching Hathor transactions: {e}")
            return []
    
    async def _analyze_hathor_transaction(self, tx_data: Dict) -> tuple[float, TransactionRisk, List[str]]:
        """Analyze Hathor transaction for security risks"""
        risk_score = 0.0
        indicators = []
        
        # Check transaction value
        total_value = sum(output.get('value', 0) for output in tx_data.get('outputs', []))
        if total_value > 1000000:  # Large value transactions (1M HTR)
            risk_score += 0.3
            indicators.append("large_value_transfer")
        
        # Check for unusual patterns
        inputs_count = len(tx_data.get('inputs', []))
        outputs_count = len(tx_data.get('outputs', []))
        
        if inputs_count > 10 or outputs_count > 10:
            risk_score += 0.2
            indicators.append("complex_transaction")
        
        # Check for token creation
        if tx_data.get('version', 0) == 2:  # Token creation transaction
            risk_score += 0.1
            indicators.append("token_creation")
        
        # Determine risk level
        if risk_score >= 0.7:
            risk_level = TransactionRisk.CRITICAL
        elif risk_score >= 0.5:
            risk_level = TransactionRisk.HIGH
        elif risk_score >= 0.3:
            risk_level = TransactionRisk.MEDIUM
        else:
            risk_level = TransactionRisk.LOW
        
        return risk_score, risk_level, indicators
    
    def _extract_hathor_token_transfers(self, tx_data: Dict) -> List[Dict[str, Any]]:
        """Extract token transfer information from Hathor transaction"""
        transfers = []
        
        # Check if this is a token transaction
        if tx_data.get('version', 0) == 2:
            for output in tx_data.get('outputs', []):
                if output.get('token_data', 0) > 0:
                    transfers.append({
                        'token_id': tx_data.get('hash', 'unknown'),
                        'value': output.get('value', 0),
                        'token_data': output.get('token_data', 0)
                    })
        
        return transfers
    
    async def get_network_stats(self) -> Dict[str, Any]:
        """Get Hathor Network statistics"""
        try:
            async with self.session.get(f"{self.node_url}status") as response:
                if response.status == 200:
                    status = await response.json()
                    return {
                        'network': status.get('network', 'unknown'),
                        'latest_block': status.get('latest_block', 0),
                        'peer_count': status.get('peer_count', 0),
                        'sync_state': status.get('state', 'unknown'),
                        'version': status.get('version', 'unknown')
                    }
                else:
                    return {'error': f'API error: {response.status}'}
        except Exception as e:
            return {'error': str(e)}

class EthereumMonitor:
    """Ethereum blockchain monitoring with production APIs"""
    
    def __init__(self, rpc_url: str, ws_url: Optional[str] = None):
        self.rpc_url = rpc_url
        self.ws_url = ws_url
        self.web3 = None
        self.session = None
        
    async def initialize(self):
        """Initialize Ethereum connection"""
        try:
            self.web3 = Web3(Web3.HTTPProvider(self.rpc_url))
            
            if self.web3.is_connected():
                latest_block = self.web3.eth.block_number
                logger.info(f"✅ Connected to Ethereum: Block {latest_block}")
                return True
            else:
                logger.error("❌ Failed to connect to Ethereum")
                return False
        except Exception as e:
            logger.error(f"❌ Ethereum connection error: {e}")
            return False
    
    async def get_latest_transactions(self, limit: int = 50) -> List[BlockchainTransaction]:
        """Get latest transactions from Ethereum"""
        try:
            latest_block = self.web3.eth.get_block('latest', full_transactions=True)
            transactions = []
            
            for tx in latest_block.transactions[:limit]:
                # Get transaction receipt for gas used
                receipt = self.web3.eth.get_transaction_receipt(tx.hash)
                
                # Analyze transaction for risks
                risk_score, risk_level, indicators = await self._analyze_ethereum_transaction(tx, receipt)
                
                transaction = BlockchainTransaction(
                    tx_hash=tx.hash.hex(),
                    block_number=tx.blockNumber,
                    network=BlockchainNetwork.ETHEREUM,
                    from_address=tx['from'],
                    to_address=tx.to,
                    value=str(tx.value),
                    gas_used=receipt.gasUsed,
                    gas_price=str(tx.gasPrice),
                    timestamp=datetime.fromtimestamp(latest_block.timestamp),
                    risk_level=risk_level,
                    risk_score=risk_score,
                    threat_indicators=indicators,
                    contract_interaction=tx.to is not None and len(self.web3.eth.get_code(tx.to)) > 0,
                    token_transfers=await self._extract_token_transfers(receipt)
                )
                transactions.append(transaction)
            
            return transactions
        except Exception as e:
            logger.error(f"Error fetching Ethereum transactions: {e}")
            return []
    
    async def _analyze_ethereum_transaction(self, tx, receipt) -> tuple[float, TransactionRisk, List[str]]:
        """Analyze Ethereum transaction for security risks"""
        risk_score = 0.0
        indicators = []
        
        # High value transactions
        if tx.value > self.web3.to_wei(10, 'ether'):
            risk_score += 0.3
            indicators.append("high_value_transfer")
        
        # Failed transactions
        if receipt.status == 0:
            risk_score += 0.4
            indicators.append("failed_transaction")
        
        # High gas usage (potential complex operations)
        if receipt.gasUsed > 500000:
            risk_score += 0.2
            indicators.append("high_gas_usage")
        
        # Contract creation
        if tx.to is None:
            risk_score += 0.1
            indicators.append("contract_deployment")
        
        # Multiple logs (complex interactions)
        if len(receipt.logs) > 5:
            risk_score += 0.2
            indicators.append("complex_interaction")
        
        # Determine risk level
        if risk_score >= 0.7:
            risk_level = TransactionRisk.CRITICAL
        elif risk_score >= 0.5:
            risk_level = TransactionRisk.HIGH
        elif risk_score >= 0.3:
            risk_level = TransactionRisk.MEDIUM
        else:
            risk_level = TransactionRisk.LOW
        
        return risk_score, risk_level, indicators
    
    async def _extract_token_transfers(self, receipt) -> List[Dict[str, Any]]:
        """Extract ERC-20 token transfers from transaction receipt"""
        transfers = []
        
        # ERC-20 Transfer event signature
        transfer_signature = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
        
        for log in receipt.logs:
            if len(log.topics) > 0 and log.topics[0].hex() == transfer_signature:
                if len(log.topics) >= 3:
                    transfers.append({
                        'contract': log.address,
                        'from': '0x' + log.topics[1].hex()[-40:],
                        'to': '0x' + log.topics[2].hex()[-40:],
                        'value': int(log.data, 16) if log.data else 0
                    })
        
        return transfers
    
    async def analyze_smart_contract(self, contract_address: str) -> List[SmartContractVulnerability]:
        """Analyze smart contract for vulnerabilities"""
        vulnerabilities = []
        
        try:
            # Get contract code
            code = self.web3.eth.get_code(contract_address)
            
            if len(code) == 0:
                return vulnerabilities
            
            # Basic static analysis patterns
            code_str = code.hex()
            
            # Check for potential reentrancy
            if 'call' in code_str and 'sstore' in code_str:
                vulnerabilities.append(SmartContractVulnerability(
                    contract_address=contract_address,
                    network=BlockchainNetwork.ETHEREUM,
                    vulnerability_type="potential_reentrancy",
                    severity="medium",
                    confidence=0.6,
                    description="Contract contains call and storage operations that may be vulnerable to reentrancy",
                    code_snippet=None,
                    remediation="Implement checks-effects-interactions pattern",
                    detected_at=datetime.now()
                ))
            
            # Check for unchecked external calls
            if 'call' in code_str and 'iszero' not in code_str:
                vulnerabilities.append(SmartContractVulnerability(
                    contract_address=contract_address,
                    network=BlockchainNetwork.ETHEREUM,
                    vulnerability_type="unchecked_external_call",
                    severity="low",
                    confidence=0.4,
                    description="Contract may contain unchecked external calls",
                    code_snippet=None,
                    remediation="Always check return values of external calls",
                    detected_at=datetime.now()
                ))
            
        except Exception as e:
            logger.error(f"Error analyzing contract {contract_address}: {e}")
        
        return vulnerabilities

class PolygonMonitor(EthereumMonitor):
    """Polygon blockchain monitoring (inherits from Ethereum)"""
    
    async def initialize(self):
        """Initialize Polygon connection"""
        try:
            self.web3 = Web3(Web3.HTTPProvider(self.rpc_url))
            # Add PoA middleware for Polygon
            self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
            
            if self.web3.is_connected():
                latest_block = self.web3.eth.block_number
                logger.info(f"✅ Connected to Polygon: Block {latest_block}")
                return True
            else:
                logger.error("❌ Failed to connect to Polygon")
                return False
        except Exception as e:
            logger.error(f"❌ Polygon connection error: {e}")
            return False

class RealBlockchainMonitoringService:
    """Production blockchain monitoring service with real network integrations"""
    
    def __init__(self):
        self.monitors = {}
        self.redis_client = None
        self.is_active = False
        self.cache_ttl = 300  # 5 minutes cache
        
        # Network configurations from environment
        self.network_configs = {
            BlockchainNetwork.ETHEREUM: {
                'enabled': os.getenv('ETHEREUM_RPC_URL') is not None,
                'rpc_url': os.getenv('ETHEREUM_RPC_URL'),
                'ws_url': os.getenv('ETHEREUM_WS_URL'),
                'monitor_class': EthereumMonitor
            },
            BlockchainNetwork.POLYGON: {
                'enabled': os.getenv('POLYGON_RPC_URL') is not None,
                'rpc_url': os.getenv('POLYGON_RPC_URL'),
                'ws_url': os.getenv('POLYGON_WS_URL'),
                'monitor_class': PolygonMonitor
            },
            BlockchainNetwork.HATHOR: {
                'enabled': True,  # Always enabled (public API)
                'node_url': os.getenv('HATHOR_NODE_URL', 'https://node1.mainnet.hathor.network/v1a/'),
                'monitor_class': HathorNetworkMonitor
            }
        }
    
    async def initialize(self):
        """Initialize blockchain monitoring service"""
        try:
            logger.info("⛓️ Initializing Real Blockchain Monitoring Service...")
            
            # Initialize Redis cache
            redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
            self.redis_client = redis.from_url(redis_url, decode_responses=True)
            
            # Initialize enabled network monitors
            for network, config in self.network_configs.items():
                if config['enabled']:
                    if network == BlockchainNetwork.HATHOR:
                        monitor = HathorNetworkMonitor(config['node_url'])
                    else:
                        monitor = config['monitor_class'](config['rpc_url'], config.get('ws_url'))
                    
                    if await monitor.initialize():
                        self.monitors[network] = monitor
                        logger.info(f"✅ {network.value} monitor initialized")
                    else:
                        logger.error(f"❌ Failed to initialize {network.value} monitor")
            
            self.is_active = True
            logger.info(f"✅ Real Blockchain Monitoring Service initialized with {len(self.monitors)} networks")
            
            # Start background monitoring tasks
            asyncio.create_task(self._start_monitoring())
            
        except Exception as e:
            logger.error(f"❌ Error initializing Real Blockchain Monitoring Service: {e}")
            raise
    
    async def _start_monitoring(self):
        """Start background monitoring tasks for all networks"""
        tasks = []
        
        for network, monitor in self.monitors.items():
            task = asyncio.create_task(self._monitor_network_periodically(network, monitor))
            tasks.append(task)
        
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _monitor_network_periodically(self, network: BlockchainNetwork, monitor):
        """Periodically monitor a specific blockchain network"""
        while self.is_active:
            try:
                logger.info(f"🔄 Monitoring {network.value} network...")
                
                # Get latest transactions
                transactions = await monitor.get_latest_transactions(limit=20)
                
                if transactions:
                    # Cache transactions
                    cache_key = f"blockchain_transactions:{network.value}"
                    cached_data = {
                        'transactions': [tx.to_dict() for tx in transactions],
                        'last_updated': datetime.now().isoformat(),
                        'count': len(transactions)
                    }
                    
                    self.redis_client.setex(
                        cache_key,
                        self.cache_ttl,
                        json.dumps(cached_data)
                    )
                    
                    # Check for high-risk transactions
                    high_risk_count = sum(1 for tx in transactions if tx.risk_level in [TransactionRisk.HIGH, TransactionRisk.CRITICAL])
                    if high_risk_count > 0:
                        logger.warning(f"⚠️ {high_risk_count} high-risk transactions detected on {network.value}")
                
                logger.info(f"✅ Monitored {network.value}: {len(transactions)} transactions")
                
            except Exception as e:
                logger.error(f"❌ Error monitoring {network.value}: {e}")
            
            await asyncio.sleep(30)  # Monitor every 30 seconds
    
    async def get_recent_transactions(
        self,
        network: Optional[BlockchainNetwork] = None,
        risk_level: Optional[TransactionRisk] = None,
        limit: int = 100
    ) -> List[BlockchainTransaction]:
        """Get recent transactions with filtering"""
        try:
            all_transactions = []
            
            # Get transactions from specified network or all networks
            networks_to_check = [network] if network else list(self.monitors.keys())
            
            for net in networks_to_check:
                cache_key = f"blockchain_transactions:{net.value}"
                cached_data = self.redis_client.get(cache_key)
                
                if cached_data:
                    data = json.loads(cached_data)
                    for tx_dict in data['transactions']:
                        # Convert back to BlockchainTransaction object
                        transaction = BlockchainTransaction(
                            tx_hash=tx_dict['tx_hash'],
                            block_number=tx_dict['block_number'],
                            network=BlockchainNetwork(tx_dict['network']),
                            from_address=tx_dict['from_address'],
                            to_address=tx_dict['to_address'],
                            value=tx_dict['value'],
                            gas_used=tx_dict['gas_used'],
                            gas_price=tx_dict['gas_price'],
                            timestamp=datetime.fromisoformat(tx_dict['timestamp']),
                            risk_level=TransactionRisk(tx_dict['risk_level']),
                            risk_score=tx_dict['risk_score'],
                            threat_indicators=tx_dict['threat_indicators'],
                            contract_interaction=tx_dict['contract_interaction'],
                            token_transfers=tx_dict['token_transfers']
                        )
                        all_transactions.append(transaction)
            
            # Apply risk level filter
            if risk_level:
                all_transactions = [tx for tx in all_transactions if tx.risk_level == risk_level]
            
            # Sort by timestamp (most recent first) and limit
            all_transactions.sort(key=lambda x: x.timestamp, reverse=True)
            
            return all_transactions[:limit]
            
        except Exception as e:
            logger.error(f"Error getting recent transactions: {e}")
            return []
    
    async def analyze_contract(self, contract_address: str, network: BlockchainNetwork) -> List[SmartContractVulnerability]:
        """Analyze smart contract for vulnerabilities"""
        try:
            if network not in self.monitors:
                logger.error(f"Network {network.value} not available")
                return []
            
            monitor = self.monitors[network]
            
            # Only Ethereum-based networks support smart contract analysis
            if hasattr(monitor, 'analyze_smart_contract'):
                vulnerabilities = await monitor.analyze_smart_contract(contract_address)
                
                # Cache results
                cache_key = f"contract_analysis:{network.value}:{contract_address}"
                cached_data = {
                    'vulnerabilities': [vuln.to_dict() for vuln in vulnerabilities],
                    'analyzed_at': datetime.now().isoformat(),
                    'contract_address': contract_address,
                    'network': network.value
                }
                
                self.redis_client.setex(
                    cache_key,
                    3600,  # Cache for 1 hour
                    json.dumps(cached_data)
                )
                
                return vulnerabilities
            else:
                logger.info(f"Smart contract analysis not supported for {network.value}")
                return []
                
        except Exception as e:
            logger.error(f"Error analyzing contract {contract_address} on {network.value}: {e}")
            return []
    
    async def get_network_statistics(self) -> Dict[str, Any]:
        """Get statistics for all monitored networks"""
        try:
            stats = {
                'active_networks': len(self.monitors),
                'networks': {},
                'total_transactions_monitored': 0,
                'high_risk_transactions': 0,
                'last_updated': datetime.now().isoformat()
            }
            
            for network, monitor in self.monitors.items():
                # Get network-specific stats
                if hasattr(monitor, 'get_network_stats'):
                    network_stats = await monitor.get_network_stats()
                else:
                    network_stats = {'status': 'active'}
                
                # Get cached transaction data
                cache_key = f"blockchain_transactions:{network.value}"
                cached_data = self.redis_client.get(cache_key)
                
                if cached_data:
                    data = json.loads(cached_data)
                    tx_count = data['count']
                    high_risk_count = sum(
                        1 for tx in data['transactions'] 
                        if tx['risk_level'] in ['high', 'critical']
                    )
                    
                    stats['total_transactions_monitored'] += tx_count
                    stats['high_risk_transactions'] += high_risk_count
                    
                    stats['networks'][network.value] = {
                        **network_stats,
                        'recent_transactions': tx_count,
                        'high_risk_transactions': high_risk_count,
                        'last_updated': data['last_updated']
                    }
                else:
                    stats['networks'][network.value] = {
                        **network_stats,
                        'recent_transactions': 0,
                        'high_risk_transactions': 0,
                        'last_updated': None
                    }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting network statistics: {e}")
            return {'error': str(e)}
    
    async def get_threat_summary(self) -> Dict[str, Any]:
        """Get threat summary across all networks"""
        try:
            summary = {
                'total_threats': 0,
                'threats_by_network': {},
                'threats_by_type': {},
                'recent_threats': [],
                'threat_trends': [],
                'last_updated': datetime.now().isoformat()
            }
            
            # Analyze recent transactions for threats
            recent_transactions = await self.get_recent_transactions(limit=500)
            
            for tx in recent_transactions:
                if tx.risk_level in [TransactionRisk.HIGH, TransactionRisk.CRITICAL]:
                    summary['total_threats'] += 1
                    
                    # Count by network
                    network_key = tx.network.value
                    if network_key not in summary['threats_by_network']:
                        summary['threats_by_network'][network_key] = 0
                    summary['threats_by_network'][network_key] += 1
                    
                    # Count by threat indicators
                    for indicator in tx.threat_indicators:
                        if indicator not in summary['threats_by_type']:
                            summary['threats_by_type'][indicator] = 0
                        summary['threats_by_type'][indicator] += 1
                    
                    # Add to recent threats (limit to 10)
                    if len(summary['recent_threats']) < 10:
                        summary['recent_threats'].append({
                            'tx_hash': tx.tx_hash,
                            'network': tx.network.value,
                            'risk_level': tx.risk_level.value,
                            'risk_score': tx.risk_score,
                            'indicators': tx.threat_indicators,
                            'timestamp': tx.timestamp.isoformat()
                        })
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting threat summary: {e}")
            return {'error': str(e)}
    
    async def cleanup(self):
        """Cleanup resources"""
        self.is_active = False
        
        for monitor in self.monitors.values():
            if hasattr(monitor, 'session') and monitor.session:
                await monitor.session.close()
        
        if self.redis_client:
            self.redis_client.close()

# Global instance
real_blockchain_monitor = RealBlockchainMonitoringService() 