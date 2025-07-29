from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

from ..models.interaction import InteractionAction
from .suggestion import SuggestionResponse


class InteractionBase(BaseModel):
    """Base schema for interaction."""
    action: InteractionAction
    feedback: Optional[str] = Field(None, max_length=500)
    extra_data: Optional[str] = None


class InteractionCreate(InteractionBase):
    """Schema for creating an interaction."""
    suggestion_id: UUID


class InteractionResponse(InteractionBase):
    """Schema for interaction response."""
    id: UUID
    user_id: UUID
    suggestion_id: UUID
    timestamp: datetime
    suggestion: Optional[SuggestionResponse] = None
    
    class Config:
        from_attributes = True


class InteractionStats(BaseModel):
    """Schema for interaction statistics."""
    total_interactions: int
    by_action: dict
    recent_interactions: list


class InteractionFilter(BaseModel):
    """Schema for filtering interactions."""
    action: Optional[InteractionAction] = None
    suggestion_id: Optional[UUID] = None
    date_range: Optional[str] = Field(None, pattern="^(today|week|month|year)$")
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None