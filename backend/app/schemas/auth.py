from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
from uuid import UUID

from ..utils.validators import validate_password_strength, validate_username


class UserCreate(BaseModel):
    """Schema for user registration."""
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(..., min_length=8)
    
    @field_validator('username')
    def validate_username(cls, v):
        is_valid, error = validate_username(v)
        if not is_valid:
            raise ValueError(error)
        return v.lower()  # Store usernames in lowercase
    
    @field_validator('password')
    def validate_password(cls, v):
        is_valid, error = validate_password_strength(v)
        if not is_valid:
            raise ValueError(error)
        return v


class UserLogin(BaseModel):
    """Schema for user login."""
    username: str  # Can be username or email
    password: str


class TokenResponse(BaseModel):
    """Schema for token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    """Schema for token refresh."""
    refresh_token: str


class UserResponse(BaseModel):
    """Schema for user response (safe to send to client)."""
    id: UUID
    username: str
    email: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PasswordChange(BaseModel):
    """Schema for password change."""
    current_password: str
    new_password: str = Field(..., min_length=8)
    
    @field_validator('new_password')
    def validate_new_password(cls, v, values):
        is_valid, error = validate_password_strength(v)
        if not is_valid:
            raise ValueError(error)
        
        # Check that new password is different from current
        if 'current_password' in values and v == values['current_password']:
            raise ValueError("New password must be different from current password")
        
        return v


class PasswordReset(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Schema for password reset confirmation."""
    token: str
    new_password: str = Field(..., min_length=8)
    
    @field_validator('new_password')
    def validate_new_password(cls, v):
        is_valid, error = validate_password_strength(v)
        if not is_valid:
            raise ValueError(error)
        return v