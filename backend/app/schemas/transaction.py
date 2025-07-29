from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from ..utils.validators import sanitize_input


class TransactionBase(BaseModel):
    """Base schema for transaction."""
    type: str = Field(..., max_length=50)
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    date: datetime
    category: str = Field(..., max_length=50)
    location: Optional[str] = Field(None, max_length=255)
    description: str = Field(..., max_length=500)
    
    @field_validator('type', 'category')
    def validate_type_category(cls, v):
        if not v or not v.strip():
            raise ValueError("Cannot be empty")
        return v.lower().strip()
    
    @field_validator('description', 'location')
    def sanitize_text_fields(cls, v):
        if v:
            return sanitize_input(v)
        return v


class TransactionCreate(TransactionBase):
    """Schema for creating a transaction."""
    pass


class TransactionUpdate(BaseModel):
    """Schema for updating a transaction."""
    type: Optional[str] = Field(None, max_length=50)
    amount: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    date: Optional[datetime] = None
    category: Optional[str] = Field(None, max_length=50)
    location: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=500)
    
    @field_validator('type', 'category')
    def validate_type_category(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError("Cannot be empty")
            return v.lower().strip()
        return v
    
    @field_validator('description', 'location')
    def sanitize_text_fields(cls, v):
        if v:
            return sanitize_input(v)
        return v


class TransactionResponse(TransactionBase):
    """Schema for transaction response."""
    id: UUID
    user_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


class TransactionFilter(BaseModel):
    """Schema for filtering transactions."""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    category: Optional[str] = None
    type: Optional[str] = None
    min_amount: Optional[Decimal] = Field(None, ge=0)
    max_amount: Optional[Decimal] = Field(None, ge=0)
    
    @field_validator('end_date')
    def validate_date_range(cls, v, values):
        if v and 'start_date' in values and values['start_date']:
            if v < values['start_date']:
                raise ValueError("End date must be after start date")
        return v


class TransactionAnalytics(BaseModel):
    """Schema for transaction analytics."""
    total_spent: Decimal
    average_transaction: Decimal
    transaction_count: int
    by_category: Dict[str, Decimal]
    by_type: Dict[str, Decimal]
    spending_trend: List[Dict[str, Any]]  # Date and amount pairs
    most_frequent_category: Optional[str] = None
    most_expensive_category: Optional[str] = None