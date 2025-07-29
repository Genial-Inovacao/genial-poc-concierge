from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
import json

from ..models.suggestion import SuggestionStatus, SuggestionType
from ..utils.validators import sanitize_input


class SuggestionBase(BaseModel):
    """Base schema for suggestion."""
    content: str
    type: SuggestionType
    priority: int = Field(5, ge=1, le=10)
    scheduled_date: datetime
    context_data: Optional[str] = None
    
    @field_validator('content')
    def sanitize_content(cls, v):
        return sanitize_input(v)
    
    @field_validator('context_data')
    def validate_context_data(cls, v):
        if v:
            try:
                # Validate it's valid JSON
                json.loads(v)
            except json.JSONDecodeError:
                raise ValueError("Context data must be valid JSON")
        return v


class SuggestionCreate(SuggestionBase):
    """Schema for creating a suggestion (admin/system only)."""
    user_id: UUID
    status: SuggestionStatus = SuggestionStatus.PENDING


class SuggestionUpdate(BaseModel):
    """Schema for updating a suggestion."""
    content: Optional[str] = None
    priority: Optional[int] = Field(None, ge=1, le=10)
    scheduled_date: Optional[datetime] = None
    status: Optional[SuggestionStatus] = None
    context_data: Optional[str] = None
    
    @field_validator('content')
    def sanitize_content(cls, v):
        if v:
            return sanitize_input(v)
        return v
    
    @field_validator('context_data')
    def validate_context_data(cls, v):
        if v:
            try:
                json.loads(v)
            except json.JSONDecodeError:
                raise ValueError("Context data must be valid JSON")
        return v


class SuggestionResponse(SuggestionBase):
    """Schema for suggestion response."""
    id: UUID
    user_id: UUID
    status: SuggestionStatus
    created_at: datetime
    executed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class SuggestionInteraction(BaseModel):
    """Schema for interacting with a suggestion."""
    action: str = Field(..., pattern="^(accept|reject|snooze|execute)$")
    feedback: Optional[str] = Field(None, max_length=500)
    snooze_hours: Optional[int] = Field(None, ge=1, le=168)  # Max 1 week
    
    @field_validator('feedback')
    def sanitize_feedback(cls, v):
        if v:
            return sanitize_input(v)
        return v
    
    @field_validator('snooze_hours')
    def validate_snooze(cls, v, values):
        if v is not None and values.get('action') != 'snooze':
            raise ValueError("Snooze hours can only be set when action is 'snooze'")
        if values.get('action') == 'snooze' and v is None:
            raise ValueError("Snooze hours must be provided when action is 'snooze'")
        return v


class SuggestionFilter(BaseModel):
    """Schema for filtering suggestions."""
    status: Optional[SuggestionStatus] = None
    type: Optional[SuggestionType] = None
    priority_min: Optional[int] = Field(None, ge=1, le=10)
    priority_max: Optional[int] = Field(None, ge=1, le=10)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    
    @field_validator('priority_max')
    def validate_priority_range(cls, v, values):
        if v and 'priority_min' in values and values['priority_min']:
            if v < values['priority_min']:
                raise ValueError("Max priority must be greater than or equal to min priority")
        return v
    
    @field_validator('end_date')
    def validate_date_range(cls, v, values):
        if v and 'start_date' in values and values['start_date']:
            if v < values['start_date']:
                raise ValueError("End date must be after start date")
        return v


class SuggestionStats(BaseModel):
    """Schema for suggestion statistics."""
    total_suggestions: int
    pending_suggestions: int
    accepted_suggestions: int
    rejected_suggestions: int
    executed_suggestions: int
    acceptance_rate: float
    execution_rate: float
    by_type: Dict[str, int]
    by_status: Dict[str, int]
    average_time_to_action: Optional[float] = None  # In hours