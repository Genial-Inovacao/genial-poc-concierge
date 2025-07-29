from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any
from datetime import date, datetime
from uuid import UUID

from ..utils.validators import sanitize_input


class ProfileBase(BaseModel):
    """Base schema for profile."""
    name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    birth_date: Optional[date] = None
    spouse_name: Optional[str] = Field(None, max_length=100)
    spouse_birth_date: Optional[date] = None
    
    @field_validator('name')
    def sanitize_name(cls, v):
        if v is None:
            return v
        return sanitize_input(v)
    
    @field_validator('spouse_name')
    def sanitize_spouse_name(cls, v):
        if v is None:
            return v
        return sanitize_input(v)


class ProfileCreate(ProfileBase):
    """Schema for creating a profile."""
    pass


class ProfileUpdate(ProfileBase):
    """Schema for updating a profile."""
    pass


class ProfileResponse(ProfileBase):
    """Schema for profile response."""
    id: UUID
    user_id: UUID
    preferences_json: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PreferencesUpdate(BaseModel):
    """Schema for updating user preferences."""
    notifications: Optional[Dict[str, bool]] = None
    suggestion_categories: Optional[Dict[str, bool]] = None
    quiet_hours: Optional[Dict[str, Any]] = None
    suggestion_frequency: Optional[str] = Field(None, pattern="^(low|normal|high)$")
    max_daily_suggestions: Optional[int] = Field(None, ge=1, le=20)
    categories_of_interest: Optional[list[str]] = None
    preferred_times: Optional[Dict[str, bool]] = None
    
    @field_validator('quiet_hours')
    def validate_quiet_hours(cls, v):
        if v and 'enabled' in v:
            if v['enabled'] and ('start' not in v or 'end' not in v):
                raise ValueError("When quiet hours are enabled, start and end times must be provided")
        return v


class UserWithProfile(BaseModel):
    """Schema for user with profile information."""
    id: UUID
    username: str
    email: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    profile: Optional[ProfileResponse] = None
    
    class Config:
        from_attributes = True


class UserStats(BaseModel):
    """Schema for user statistics."""
    days_active: int
    total_interactions: int
    total_suggestions: int
    accepted_suggestions: int
    rejected_suggestions: int
    executed_suggestions: int
    acceptance_rate: float
    most_common_suggestion_type: Optional[str] = None
    last_activity: Optional[datetime] = None