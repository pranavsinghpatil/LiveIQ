# Understanding Authentication in ChatSynth

## What is Authentication?

Authentication is how we make sure users are who they say they are. Think of it like a key card system:
1. You get a special card (token) when you log in
2. You show this card every time you want to do something
3. The system checks if your card is valid

## How We Implement It

### 1. User Registration
First, let's see how we create new users:

```python
# In models.py - Our User model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)  # Each email can only be used once
    hashed_password = Column(String)     # We never store actual passwords
    
    # Let's break this down:
    # 1. email must be unique - no two users can have same email
    # 2. hashed_password is the encrypted version of the password
    # 3. We never store the actual password - only its encrypted form

# In schemas.py - How we handle user data
class UserCreate(BaseModel):
    email: str
    password: str  # The actual password (we'll hash it)
    
    # Validate email format
    @validator("email")
    def validate_email(cls, v):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", v):
            raise ValueError("Invalid email format")
        return v
    
    # Validate password strength
    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain a number")
        return v

# In auth.py - Functions for handling passwords
def hash_password(password: str) -> str:
    """Convert password to secure hash
    
    Args:
        password: The plain text password
    
    Returns:
        Hashed version of password that's safe to store
    
    Example:
        plain_password = "mypassword123"
        hashed = hash_password(plain_password)
        # hashed will look like: $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKxcQw8Ac8AC8qC
    """
    # We use bcrypt to hash passwords
    salt = bcrypt.gensalt()  # Create random salt
    hashed = bcrypt.hashpw(password.encode(), salt)  # Hash with salt
    return hashed.decode()  # Convert back to string

# In routes.py - The registration endpoint
@app.post("/register")
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # 1. Check if email already exists
    existing_user = db.query(User)\
        .filter(User.email == user_data.email)\
        .first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # 2. Create new user
    new_user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )
    
    # 3. Save to database
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "User created successfully"}
    except Exception as e:
        db.rollback()  # If anything goes wrong, undo changes
        raise HTTPException(
            status_code=500,
            detail="Failed to create user"
        )
```

### 2. User Login
When users want to access their account:

```python
# In schemas.py - Login data structure
class UserLogin(BaseModel):
    email: str
    password: str

# In auth.py - Password checking
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if a password matches its hash
    
    Args:
        plain_password: The password to check
        hashed_password: The stored hash to check against
    
    Returns:
        True if password matches, False if not
    
    Example:
        stored_hash = user.hashed_password
        is_valid = verify_password("mypassword123", stored_hash)
        # is_valid will be True if password is correct
    """
    return bcrypt.checkpw(
        plain_password.encode(),
        hashed_password.encode()
    )

# In auth.py - Creating access tokens
def create_access_token(data: dict) -> str:
    """Create a JWT token for user authentication
    
    Args:
        data: Dictionary of data to include in token
    
    Returns:
        JWT token string
    
    Example:
        token = create_access_token({"sub": user.email})
        # token will look like: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
    """
    to_encode = data.copy()
    # Add expiration time
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # Create JWT token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# In routes.py - Login endpoint
@app.post("/login")
async def login(
    form_data: UserLogin,
    db: Session = Depends(get_db)
):
    # 1. Find user by email
    user = db.query(User)\
        .filter(User.email == form_data.email)\
        .first()
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )
    
    # 2. Check password
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )
    
    # 3. Create access token
    access_token = create_access_token(
        data={"sub": user.email}
    )
    
    # 4. Return token to user
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
```

### 3. Protecting Routes
How we make sure only logged-in users can access certain features:

```python
# In auth.py - Getting the current user
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Get the current logged-in user from their token
    
    Args:
        token: JWT token from request
        db: Database session
    
    Returns:
        User object if token is valid
    
    Raises:
        HTTPException if token is invalid
    
    Example:
        @app.get("/me")
        async def read_me(user: User = Depends(get_current_user)):
            return user
    """
    # 1. Define error response
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 2. Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        
        # 3. Get user from database
        user = db.query(User)\
            .filter(User.email == email)\
            .first()
        if user is None:
            raise credentials_exception
            
        return user
        
    except JWTError:
        raise credentials_exception

# In routes.py - Protected route example
@app.get("/chats")
async def get_my_chats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all chats for the logged-in user
    
    This route is protected - you must be logged in to use it
    
    Args:
        current_user: Automatically gets the logged-in user
        db: Database session
    
    Returns:
        List of user's chats
    """
    return db.query(ChatLog)\
        .filter(ChatLog.user_id == current_user.id)\
        .all()
```

### 4. Logout and Token Management
We use Redis to handle token invalidation:

```python
# In auth.py - Redis for token blacklist
class TokenBlacklist:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client
        self.prefix = "token_blacklist:"
    
    async def blacklist_token(self, token: str):
        """Add a token to the blacklist
        
        Args:
            token: JWT token to blacklist
        
        Example:
            await blacklist.blacklist_token(token)
            # Token will no longer work for requests
        """
        # Get token expiration
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            exp = payload.get("exp")
            if exp:
                # Store in Redis until token expires
                ttl = exp - datetime.utcnow().timestamp()
                if ttl > 0:
                    await self.redis.setex(
                        f"{self.prefix}{token}",
                        int(ttl),
                        "1"
                    )
        except JWTError:
            pass  # Invalid tokens don't need blacklisting

    async def is_blacklisted(self, token: str) -> bool:
        """Check if a token is blacklisted
        
        Args:
            token: JWT token to check
        
        Returns:
            True if token is blacklisted, False if not
        """
        return await self.redis.exists(f"{self.prefix}{token}")

# In routes.py - Logout endpoint
@app.post("/logout")
async def logout(
    token: str = Depends(oauth2_scheme),
    blacklist: TokenBlacklist = Depends(get_token_blacklist)
):
    """Log out a user by blacklisting their token
    
    Args:
        token: Current user's token (automatic)
        blacklist: Token blacklist service
    """
    await blacklist.blacklist_token(token)
    return {"message": "Successfully logged out"}
```

## Security Best Practices

1. **Password Storage**:
   - Never store plain passwords
   - Use strong hashing (bcrypt)
   - Add random salt to each hash

2. **Token Security**:
   - Short expiration times
   - Secure token storage
   - Token blacklisting for logout

3. **Error Messages**:
   - Don't reveal if email exists
   - Use generic error messages
   - Log detailed errors internally

## Practice Exercise

Try to create a password reset system:
1. Endpoint to request reset
2. Token generation for reset
3. Endpoint to perform reset

Here's a starter template:
```python
@app.post("/reset-password/request")
async def request_password_reset(
    email: str,
    db: Session = Depends(get_db)
):
    # Your code here
    pass

@app.post("/reset-password/confirm")
async def confirm_password_reset(
    token: str,
    new_password: str,
    db: Session = Depends(get_db)
):
    # Your code here
    pass
```

## Next Steps
1. Try the practice exercise
2. Learn about rate limiting
3. Study session management
4. Explore two-factor authentication
