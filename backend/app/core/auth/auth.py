import os
import json
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import uuid

import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from redis import Redis
from pydantic import BaseModel

class User(BaseModel):
    id: str
    email: str
    name: str
    is_guest: bool = False
    guest_imports_remaining: Optional[int] = None
    guest_messages_remaining: Optional[int] = None

class AuthManager:
    def __init__(self):
        self.jwt_secret = os.getenv('JWT_SECRET', 'your-secret-key')
        self.redis = Redis(host='localhost', port=6379, db=0)
        self.security = HTTPBearer()
        
    async def create_token(self, user: User) -> str:
        """Create JWT token for user"""
        payload = {
            'sub': user.id,
            'email': user.email,
            'name': user.name,
            'is_guest': user.is_guest,
            'exp': datetime.utcnow() + timedelta(days=1)
        }
        
        if user.is_guest:
            payload.update({
                'guest_imports_remaining': user.guest_imports_remaining,
                'guest_messages_remaining': user.guest_messages_remaining
            })
            
        return jwt.encode(payload, self.jwt_secret, algorithm='HS256')
        
    async def verify_token(
        self,
        credentials: HTTPAuthorizationCredentials = Security(HTTPBearer())
    ) -> User:
        """Verify JWT token and return user"""
        try:
            token = credentials.credentials
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            
            # Check if token is blacklisted
            if await self.redis.get(f"blacklist:{token}"):
                raise HTTPException(status_code=401, detail="Token has been revoked")
                
            return User(
                id=payload['sub'],
                email=payload['email'],
                name=payload['name'],
                is_guest=payload.get('is_guest', False),
                guest_imports_remaining=payload.get('guest_imports_remaining'),
                guest_messages_remaining=payload.get('guest_messages_remaining')
            )
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
            
    async def create_guest_user(self) -> User:
        """Create a new guest user"""
        return User(
            id=str(uuid.uuid4()),
            email=f"guest_{uuid.uuid4()}@voxstitch.com",
            name="Guest User",
            is_guest=True,
            guest_imports_remaining=2,
            guest_messages_remaining=5
        )
        
    async def update_guest_limits(self, user: User, action: str) -> User:
        """Update guest user limits"""
        if not user.is_guest:
            return user
            
        if action == 'import':
            if user.guest_imports_remaining <= 0:
                raise HTTPException(
                    status_code=403,
                    detail="Guest import limit reached"
                )
            user.guest_imports_remaining -= 1
            
        elif action == 'message':
            if user.guest_messages_remaining <= 0:
                raise HTTPException(
                    status_code=403,
                    detail="Guest message limit reached"
                )
            user.guest_messages_remaining -= 1
            
        return user
        
    async def revoke_token(self, token: str):
        """Revoke JWT token"""
        try:
            # Decode token to get expiration
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            exp = datetime.fromtimestamp(payload['exp'])
            ttl = (exp - datetime.utcnow()).total_seconds()
            
            # Add token to blacklist
            await self.redis.set(
                f"blacklist:{token}",
                "1",
                ex=int(ttl)
            )
            
        except jwt.InvalidTokenError:
            pass  # Token is already invalid
            
    async def upgrade_guest(self, user: User, email: str, name: str) -> User:
        """Upgrade guest user to regular user"""
        if not user.is_guest:
            raise HTTPException(
                status_code=400,
                detail="User is not a guest"
            )
            
        return User(
            id=user.id,
            email=email,
            name=name,
            is_guest=False
        )
        
class RateLimiter:
    def __init__(self, redis: Redis):
        self.redis = redis
        
    async def check_rate_limit(
        self,
        key: str,
        limit: int,
        window: int
    ) -> bool:
        """Check if rate limit is exceeded"""
        current = await self.redis.incr(key)
        if current == 1:
            await self.redis.expire(key, window)
            
        return current <= limit
        
    async def get_remaining(self, key: str) -> Optional[int]:
        """Get remaining requests in window"""
        count = await self.redis.get(key)
        if count is None:
            return None
            
        ttl = await self.redis.ttl(key)
        if ttl <= 0:
            return None
            
        return max(0, int(count))
        
class SecurityConfig:
    CORS_ORIGINS = [
        "http://localhost:3000",
        "https://voxstitch.com"
    ]
    
    RATE_LIMITS = {
        'login': {'limit': 5, 'window': 300},  # 5 attempts per 5 minutes
        'register': {'limit': 3, 'window': 3600},  # 3 attempts per hour
        'api': {'limit': 100, 'window': 60}  # 100 requests per minute
    }
