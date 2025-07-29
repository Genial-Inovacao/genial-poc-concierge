from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Enum, Index
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime, timezone
import enum

from ..database import Base
from ..utils.database_types import GUID


class SuggestionStatus(str, enum.Enum):
    """Enumeration for suggestion status."""
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXECUTED = "executed"
    SNOOZED = "snoozed"
    EXPIRED = "expired"


class SuggestionType(str, enum.Enum):
    """Enumeration for suggestion types."""
    ANNIVERSARY = "anniversary"
    PURCHASE = "purchase"
    ROUTINE = "routine"
    SEASONAL = "seasonal"
    SAVINGS = "savings"
    REMINDER = "reminder"
    RECOMMENDATION = "recommendation"


class Suggestion(Base):
    """Suggestion model for AI-generated recommendations."""
    
    __tablename__ = "suggestions"
    
    # Primary key
    id = Column(
        GUID(),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    
    # Foreign key to user
    user_id = Column(
        GUID(),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Suggestion details
    content = Column(Text, nullable=False)
    
    type = Column(
        Enum(SuggestionType),
        nullable=False,
        index=True
    )
    
    priority = Column(
        Integer,
        nullable=False,
        default=5
    )  # 1-10, where 10 is highest priority
    
    status = Column(
        Enum(SuggestionStatus),
        nullable=False,
        default=SuggestionStatus.PENDING,
        index=True
    )
    
    scheduled_date = Column(
        DateTime(timezone=True),
        nullable=False,
        index=True
    )
    
    # Additional metadata
    context_data = Column(
        Text,
        nullable=True
    )  # JSON string with additional context
    
    # Timestamp fields
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    
    executed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )
    
    # Relationships
    user = relationship("User", back_populates="suggestions")
    interactions = relationship(
        "Interaction",
        back_populates="suggestion",
        cascade="all, delete-orphan"
    )
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_user_status', 'user_id', 'status'),
        Index('idx_user_scheduled', 'user_id', 'scheduled_date'),
        Index('idx_user_type', 'user_id', 'type'),
    )
    
    def __repr__(self):
        return f"<Suggestion(id={self.id}, type={self.type}, status={self.status}, priority={self.priority})>"
    
    def mark_as_executed(self):
        """Mark suggestion as executed."""
        self.status = SuggestionStatus.EXECUTED
        self.executed_at = datetime.now(timezone.utc)
    
    def mark_as_accepted(self):
        """Mark suggestion as accepted."""
        self.status = SuggestionStatus.ACCEPTED
    
    def mark_as_rejected(self):
        """Mark suggestion as rejected."""
        self.status = SuggestionStatus.REJECTED
    
    def mark_as_snoozed(self):
        """Mark suggestion as snoozed."""
        self.status = SuggestionStatus.SNOOZED
    
    @property
    def is_active(self) -> bool:
        """Check if suggestion is still active (pending or snoozed)."""
        return self.status in [SuggestionStatus.PENDING, SuggestionStatus.SNOOZED]
    
    @property
    def is_overdue(self) -> bool:
        """Check if suggestion is overdue."""
        return (
            self.is_active and
            self.scheduled_date < datetime.now(timezone.utc)
        )