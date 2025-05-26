"""
🛡️ QUANTUM-AI CYBER GOD - API RATE LIMITER SERVICE
Enterprise-grade rate limiting with multi-tier support and advanced monitoring
"""

import asyncio
import time
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict, deque
from enum import Enum
import redis.asyncio as redis
from dataclasses import dataclass, asdict
import hashlib

logger = logging.getLogger(__name__)

class RateLimitTier(str, Enum):
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    ENTERPRISE_PLUS = "enterprise_plus"

class RateLimitType(str, Enum):
    PER_MINUTE = "per_minute"
    PER_HOUR = "per_hour"
    PER_DAY = "per_day"
    BURST = "burst"

@dataclass
class RateLimitConfig:
    requests_per_minute: int
    requests_per_hour: int
    requests_per_day: int
    burst_limit: int
    burst_window: int  # seconds
    
@dataclass
class RateLimitStatus:
    allowed: bool
    remaining: int
    reset_time: int
    retry_after: Optional[int] = None
    tier: str = ""
    endpoint: str = ""

class TokenBucket:
    """Token bucket implementation for rate limiting"""
    
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refill = time.time()
    
    def consume(self, tokens: int = 1) -> bool:
        """Try to consume tokens from bucket"""
        self._refill()
        
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False
    
    def _refill(self):
        """Refill tokens based on time elapsed"""
        now = time.time()
        elapsed = now - self.last_refill
        tokens_to_add = elapsed * self.refill_rate
        
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now

class APIRateLimiter:
    """Enterprise API Rate Limiter with multi-tier support"""
    
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self.local_buckets: Dict[str, TokenBucket] = {}
        self.rate_limit_configs = self._initialize_rate_limits()
        self.violation_tracking: Dict[str, List[float]] = defaultdict(list)
        self.blocked_ips: Dict[str, float] = {}  # IP -> unblock_time
        self.suspicious_patterns: Dict[str, int] = defaultdict(int)
        
    def _initialize_rate_limits(self) -> Dict[RateLimitTier, RateLimitConfig]:
        """Initialize rate limit configurations for different tiers"""
        return {
            RateLimitTier.STARTER: RateLimitConfig(
                requests_per_minute=100,
                requests_per_hour=5000,
                requests_per_day=50000,
                burst_limit=20,
                burst_window=10
            ),
            RateLimitTier.PROFESSIONAL: RateLimitConfig(
                requests_per_minute=500,
                requests_per_hour=25000,
                requests_per_day=500000,
                burst_limit=100,
                burst_window=10
            ),
            RateLimitTier.ENTERPRISE: RateLimitConfig(
                requests_per_minute=2000,
                requests_per_hour=100000,
                requests_per_day=2000000,
                burst_limit=500,
                burst_window=10
            ),
            RateLimitTier.ENTERPRISE_PLUS: RateLimitConfig(
                requests_per_minute=10000,
                requests_per_hour=500000,
                requests_per_day=10000000,
                burst_limit=2000,
                burst_window=10
            )
        }
    
    async def initialize(self):
        """Initialize the rate limiter service"""
        try:
            # Try to connect to Redis for distributed rate limiting
            self.redis_client = redis.Redis(
                host='localhost',
                port=6379,
                decode_responses=True,
                socket_connect_timeout=5
            )
            await self.redis_client.ping()
            logger.info("✅ Connected to Redis for distributed rate limiting")
            
        except Exception as e:
            logger.warning(f"⚠️ Redis not available, using local rate limiting: {e}")
            self.redis_client = None
        
        logger.info("🛡️ API Rate Limiter initialized")
    
    async def check_rate_limit(
        self, 
        tenant_id: str, 
        endpoint: str, 
        tier: RateLimitTier,
        client_ip: str = "unknown",
        user_id: Optional[str] = None
    ) -> RateLimitStatus:
        """Check if request is within rate limits"""
        
        # Check if IP is blocked
        if await self._is_ip_blocked(client_ip):
            return RateLimitStatus(
                allowed=False,
                remaining=0,
                reset_time=int(self.blocked_ips.get(client_ip, time.time() + 3600)),
                retry_after=int(self.blocked_ips.get(client_ip, time.time() + 3600) - time.time()),
                tier=tier.value,
                endpoint=endpoint
            )
        
        config = self.rate_limit_configs[tier]
        current_time = time.time()
        
        # Create unique keys for different rate limit windows
        minute_key = f"{tenant_id}:{endpoint}:minute:{int(current_time // 60)}"
        hour_key = f"{tenant_id}:{endpoint}:hour:{int(current_time // 3600)}"
        day_key = f"{tenant_id}:{endpoint}:day:{int(current_time // 86400)}"
        burst_key = f"{tenant_id}:{endpoint}:burst"
        
        # Check all rate limit windows
        checks = [
            (minute_key, config.requests_per_minute, 60),
            (hour_key, config.requests_per_hour, 3600),
            (day_key, config.requests_per_day, 86400)
        ]
        
        for key, limit, window in checks:
            if self.redis_client:
                current_count = await self._redis_check_and_increment(key, window)
            else:
                current_count = await self._local_check_and_increment(key, window)
            
            if current_count > limit:
                # Rate limit exceeded
                await self._record_violation(tenant_id, client_ip, endpoint)
                
                return RateLimitStatus(
                    allowed=False,
                    remaining=0,
                    reset_time=int(current_time + window),
                    retry_after=window,
                    tier=tier.value,
                    endpoint=endpoint
                )
        
        # Check burst limit using token bucket
        if not await self._check_burst_limit(burst_key, config):
            await self._record_violation(tenant_id, client_ip, endpoint)
            
            return RateLimitStatus(
                allowed=False,
                remaining=0,
                reset_time=int(current_time + config.burst_window),
                retry_after=config.burst_window,
                tier=tier.value,
                endpoint=endpoint
            )
        
        # Calculate remaining requests (use minute window as reference)
        if self.redis_client:
            minute_count = await self._redis_get_count(minute_key)
        else:
            minute_count = await self._local_get_count(minute_key)
        
        remaining = max(0, config.requests_per_minute - minute_count)
        
        return RateLimitStatus(
            allowed=True,
            remaining=remaining,
            reset_time=int((current_time // 60 + 1) * 60),
            tier=tier.value,
            endpoint=endpoint
        )
    
    async def _redis_check_and_increment(self, key: str, window: int) -> int:
        """Check and increment counter using Redis"""
        pipe = self.redis_client.pipeline()
        pipe.incr(key)
        pipe.expire(key, window)
        results = await pipe.execute()
        return results[0]
    
    async def _redis_get_count(self, key: str) -> int:
        """Get current count from Redis"""
        count = await self.redis_client.get(key)
        return int(count) if count else 0
    
    async def _local_check_and_increment(self, key: str, window: int) -> int:
        """Check and increment counter using local storage"""
        current_time = time.time()
        
        if key not in self.local_buckets:
            # Create new bucket
            self.local_buckets[key] = {
                'count': 1,
                'window_start': current_time,
                'window_size': window
            }
            return 1
        
        bucket = self.local_buckets[key]
        
        # Check if window has expired
        if current_time - bucket['window_start'] >= window:
            bucket['count'] = 1
            bucket['window_start'] = current_time
        else:
            bucket['count'] += 1
        
        return bucket['count']
    
    async def _local_get_count(self, key: str) -> int:
        """Get current count from local storage"""
        if key not in self.local_buckets:
            return 0
        
        bucket = self.local_buckets[key]
        current_time = time.time()
        
        # Check if window has expired
        if current_time - bucket['window_start'] >= bucket['window_size']:
            return 0
        
        return bucket['count']
    
    async def _check_burst_limit(self, key: str, config: RateLimitConfig) -> bool:
        """Check burst limit using token bucket algorithm"""
        if key not in self.local_buckets:
            self.local_buckets[key] = TokenBucket(
                capacity=config.burst_limit,
                refill_rate=config.burst_limit / config.burst_window
            )
        
        bucket = self.local_buckets[key]
        return bucket.consume(1)
    
    async def _record_violation(self, tenant_id: str, client_ip: str, endpoint: str):
        """Record rate limit violation for monitoring"""
        current_time = time.time()
        violation_key = f"{tenant_id}:{client_ip}"
        
        # Track violations
        self.violation_tracking[violation_key].append(current_time)
        
        # Clean old violations (older than 1 hour)
        self.violation_tracking[violation_key] = [
            t for t in self.violation_tracking[violation_key] 
            if current_time - t < 3600
        ]
        
        # Check for suspicious patterns
        violations_in_hour = len(self.violation_tracking[violation_key])
        
        if violations_in_hour > 50:  # More than 50 violations in an hour
            await self._block_ip(client_ip, duration=3600)  # Block for 1 hour
            logger.warning(f"🚨 Blocked IP {client_ip} due to excessive rate limit violations")
        
        elif violations_in_hour > 20:  # More than 20 violations in an hour
            await self._block_ip(client_ip, duration=300)   # Block for 5 minutes
            logger.warning(f"⚠️ Temporarily blocked IP {client_ip} due to rate limit violations")
        
        # Log violation
        logger.info(f"📊 Rate limit violation: {tenant_id} from {client_ip} on {endpoint}")
    
    async def _block_ip(self, client_ip: str, duration: int):
        """Block an IP address for specified duration"""
        unblock_time = time.time() + duration
        self.blocked_ips[client_ip] = unblock_time
        
        if self.redis_client:
            await self.redis_client.setex(f"blocked_ip:{client_ip}", duration, unblock_time)
    
    async def _is_ip_blocked(self, client_ip: str) -> bool:
        """Check if IP address is currently blocked"""
        current_time = time.time()
        
        # Check local blocks
        if client_ip in self.blocked_ips:
            if current_time < self.blocked_ips[client_ip]:
                return True
            else:
                del self.blocked_ips[client_ip]
        
        # Check Redis blocks
        if self.redis_client:
            blocked_until = await self.redis_client.get(f"blocked_ip:{client_ip}")
            if blocked_until and current_time < float(blocked_until):
                return True
        
        return False
    
    async def get_rate_limit_stats(self, tenant_id: str) -> Dict[str, Any]:
        """Get rate limiting statistics for a tenant"""
        current_time = time.time()
        
        # Get violation stats
        violation_keys = [k for k in self.violation_tracking.keys() if k.startswith(f"{tenant_id}:")]
        total_violations = sum(len(violations) for violations in 
                             [self.violation_tracking[k] for k in violation_keys])
        
        # Get current usage stats
        minute_key = f"{tenant_id}:*:minute:{int(current_time // 60)}"
        hour_key = f"{tenant_id}:*:hour:{int(current_time // 3600)}"
        day_key = f"{tenant_id}:*:day:{int(current_time // 86400)}"
        
        stats = {
            "tenant_id": tenant_id,
            "timestamp": datetime.now().isoformat(),
            "violations_last_hour": total_violations,
            "blocked_ips": len([ip for ip, unblock_time in self.blocked_ips.items() 
                              if current_time < unblock_time]),
            "rate_limit_configs": {
                tier.value: asdict(config) 
                for tier, config in self.rate_limit_configs.items()
            },
            "current_usage": {
                "requests_this_minute": await self._get_usage_count(minute_key),
                "requests_this_hour": await self._get_usage_count(hour_key),
                "requests_this_day": await self._get_usage_count(day_key)
            }
        }
        
        return stats
    
    async def _get_usage_count(self, pattern: str) -> int:
        """Get usage count for a pattern"""
        if self.redis_client:
            keys = await self.redis_client.keys(pattern)
            if keys:
                counts = await self.redis_client.mget(keys)
                return sum(int(count) for count in counts if count)
        
        # Local fallback
        matching_keys = [k for k in self.local_buckets.keys() if pattern.replace('*', '') in k]
        return sum(await self._local_get_count(key) for key in matching_keys)
    
    async def reset_rate_limits(self, tenant_id: str, endpoint: Optional[str] = None):
        """Reset rate limits for a tenant (admin function)"""
        pattern = f"{tenant_id}:{endpoint or '*'}:*"
        
        if self.redis_client:
            keys = await self.redis_client.keys(pattern)
            if keys:
                await self.redis_client.delete(*keys)
        
        # Clear local buckets
        keys_to_remove = [k for k in self.local_buckets.keys() 
                         if k.startswith(f"{tenant_id}:")]
        for key in keys_to_remove:
            del self.local_buckets[key]
        
        logger.info(f"🔄 Reset rate limits for tenant {tenant_id}")
    
    async def unblock_ip(self, client_ip: str):
        """Unblock an IP address (admin function)"""
        if client_ip in self.blocked_ips:
            del self.blocked_ips[client_ip]
        
        if self.redis_client:
            await self.redis_client.delete(f"blocked_ip:{client_ip}")
        
        logger.info(f"🔓 Unblocked IP {client_ip}")
    
    async def get_blocked_ips(self) -> List[Dict[str, Any]]:
        """Get list of currently blocked IPs"""
        current_time = time.time()
        blocked_list = []
        
        # Local blocks
        for ip, unblock_time in self.blocked_ips.items():
            if current_time < unblock_time:
                blocked_list.append({
                    "ip": ip,
                    "unblock_time": datetime.fromtimestamp(unblock_time).isoformat(),
                    "remaining_seconds": int(unblock_time - current_time)
                })
        
        # Redis blocks
        if self.redis_client:
            keys = await self.redis_client.keys("blocked_ip:*")
            for key in keys:
                ip = key.replace("blocked_ip:", "")
                unblock_time = await self.redis_client.get(key)
                if unblock_time and current_time < float(unblock_time):
                    blocked_list.append({
                        "ip": ip,
                        "unblock_time": datetime.fromtimestamp(float(unblock_time)).isoformat(),
                        "remaining_seconds": int(float(unblock_time) - current_time)
                    })
        
        return blocked_list
    
    async def shutdown(self):
        """Shutdown the rate limiter service"""
        if self.redis_client:
            await self.redis_client.close()
        logger.info("🛑 API Rate Limiter shutdown complete")

# Global instance
api_rate_limiter = APIRateLimiter() 