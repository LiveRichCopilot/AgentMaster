"""
API Utilities for JAi Cortex Agents
Handles authentication, rate limiting, retries, caching
"""

import time
import functools
import hashlib
import json
from typing import Dict, Any, Optional, Callable
from collections import defaultdict
from datetime import datetime, timedelta
import os

# ============================================================================
# RATE LIMITING
# ============================================================================

class RateLimiter:
    """Token bucket rate limiter"""
    
    def __init__(self):
        self.buckets = defaultdict(lambda: {"tokens": 100, "last_refill": time.time()})
        self.limits = {
            "gemini": {"rate": 60, "per": 60},  # 60 requests per minute
            "web_search": {"rate": 100, "per": 60},
            "firestore": {"rate": 500, "per": 60},
            "storage": {"rate": 1000, "per": 60},
            "default": {"rate": 100, "per": 60}
        }
    
    def acquire(self, api_name: str = "default") -> bool:
        """Acquire a token for API call"""
        limit = self.limits.get(api_name, self.limits["default"])
        bucket = self.buckets[api_name]
        
        # Refill tokens
        now = time.time()
        time_passed = now - bucket["last_refill"]
        refill_amount = (time_passed / limit["per"]) * limit["rate"]
        
        bucket["tokens"] = min(limit["rate"], bucket["tokens"] + refill_amount)
        bucket["last_refill"] = now
        
        # Check if we have tokens
        if bucket["tokens"] >= 1:
            bucket["tokens"] -= 1
            return True
        return False
    
    def wait_if_needed(self, api_name: str = "default", max_wait: float = 5.0):
        """Wait until a token is available"""
        start = time.time()
        while not self.acquire(api_name):
            if time.time() - start > max_wait:
                raise Exception(f"Rate limit exceeded for {api_name}, waited {max_wait}s")
            time.sleep(0.1)

# Global rate limiter instance
rate_limiter = RateLimiter()

# ============================================================================
# RETRY WITH EXPONENTIAL BACKOFF
# ============================================================================

def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff_factor: float = 2.0
):
    """Decorator for retrying with exponential backoff"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    
                    if attempt < max_retries - 1:
                        delay = min(base_delay * (backoff_factor ** attempt), max_delay)
                        print(f"⚠️  {func.__name__} failed (attempt {attempt + 1}/{max_retries}), retrying in {delay:.1f}s: {str(e)}")
                        time.sleep(delay)
                    else:
                        print(f"❌ {func.__name__} failed after {max_retries} attempts: {str(e)}")
            
            raise last_exception
        return wrapper
    return decorator

# ============================================================================
# CACHING
# ============================================================================

class SimpleCache:
    """Simple in-memory cache with TTL"""
    
    def __init__(self, default_ttl: int = 300):
        self.cache = {}
        self.default_ttl = default_ttl
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached value"""
        if key in self.cache:
            value, expiry = self.cache[key]
            if datetime.now() < expiry:
                return value
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set cached value"""
        expiry = datetime.now() + timedelta(seconds=ttl or self.default_ttl)
        self.cache[key] = (value, expiry)
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()

# Global cache instance
cache = SimpleCache()

def cache_result(ttl: int = 300, key_func: Optional[Callable] = None):
    """Decorator for caching function results"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                key_data = f"{func.__name__}:{str(args)}:{str(kwargs)}"
                cache_key = hashlib.md5(key_data.encode()).hexdigest()
            
            # Check cache
            cached = cache.get(cache_key)
            if cached is not None:
                print(f"📦 Cache hit for {func.__name__}")
                return cached
            
            # Execute and cache
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            return result
        return wrapper
    return decorator

# ============================================================================
# AUTHENTICATION & CREDENTIALS
# ============================================================================

class CredentialManager:
    """Manage API credentials securely"""
    
    def __init__(self):
        self.credentials = {}
        self._load_from_env()
    
    def _load_from_env(self):
        """Load credentials from environment variables"""
        # Google Cloud
        if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            self.credentials["google_cloud"] = {
                "type": "service_account",
                "path": os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            }
        
        # Vertex AI
        if os.getenv("GOOGLE_CLOUD_PROJECT"):
            self.credentials["vertex_ai"] = {
                "project": os.getenv("GOOGLE_CLOUD_PROJECT"),
                "location": os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
            }
        
        # API Keys
        for key in ["GEMINI_API_KEY", "SERPER_API_KEY", "OPENAI_API_KEY"]:
            if os.getenv(key):
                self.credentials[key.lower()] = os.getenv(key)
    
    def get(self, service: str) -> Optional[Any]:
        """Get credentials for a service"""
        return self.credentials.get(service)
    
    def set(self, service: str, credential: Any):
        """Set credentials for a service"""
        self.credentials[service] = credential

# Global credential manager
cred_manager = CredentialManager()

# ============================================================================
# API CALL WRAPPER
# ============================================================================

def api_call(
    api_name: str = "default",
    retry: bool = True,
    cache_ttl: Optional[int] = None,
    rate_limit: bool = True
):
    """
    Comprehensive API call decorator
    Combines rate limiting, retries, caching, and error handling
    """
    def decorator(func: Callable) -> Callable:
        # Apply decorators in order
        wrapped = func
        
        # 1. Caching (innermost)
        if cache_ttl is not None:
            wrapped = cache_result(ttl=cache_ttl)(wrapped)
        
        # 2. Retry logic
        if retry:
            wrapped = retry_with_backoff()(wrapped)
        
        # 3. Rate limiting (outermost)
        @functools.wraps(wrapped)
        def wrapper(*args, **kwargs):
            if rate_limit:
                rate_limiter.wait_if_needed(api_name)
            
            try:
                return wrapped(*args, **kwargs)
            except Exception as e:
                # Structured error logging
                error_info = {
                    "function": func.__name__,
                    "api": api_name,
                    "error": str(e),
                    "type": type(e).__name__,
                    "timestamp": datetime.now().isoformat()
                }
                print(f"❌ API Error: {json.dumps(error_info, indent=2)}")
                raise
        
        return wrapper
    return decorator

# ============================================================================
# VALIDATION HELPERS
# ============================================================================

def validate_response(response: Dict[str, Any], required_fields: list) -> bool:
    """Validate API response has required fields"""
    for field in required_fields:
        if field not in response:
            raise ValueError(f"Missing required field: {field}")
    return True

def sanitize_data(data: Any, max_size: int = 1_000_000) -> Any:
    """Sanitize data before processing"""
    if isinstance(data, str) and len(data) > max_size:
        raise ValueError(f"Data too large: {len(data)} bytes (max: {max_size})")
    return data

