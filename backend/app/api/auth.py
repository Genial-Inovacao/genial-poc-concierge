from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Dict, Any
import logging

from ..database import get_db
from ..models import User, Profile
from ..schemas import (
    UserCreate,
    UserLogin,
    TokenResponse,
    TokenRefresh,
    UserResponse,
    PasswordChange,
    PasswordReset,
    PasswordResetConfirm
)
from ..services.auth import authenticate_user, get_current_user, rate_limiter
from ..utils.security import get_password_hash, create_tokens, decode_token

router = APIRouter(prefix="/auth", tags=["Authentication"])
logger = logging.getLogger(__name__)


@router.post("/register", response_model=TokenResponse)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    request: Request = None
):
    """
    Register a new user.
    
    Args:
        user_data: User registration data
        db: Database session
        request: HTTP request for rate limiting
        
    Returns:
        Token response with access and refresh tokens
        
    Raises:
        HTTPException: If username/email already exists or rate limit exceeded
    """
    # Rate limiting by IP
    client_ip = request.client.host if request else "127.0.0.1"
    if not rate_limiter.check_rate_limit(f"register:{client_ip}"):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many registration attempts. Please try again later."
        )
    
    # Check if username or email already exists
    existing_user = db.query(User).filter(
        (User.username == user_data.username) |
        (User.email == user_data.email)
    ).first()
    
    if existing_user:
        if existing_user.username == user_data.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Create new user
    try:
        # Hash password
        hashed_password = get_password_hash(user_data.password)
        
        # Create user
        new_user = User(
            username=user_data.username.lower(),
            email=user_data.email.lower(),
            password_hash=hashed_password
        )
        db.add(new_user)
        db.flush()  # Get the user ID
        
        # Create empty profile
        new_profile = Profile(user_id=new_user.id)
        db.add(new_profile)
        
        db.commit()
        db.refresh(new_user)
        
        # Generate tokens
        tokens = create_tokens(str(new_user.id))
        
        # Reset rate limit on successful registration
        rate_limiter.reset_attempts(f"register:{client_ip}")
        
        return tokens
        
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User registration failed"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during registration"
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: UserLogin,
    db: Session = Depends(get_db),
    request: Request = None
):
    """
    Login user with username/email and password.
    
    Args:
        credentials: Login credentials with username and password
        db: Database session
        request: HTTP request for rate limiting
        
    Returns:
        Token response with access and refresh tokens
        
    Raises:
        HTTPException: If credentials invalid or rate limit exceeded
    """
    # Rate limiting by username and IP
    client_ip = request.client.host if request else "127.0.0.1"
    rate_limit_key = f"login:{credentials.username}:{client_ip}"
    
    if not rate_limiter.check_rate_limit(rate_limit_key):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Please try again later."
        )
    
    # Authenticate user
    user = authenticate_user(db, credentials.username, credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated"
        )
    
    # Generate tokens
    tokens = create_tokens(str(user.id))
    
    # Reset rate limit on successful login
    rate_limiter.reset_attempts(rate_limit_key)
    
    return tokens


@router.post("/token", response_model=TokenResponse)
async def login_for_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    OAuth2 compatible login endpoint for Swagger UI.
    
    This endpoint accepts form data instead of JSON.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated"
        )
    
    return create_tokens(str(user.id))


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    token_data: TokenRefresh,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token.
    
    Args:
        token_data: Refresh token
        db: Database session
        
    Returns:
        New token response with access and refresh tokens
        
    Raises:
        HTTPException: If refresh token invalid or expired
    """
    # Decode refresh token
    payload = decode_token(token_data.refresh_token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Check if it's a refresh token
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )
    
    # Get user ID
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    # Verify user exists and is active
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Generate new tokens
    tokens = create_tokens(str(user.id))
    
    return tokens


@router.post("/logout", response_model=Dict[str, str])
async def logout(current_user: User = Depends(get_current_user)):
    """
    Logout current user.
    
    In a real implementation, you would invalidate the tokens here.
    For now, we just return a success message.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Success message
    """
    # In a production system, you would:
    # 1. Add the token to a blacklist
    # 2. Or store active tokens in Redis and remove them
    # 3. Or implement token versioning
    
    return {"message": "Successfully logged out"}


@router.post("/change-password", response_model=Dict[str, str])
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change password for current user.
    
    Args:
        password_data: Current and new password
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If current password incorrect
    """
    # Verify current password
    if not authenticate_user(db, current_user.username, password_data.current_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Update password
    current_user.password_hash = get_password_hash(password_data.new_password)
    db.commit()
    
    return {"message": "Password successfully changed"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current user information.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User information
    """
    return current_user