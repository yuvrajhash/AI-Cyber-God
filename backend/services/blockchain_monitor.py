"""
🔗 QUANTUM-AI CYBER GOD - BLOCKCHAIN MONITOR
Real-time blockchain monitoring and analysis service
"""

import asyncio
import json
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import aiohttp
import websockets
from web3 import Web3
try:
    from web3.middleware import geth_poa_middleware
except ImportError:
    # For newer versions of web3.py
    try:
        from web3.middleware.geth_poa import geth_poa_middleware
    except ImportError:
        from web3.middleware.proof_of_authority import ExtraDataToPOAMiddleware as geth_poa_middleware
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class BlockchainEvent:
    """Blockchain event data structure"""
    event_id: str
    chain_id: int
    block_number: int
    transaction_hash: str
    event_type: str
    contract_address: str
    timestamp: datetime
    risk_score: float
    details: Dict[str, Any]
    
    def to_dict(self):
        return {
            **asdict(self),
            'timestamp': self.timestamp.isoformat()
        }

@dataclass
class ChainConfig:
    """Blockchain configuration"""
    name: str
    chain_id: int
    rpc_url: str
    ws_url: Optional[str]
    explorer_api: str
    native_token: str
    is_testnet: bool

class BlockchainMonitor:
    """Advanced blockchain monitoring system"""
    
    def __init__(self):
        self.chains = self._initialize_chains()
        self.web3_connections = {}
        self.ws_connections = {}
        self.monitoring_active = False
        self.event_queue = asyncio.Queue()
        self.risk_patterns = self._load_risk_patterns()
        
    def _initialize_chains(self) -> Dict[int, ChainConfig]:
        """Initialize supported blockchain configurations"""
        return {
            1: ChainConfig(
                name="Ethereum Mainnet",
                chain_id=1,
                rpc_url="https://eth-mainnet.g.alchemy.com/v2/demo",
                ws_url="wss://eth-mainnet.g.alchemy.com/v2/demo",
                explorer_api="https://api.etherscan.io/api",
                native_token="ETH",
                is_testnet=False
            ),
            11155111: ChainConfig(
                name="Ethereum Sepolia",
                chain_id=11155111,
                rpc_url="https://eth-sepolia.g.alchemy.com/v2/demo",
                ws_url="wss://eth-sepolia.g.alchemy.com/v2/demo",
                explorer_api="https://api-sepolia.etherscan.io/api",
                native_token="ETH",
                is_testnet=True
            ),
            137: ChainConfig(
                name="Polygon Mainnet",
                chain_id=137,
                rpc_url="https://polygon-rpc.com",
                ws_url="wss://polygon-rpc.com",
                explorer_api="https://api.polygonscan.com/api",
                native_token="MATIC",
                is_testnet=False
            ),
            56: ChainConfig(
                name="BSC Mainnet",
                chain_id=56,
                rpc_url="https://bsc-dataseed1.binance.org",
                ws_url="wss://bsc-ws-node.nariox.org:443",
                explorer_api="https://api.bscscan.com/api",
                native_token="BNB",
                is_testnet=False
            )
        }
    
    def _load_risk_patterns(self) -> Dict[str, Any]:
        """Load risk detection patterns"""
        return {
            "flash_loan_indicators": [
                "flashLoan",
                "borrow",
                "repay",
                "arbitrage"
            ],
            "reentrancy_patterns": [
                "call.value",
                "transfer",
                "send",
                "delegatecall"
            ],
            "suspicious_amounts": {
                "min_eth": 10,  # ETH
                "min_usd": 50000  # USD equivalent
            },
            "time_windows": {
                "flash_loan": 1,  # seconds
                "reentrancy": 5,  # seconds
                "sandwich": 3  # blocks
            }
        }
    
    async def initialize_connections(self, chain_ids: List[int] = None):
        """Initialize Web3 connections for specified chains"""
        if chain_ids is None:
            chain_ids = [1, 11155111, 137]  # Default to major chains
            
        for chain_id in chain_ids:
            if chain_id not in self.chains:
                logger.warning(f"Chain {chain_id} not supported")
                continue
                
            chain = self.chains[chain_id]
            try:
                # Initialize Web3 connection
                web3 = Web3(Web3.HTTPProvider(chain.rpc_url))
                
                # Add PoA middleware for some chains
                if chain_id in [56, 137]:
                    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
                
                if web3.is_connected():
                    self.web3_connections[chain_id] = web3
                    logger.info(f"Connected to {chain.name}")
                else:
                    logger.error(f"Failed to connect to {chain.name}")
                    
            except Exception as e:
                logger.error(f"Error connecting to {chain.name}: {e}")
    
    async def start_monitoring(self, chain_ids: List[int] = None):
        """Start real-time blockchain monitoring"""
        if not self.web3_connections:
            await self.initialize_connections(chain_ids)
        
        self.monitoring_active = True
        logger.info("Starting blockchain monitoring...")
        
        # Start monitoring tasks for each chain
        tasks = []
        for chain_id, web3 in self.web3_connections.items():
            tasks.append(asyncio.create_task(self._monitor_chain(chain_id, web3)))
            tasks.append(asyncio.create_task(self._monitor_mempool(chain_id, web3)))
        
        # Start event processing task
        tasks.append(asyncio.create_task(self._process_events()))
        
        await asyncio.gather(*tasks)
    
    async def _monitor_chain(self, chain_id: int, web3: Web3):
        """Monitor blockchain for new blocks and transactions"""
        chain = self.chains[chain_id]
        last_block = web3.eth.block_number
        
        while self.monitoring_active:
            try:
                current_block = web3.eth.block_number
                
                if current_block > last_block:
                    # Process new blocks
                    for block_num in range(last_block + 1, current_block + 1):
                        await self._analyze_block(chain_id, web3, block_num)
                    
                    last_block = current_block
                
                await asyncio.sleep(2)  # Check every 2 seconds
                
            except Exception as e:
                logger.error(f"Error monitoring {chain.name}: {e}")
                await asyncio.sleep(5)
    
    async def _monitor_mempool(self, chain_id: int, web3: Web3):
        """Monitor mempool for pending transactions"""
        chain = self.chains[chain_id]
        
        while self.monitoring_active:
            try:
                # Get pending transactions (if supported)
                pending_filter = web3.eth.filter('pending')
                
                for tx_hash in pending_filter.get_new_entries():
                    await self._analyze_pending_transaction(chain_id, web3, tx_hash)
                
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Error monitoring mempool for {chain.name}: {e}")
                await asyncio.sleep(10)
    
    async def _analyze_block(self, chain_id: int, web3: Web3, block_number: int):
        """Analyze a specific block for security events"""
        try:
            block = web3.eth.get_block(block_number, full_transactions=True)
            
            for tx in block.transactions:
                await self._analyze_transaction(chain_id, web3, tx, block_number)
                
        except Exception as e:
            logger.error(f"Error analyzing block {block_number}: {e}")
    
    async def _analyze_transaction(self, chain_id: int, web3: Web3, tx, block_number: int):
        """Analyze individual transaction for security risks"""
        try:
            # Get transaction receipt for logs
            receipt = web3.eth.get_transaction_receipt(tx.hash)
            
            # Calculate risk score
            risk_score = await self._calculate_risk_score(chain_id, web3, tx, receipt)
            
            if risk_score > 0.3:  # Only process medium+ risk transactions
                event = BlockchainEvent(
                    event_id=f"{chain_id}_{tx.hash.hex()}",
                    chain_id=chain_id,
                    block_number=block_number,
                    transaction_hash=tx.hash.hex(),
                    event_type=self._classify_transaction(tx, receipt),
                    contract_address=tx.to.hex() if tx.to else "",
                    timestamp=datetime.now(),
                    risk_score=risk_score,
                    details={
                        "value": str(tx.value),
                        "gas_used": receipt.gasUsed,
                        "gas_price": str(tx.gasPrice),
                        "from": tx["from"],
                        "to": tx.to.hex() if tx.to else None,
                        "logs_count": len(receipt.logs)
                    }
                )
                
                await self.event_queue.put(event)
                
        except Exception as e:
            logger.error(f"Error analyzing transaction {tx.hash.hex()}: {e}")
    
    async def _analyze_pending_transaction(self, chain_id: int, web3: Web3, tx_hash):
        """Analyze pending transaction for front-running detection"""
        try:
            tx = web3.eth.get_transaction(tx_hash)
            
            # Check for MEV opportunities
            if self._detect_mev_opportunity(tx):
                event = BlockchainEvent(
                    event_id=f"{chain_id}_{tx_hash.hex()}_pending",
                    chain_id=chain_id,
                    block_number=0,  # Pending
                    transaction_hash=tx_hash.hex(),
                    event_type="MEV_OPPORTUNITY",
                    contract_address=tx.to.hex() if tx.to else "",
                    timestamp=datetime.now(),
                    risk_score=0.8,
                    details={
                        "status": "pending",
                        "gas_price": str(tx.gasPrice),
                        "value": str(tx.value)
                    }
                )
                
                await self.event_queue.put(event)
                
        except Exception as e:
            logger.error(f"Error analyzing pending transaction: {e}")
    
    async def _calculate_risk_score(self, chain_id: int, web3: Web3, tx, receipt) -> float:
        """Calculate risk score for a transaction"""
        risk_score = 0.0
        
        # High value transactions
        if tx.value > web3.to_wei(10, 'ether'):
            risk_score += 0.3
        
        # Contract interactions
        if tx.to and len(web3.eth.get_code(tx.to)) > 0:
            risk_score += 0.2
        
        # Multiple logs (complex interactions)
        if len(receipt.logs) > 5:
            risk_score += 0.2
        
        # High gas usage
        if receipt.gasUsed > 500000:
            risk_score += 0.2
        
        # Failed transactions
        if receipt.status == 0:
            risk_score += 0.4
        
        return min(risk_score, 1.0)
    
    def _classify_transaction(self, tx, receipt) -> str:
        """Classify transaction type based on patterns"""
        if receipt.status == 0:
            return "FAILED_TRANSACTION"
        
        if tx.value > 0 and tx.to:
            return "TOKEN_TRANSFER"
        
        if len(receipt.logs) > 0:
            return "CONTRACT_INTERACTION"
        
        if tx.to is None:
            return "CONTRACT_DEPLOYMENT"
        
        return "STANDARD_TRANSFER"
    
    def _detect_mev_opportunity(self, tx) -> bool:
        """Detect potential MEV opportunities"""
        # Simple MEV detection based on gas price and value
        if tx.gasPrice > Web3.to_wei(100, 'gwei') and tx.value > Web3.to_wei(1, 'ether'):
            return True
        return False
    
    async def _process_events(self):
        """Process blockchain events and trigger alerts"""
        while self.monitoring_active:
            try:
                event = await asyncio.wait_for(self.event_queue.get(), timeout=1.0)
                
                # Process the event
                await self._handle_security_event(event)
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error processing events: {e}")
    
    async def _handle_security_event(self, event: BlockchainEvent):
        """Handle detected security events"""
        logger.info(f"Security event detected: {event.event_type} (Risk: {event.risk_score})")
        
        # Here you would typically:
        # 1. Store in database
        # 2. Send alerts
        # 3. Update real-time dashboard
        # 4. Trigger automated responses
        
        if event.risk_score > 0.8:
            logger.warning(f"HIGH RISK EVENT: {event.transaction_hash}")
    
    async def get_real_time_stats(self) -> Dict[str, Any]:
        """Get real-time blockchain monitoring statistics"""
        stats = {
            "monitoring_active": self.monitoring_active,
            "connected_chains": len(self.web3_connections),
            "chains": {},
            "total_events_processed": 0,
            "high_risk_events": 0,
            "last_update": datetime.now().isoformat()
        }
        
        for chain_id, web3 in self.web3_connections.items():
            chain = self.chains[chain_id]
            try:
                latest_block = web3.eth.block_number
                stats["chains"][chain.name] = {
                    "chain_id": chain_id,
                    "latest_block": latest_block,
                    "connected": True,
                    "is_testnet": chain.is_testnet
                }
            except Exception as e:
                stats["chains"][chain.name] = {
                    "chain_id": chain_id,
                    "connected": False,
                    "error": str(e)
                }
        
        return stats
    
    async def analyze_smart_contract(self, chain_id: int, contract_address: str) -> Dict[str, Any]:
        """Analyze smart contract for vulnerabilities"""
        if chain_id not in self.web3_connections:
            raise ValueError(f"Chain {chain_id} not connected")
        
        web3 = self.web3_connections[chain_id]
        
        try:
            # Get contract code
            code = web3.eth.get_code(contract_address)
            
            if len(code) == 0:
                return {"error": "No contract found at address"}
            
            # Basic vulnerability analysis
            vulnerabilities = []
            risk_score = 0.0
            
            # Check for common vulnerability patterns
            code_str = code.hex()
            
            # Reentrancy check
            if "call" in code_str.lower():
                vulnerabilities.append({
                    "type": "POTENTIAL_REENTRANCY",
                    "severity": "HIGH",
                    "description": "Contract contains external calls that may be vulnerable to reentrancy"
                })
                risk_score += 0.4
            
            # Integer overflow check (for older contracts)
            if "add" in code_str.lower() or "mul" in code_str.lower():
                vulnerabilities.append({
                    "type": "POTENTIAL_OVERFLOW",
                    "severity": "MEDIUM",
                    "description": "Contract may be vulnerable to integer overflow"
                })
                risk_score += 0.2
            
            # Unchecked external calls
            if "call" in code_str.lower() and "require" not in code_str.lower():
                vulnerabilities.append({
                    "type": "UNCHECKED_CALL",
                    "severity": "HIGH",
                    "description": "Contract contains unchecked external calls"
                })
                risk_score += 0.3
            
            return {
                "contract_address": contract_address,
                "chain_id": chain_id,
                "code_size": len(code),
                "vulnerabilities": vulnerabilities,
                "risk_score": min(risk_score, 1.0),
                "analysis_timestamp": datetime.now().isoformat(),
                "recommendations": self._generate_recommendations(vulnerabilities)
            }
            
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _generate_recommendations(self, vulnerabilities: List[Dict]) -> List[str]:
        """Generate security recommendations based on vulnerabilities"""
        recommendations = []
        
        for vuln in vulnerabilities:
            if vuln["type"] == "POTENTIAL_REENTRANCY":
                recommendations.append("Implement reentrancy guards using OpenZeppelin's ReentrancyGuard")
            elif vuln["type"] == "POTENTIAL_OVERFLOW":
                recommendations.append("Use SafeMath library or Solidity 0.8+ for automatic overflow protection")
            elif vuln["type"] == "UNCHECKED_CALL":
                recommendations.append("Always check return values of external calls")
        
        if not recommendations:
            recommendations.append("Contract appears to follow basic security practices")
        
        return recommendations
    
    async def stop_monitoring(self):
        """Stop blockchain monitoring"""
        self.monitoring_active = False
        logger.info("Blockchain monitoring stopped")

# Global monitor instance
blockchain_monitor = BlockchainMonitor() 