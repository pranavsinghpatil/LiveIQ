import os
from typing import Dict, Any, Optional
import json
import uuid
from datetime import datetime

import httpx
from fastapi import HTTPException
from pydantic import BaseModel

class OAuthConfig:
    GOOGLE = {
        'client_id': os.getenv('GOOGLE_CLIENT_ID'),
        'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
        'redirect_uri': os.getenv('GOOGLE_REDIRECT_URI'),
        'auth_url': 'https://accounts.google.com/o/oauth2/v2/auth',
        'token_url': 'https://oauth2.googleapis.com/token',
        'userinfo_url': 'https://www.googleapis.com/oauth2/v3/userinfo',
        'scopes': ['openid', 'email', 'profile']
    }
    
    GITHUB = {
        'client_id': os.getenv('GITHUB_CLIENT_ID'),
        'client_secret': os.getenv('GITHUB_CLIENT_SECRET'),
        'redirect_uri': os.getenv('GITHUB_REDIRECT_URI'),
        'auth_url': 'https://github.com/login/oauth/authorize',
        'token_url': 'https://github.com/login/oauth/access_token',
        'userinfo_url': 'https://api.github.com/user',
        'scopes': ['read:user', 'user:email']
    }
    
    APPLE = {
        'client_id': os.getenv('APPLE_CLIENT_ID'),
        'team_id': os.getenv('APPLE_TEAM_ID'),
        'key_id': os.getenv('APPLE_KEY_ID'),
        'private_key': os.getenv('APPLE_PRIVATE_KEY'),
        'redirect_uri': os.getenv('APPLE_REDIRECT_URI'),
        'auth_url': 'https://appleid.apple.com/auth/authorize',
        'token_url': 'https://appleid.apple.com/auth/token'
    }

class SocialUser(BaseModel):
    id: str
    email: str
    name: str
    provider: str
    avatar_url: Optional[str] = None
    provider_data: Dict[str, Any]

class OAuthManager:
    def __init__(self):
        self.config = OAuthConfig()
        self.http_client = httpx.AsyncClient()
        
    async def get_oauth_url(self, provider: str) -> str:
        """Get OAuth URL for provider"""
        if provider == 'google':
            return self._get_google_oauth_url()
        elif provider == 'github':
            return self._get_github_oauth_url()
        elif provider == 'apple':
            return self._get_apple_oauth_url()
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported provider: {provider}"
            )
            
    def _get_google_oauth_url(self) -> str:
        """Get Google OAuth URL"""
        params = {
            'client_id': self.config.GOOGLE['client_id'],
            'redirect_uri': self.config.GOOGLE['redirect_uri'],
            'response_type': 'code',
            'scope': ' '.join(self.config.GOOGLE['scopes']),
            'access_type': 'offline',
            'include_granted_scopes': 'true',
            'state': str(uuid.uuid4())
        }
        
        query = '&'.join(f"{k}={v}" for k, v in params.items())
        return f"{self.config.GOOGLE['auth_url']}?{query}"
        
    def _get_github_oauth_url(self) -> str:
        """Get GitHub OAuth URL"""
        params = {
            'client_id': self.config.GITHUB['client_id'],
            'redirect_uri': self.config.GITHUB['redirect_uri'],
            'scope': ' '.join(self.config.GITHUB['scopes']),
            'state': str(uuid.uuid4())
        }
        
        query = '&'.join(f"{k}={v}" for k, v in params.items())
        return f"{self.config.GITHUB['auth_url']}?{query}"
        
    def _get_apple_oauth_url(self) -> str:
        """Get Apple OAuth URL"""
        params = {
            'client_id': self.config.APPLE['client_id'],
            'redirect_uri': self.config.APPLE['redirect_uri'],
            'response_type': 'code',
            'scope': 'name email',
            'response_mode': 'form_post',
            'state': str(uuid.uuid4())
        }
        
        query = '&'.join(f"{k}={v}" for k, v in params.items())
        return f"{self.config.APPLE['auth_url']}?{query}"
        
    async def handle_oauth_callback(
        self,
        provider: str,
        code: str,
        state: Optional[str] = None
    ) -> SocialUser:
        """Handle OAuth callback"""
        if provider == 'google':
            return await self._handle_google_callback(code)
        elif provider == 'github':
            return await self._handle_github_callback(code)
        elif provider == 'apple':
            return await self._handle_apple_callback(code)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported provider: {provider}"
            )
            
    async def _handle_google_callback(self, code: str) -> SocialUser:
        """Handle Google OAuth callback"""
        # Exchange code for token
        token_data = await self._get_google_token(code)
        
        # Get user info
        async with self.http_client.get(
            self.config.GOOGLE['userinfo_url'],
            headers={'Authorization': f"Bearer {token_data['access_token']}"}
        ) as response:
            if response.status_code != 200:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to get Google user info"
                )
                
            user_info = response.json()
            
        return SocialUser(
            id=user_info['sub'],
            email=user_info['email'],
            name=user_info.get('name', user_info['email']),
            provider='google',
            avatar_url=user_info.get('picture'),
            provider_data=user_info
        )
        
    async def _handle_github_callback(self, code: str) -> SocialUser:
        """Handle GitHub OAuth callback"""
        # Exchange code for token
        token_data = await self._get_github_token(code)
        
        # Get user info
        async with self.http_client.get(
            self.config.GITHUB['userinfo_url'],
            headers={
                'Authorization': f"token {token_data['access_token']}",
                'Accept': 'application/json'
            }
        ) as response:
            if response.status_code != 200:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to get GitHub user info"
                )
                
            user_info = response.json()
            
        # Get user email
        async with self.http_client.get(
            'https://api.github.com/user/emails',
            headers={
                'Authorization': f"token {token_data['access_token']}",
                'Accept': 'application/json'
            }
        ) as response:
            if response.status_code != 200:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to get GitHub user email"
                )
                
            emails = response.json()
            primary_email = next(
                (e['email'] for e in emails if e['primary']),
                emails[0]['email']
            )
            
        return SocialUser(
            id=str(user_info['id']),
            email=primary_email,
            name=user_info.get('name', user_info['login']),
            provider='github',
            avatar_url=user_info.get('avatar_url'),
            provider_data=user_info
        )
        
    async def _handle_apple_callback(self, code: str) -> SocialUser:
        """Handle Apple OAuth callback"""
        # Exchange code for token
        token_data = await self._get_apple_token(code)
        
        # Decode identity token
        try:
            identity_token = jwt.decode(
                token_data['id_token'],
                options={"verify_signature": False}
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=400,
                detail="Invalid Apple identity token"
            )
            
        return SocialUser(
            id=identity_token['sub'],
            email=identity_token.get('email'),
            name=token_data.get('user', {}).get('name', {}).get('firstName', 'Apple User'),
            provider='apple',
            provider_data=identity_token
        )
        
    async def _get_google_token(self, code: str) -> Dict[str, Any]:
        """Exchange Google code for token"""
        data = {
            'client_id': self.config.GOOGLE['client_id'],
            'client_secret': self.config.GOOGLE['client_secret'],
            'code': code,
            'redirect_uri': self.config.GOOGLE['redirect_uri'],
            'grant_type': 'authorization_code'
        }
        
        async with self.http_client.post(
            self.config.GOOGLE['token_url'],
            data=data
        ) as response:
            if response.status_code != 200:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to get Google token"
                )
                
            return response.json()
            
    async def _get_github_token(self, code: str) -> Dict[str, Any]:
        """Exchange GitHub code for token"""
        data = {
            'client_id': self.config.GITHUB['client_id'],
            'client_secret': self.config.GITHUB['client_secret'],
            'code': code,
            'redirect_uri': self.config.GITHUB['redirect_uri']
        }
        
        async with self.http_client.post(
            self.config.GITHUB['token_url'],
            data=data,
            headers={'Accept': 'application/json'}
        ) as response:
            if response.status_code != 200:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to get GitHub token"
                )
                
            return response.json()
            
    async def _get_apple_token(self, code: str) -> Dict[str, Any]:
        """Exchange Apple code for token"""
        # Generate client secret
        client_secret = self._generate_apple_client_secret()
        
        data = {
            'client_id': self.config.APPLE['client_id'],
            'client_secret': client_secret,
            'code': code,
            'redirect_uri': self.config.APPLE['redirect_uri'],
            'grant_type': 'authorization_code'
        }
        
        async with self.http_client.post(
            self.config.APPLE['token_url'],
            data=data
        ) as response:
            if response.status_code != 200:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to get Apple token"
                )
                
            return response.json()
            
    def _generate_apple_client_secret(self) -> str:
        """Generate Apple client secret JWT"""
        now = datetime.utcnow()
        
        payload = {
            'iss': self.config.APPLE['team_id'],
            'iat': now,
            'exp': now + timedelta(minutes=5),
            'aud': 'https://appleid.apple.com',
            'sub': self.config.APPLE['client_id']
        }
        
        headers = {
            'kid': self.config.APPLE['key_id'],
            'alg': 'ES256'
        }
        
        return jwt.encode(
            payload,
            self.config.APPLE['private_key'],
            algorithm='ES256',
            headers=headers
        )
