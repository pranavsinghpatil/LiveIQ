# Social Authentication

## Purpose
Handles social authentication integration with multiple providers (Google, GitHub, Apple) and manages secure user sessions.

## Features

### 1. OAuth Integration
```python
class OAuthManager:
    def __init__(self):
        self.config = {
            'google': {
                'client_id': os.getenv('GOOGLE_CLIENT_ID'),
                'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
                'redirect_uri': os.getenv('GOOGLE_REDIRECT_URI')
            },
            'github': {
                'client_id': os.getenv('GITHUB_CLIENT_ID'),
                'client_secret': os.getenv('GITHUB_CLIENT_SECRET'),
                'redirect_uri': os.getenv('GITHUB_REDIRECT_URI')
            },
            'apple': {
                'client_id': os.getenv('APPLE_CLIENT_ID'),
                'team_id': os.getenv('APPLE_TEAM_ID'),
                'key_id': os.getenv('APPLE_KEY_ID'),
                'private_key': os.getenv('APPLE_PRIVATE_KEY'),
                'redirect_uri': os.getenv('APPLE_REDIRECT_URI')
            }
        }
        
    async def get_oauth_url(self, provider: str) -> str:
        """
        Generate OAuth URL for specified provider
        """
        if provider == 'google':
            return self._get_google_oauth_url()
        elif provider == 'github':
            return self._get_github_oauth_url()
        elif provider == 'apple':
            return self._get_apple_oauth_url()
            
    async def handle_oauth_callback(
        self,
        provider: str,
        code: str
    ) -> UserAuth:
        """
        Handle OAuth callback and create/update user
        """
        if provider == 'google':
            user_info = await self._handle_google_callback(code)
        elif provider == 'github':
            user_info = await self._handle_github_callback(code)
        elif provider == 'apple':
            user_info = await self._handle_apple_callback(code)
            
        return await self._create_or_update_user(user_info)
```

### 2. Google Authentication
```python
class GoogleAuth:
    def __init__(self, config: Dict[str, str]):
        self.client_id = config['client_id']
        self.client_secret = config['client_secret']
        self.redirect_uri = config['redirect_uri']
        
    async def get_oauth_url(self) -> str:
        """
        Generate Google OAuth URL
        """
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': 'email profile',
            'response_type': 'code',
            'access_type': 'offline'
        }
        return f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
        
    async def handle_callback(self, code: str) -> Dict[str, Any]:
        """
        Handle Google OAuth callback
        """
        # Exchange code for tokens
        token_response = await self._exchange_code(code)
        
        # Get user info using access token
        headers = {
            'Authorization': f"Bearer {token_response['access_token']}"
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(
                'https://www.googleapis.com/oauth2/v2/userinfo',
                headers=headers
            )
            user_info = response.json()
            
        return {
            'provider': 'google',
            'provider_user_id': user_info['id'],
            'email': user_info['email'],
            'name': user_info['name'],
            'avatar_url': user_info.get('picture')
        }
```

### 3. GitHub Authentication
```python
class GitHubAuth:
    def __init__(self, config: Dict[str, str]):
        self.client_id = config['client_id']
        self.client_secret = config['client_secret']
        self.redirect_uri = config['redirect_uri']
        
    async def get_oauth_url(self) -> str:
        """
        Generate GitHub OAuth URL
        """
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': 'read:user user:email',
            'response_type': 'code'
        }
        return f"https://github.com/login/oauth/authorize?{urlencode(params)}"
        
    async def handle_callback(self, code: str) -> Dict[str, Any]:
        """
        Handle GitHub OAuth callback
        """
        # Exchange code for access token
        token_response = await self._exchange_code(code)
        
        # Get user info using access token
        headers = {
            'Authorization': f"token {token_response['access_token']}",
            'Accept': 'application/vnd.github.v3+json'
        }
        async with httpx.AsyncClient() as client:
            user_response = await client.get(
                'https://api.github.com/user',
                headers=headers
            )
            user_info = user_response.json()
            
            # Get primary email
            email_response = await client.get(
                'https://api.github.com/user/emails',
                headers=headers
            )
            primary_email = next(
                email for email in email_response.json()
                if email['primary']
            )
            
        return {
            'provider': 'github',
            'provider_user_id': str(user_info['id']),
            'email': primary_email['email'],
            'name': user_info['name'] or user_info['login'],
            'avatar_url': user_info['avatar_url']
        }
```

### 4. Apple Authentication
```python
class AppleAuth:
    def __init__(self, config: Dict[str, str]):
        self.client_id = config['client_id']
        self.team_id = config['team_id']
        self.key_id = config['key_id']
        self.private_key = config['private_key']
        self.redirect_uri = config['redirect_uri']
        
    async def get_oauth_url(self) -> str:
        """
        Generate Apple OAuth URL
        """
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': 'email name',
            'response_type': 'code',
            'response_mode': 'form_post'
        }
        return f"https://appleid.apple.com/auth/authorize?{urlencode(params)}"
        
    async def handle_callback(
        self,
        code: str,
        user_data: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Handle Apple OAuth callback
        """
        # Generate client secret
        client_secret = self._create_client_secret()
        
        # Exchange code for tokens
        token_response = await self._exchange_code(code, client_secret)
        
        # Decode identity token
        identity_token = jwt.decode(
            token_response['id_token'],
            options={'verify_signature': False}
        )
        
        # Parse user data if available (only on first login)
        user_info = {}
        if user_data:
            user_info = json.loads(user_data)
            
        return {
            'provider': 'apple',
            'provider_user_id': identity_token['sub'],
            'email': identity_token['email'],
            'name': user_info.get('name', {}).get('firstName', ''),
            'avatar_url': None
        }
```

### 5. Session Management
```python
class SessionManager:
    def __init__(self, redis: Redis):
        self.redis = redis
        self.jwt_secret = os.getenv('JWT_SECRET')
        
    async def create_session(self, user_id: int) -> str:
        """
        Create new user session
        """
        session_id = str(uuid.uuid4())
        
        # Store session in Redis
        await self.redis.set(
            f"session:{session_id}",
            json.dumps({'user_id': user_id}),
            ex=86400  # 24 hours
        )
        
        # Generate JWT
        token = jwt.encode(
            {
                'sub': user_id,
                'sid': session_id,
                'exp': datetime.utcnow() + timedelta(days=1)
            },
            self.jwt_secret,
            algorithm='HS256'
        )
        
        return token
        
    async def validate_session(self, token: str) -> Optional[int]:
        """
        Validate session token
        """
        try:
            # Decode JWT
            payload = jwt.decode(
                token,
                self.jwt_secret,
                algorithms=['HS256']
            )
            
            # Check if session exists in Redis
            session = await self.redis.get(f"session:{payload['sid']}")
            if not session:
                return None
                
            return payload['sub']
            
        except jwt.InvalidTokenError:
            return None
```

## API Integration

### 1. OAuth Routes
```python
@router.get("/auth/{provider}/login")
async def oauth_login(
    provider: str,
    oauth: OAuthManager = Depends(get_oauth_manager)
) -> Dict[str, str]:
    """
    Generate OAuth URL for provider
    """
    url = await oauth.get_oauth_url(provider)
    return {"url": url}

@router.post("/auth/{provider}/callback")
async def oauth_callback(
    provider: str,
    code: str,
    oauth: OAuthManager = Depends(get_oauth_manager),
    session: SessionManager = Depends(get_session_manager)
) -> Dict[str, str]:
    """
    Handle OAuth callback
    """
    user_auth = await oauth.handle_oauth_callback(provider, code)
    token = await session.create_session(user_auth.user_id)
    return {"token": token}
```

## Security Features

### 1. CSRF Protection
```python
class CSRFMiddleware:
    async def __call__(
        self,
        request: Request,
        call_next: RequestResponseEndpoint
    ) -> Response:
        if request.method in ('POST', 'PUT', 'DELETE', 'PATCH'):
            csrf_token = request.headers.get('X-CSRF-Token')
            if not csrf_token:
                raise HTTPException(403, 'CSRF token missing')
                
            if not await self._validate_csrf_token(csrf_token):
                raise HTTPException(403, 'Invalid CSRF token')
                
        response = await call_next(request)
        return response
```

### 2. Rate Limiting
```python
class RateLimiter:
    def __init__(self, redis: Redis):
        self.redis = redis
        
    async def check_rate_limit(
        self,
        key: str,
        limit: int,
        window: int
    ) -> bool:
        """
        Check if rate limit is exceeded
        """
        current = await self.redis.incr(key)
        if current == 1:
            await self.redis.expire(key, window)
            
        return current <= limit
```

## Recent Updates
- Added Apple Sign-In
- Enhanced session security
- Improved error handling
- Added rate limiting
- Updated OAuth flows

## Best Practices
- Secure token handling
- Input validation
- Error logging
- Session management
- Rate limiting
