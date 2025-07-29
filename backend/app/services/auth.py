from typing import Optional, Dict, Any
from datetime import datetime, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..utils.security import decode_token

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Get the current authenticated user from JWT token.
    
    Args:
        token: JWT access token
        db: Database session
        
    Returns:
        User: Current authenticated user
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    
    # Check if it's an access token
    if payload.get("type") != "access":
        raise credentials_exception
    
    # Get user ID from token
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    # Get user from database
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get the current active user.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User: Current active user
        
    Raises:
        HTTPException: If user is not active
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """
    Authenticate a user by username and password.
    
    Args:
        db: Database session
        username: Username or email
        password: Plain text password
        
    Returns:
        Optional[User]: User if authentication successful, None otherwise
    """
    from ..utils.security import verify_password
    
    # Try to find user by username or email
    user = db.query(User).filter(
        (User.username == username) | (User.email == username)
    ).first()
    
    if not user:
        return None
    
    if not verify_password(password, user.password_hash):
        return None
    
    return user


class RateLimiter:
    """
    Simple in-memory rate limiter for authentication endpoints.
    """
    def __init__(self):
        self.attempts: Dict[str, list] = {}
        self.max_attempts = 5
        self.window_minutes = 15
    
    def check_rate_limit(self, identifier: str) -> bool:
        """
        Check if an identifier (IP or username) has exceeded rate limit.
        
        Args:
            identifier: IP address or username
            
        Returns:
            bool: True if within rate limit, False if exceeded
        """
        now = datetime.now(timezone.utc)
        window_start = now.timestamp() - (self.window_minutes * 60)
        
        # Get attempts for this identifier
        if identifier not in self.attempts:
            self.attempts[identifier] = []
        
        # Remove old attempts outside the window
        self.attempts[identifier] = [
            attempt for attempt in self.attempts[identifier]
            if attempt > window_start
        ]
        
        # Check if limit exceeded
        if len(self.attempts[identifier]) >= self.max_attempts:
            return False
        
        # Add current attempt
        self.attempts[identifier].append(now.timestamp())
        return True
    
    def reset_attempts(self, identifier: str):
        """
        Reset attempts for an identifier (e.g., after successful login).
        
        Args:
            identifier: IP address or username
        """
        if identifier in self.attempts:
            del self.attempts[identifier]


# Global rate limiter instance
rate_limiter = RateLimiter()