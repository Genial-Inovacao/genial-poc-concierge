from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Enum, Index
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime, timezone
import enum

from ..database import Base
from ..utils.database_types import GUID


class InteractionAction(str, enum.Enum):
    """Enumeration for interaction actions."""
    VIEWED = "viewed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    SNOOZED = "snoozed"
    EXECUTED = "executed"
    DISMISSED = "dismissed"
    CLICKED = "clicked"


class Interaction(Base):
    """Interaction model for tracking user engagement with suggestions."""
    
    __tablename__ = "interactions"
    
    # Primary key
    id = Column(
        GUID(),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    
    # Foreign keys
    user_id = Column(
        GUID(),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    suggestion_id = Column(
        GUID(),
        ForeignKey("suggestions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Interaction details
    action = Column(
        Enum(InteractionAction),
        nullable=False,
        index=True
    )
    
    timestamp = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True
    )
    
    feedback = Column(Text, nullable=True)  # Optional user feedback
    
    # Additional metadata
    extra_data = Column(
        Text,
        nullable=True
    )  # JSON string with additional data (e.g., snooze duration)
    
    # Relationships
    user = relationship("User", back_populates="interactions")
    suggestion = relationship("Suggestion", back_populates="interactions")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_user_timestamp', 'user_id', 'timestamp'),
        Index('idx_suggestion_action', 'suggestion_id', 'action'),
        Index('idx_user_suggestion', 'user_id', 'suggestion_id'),
    )
    
    def __repr__(self):
        return f"<Interaction(id={self.id}, action={self.action}, timestamp={self.timestamp})>"
    
    @classmethod
    def create_viewed(cls, user_id: str, suggestion_id: str):
        """Create a 'viewed' interaction."""
        return cls(
            user_id=user_id,
            suggestion_id=suggestion_id,
            action=InteractionAction.VIEWED
        )
    
    @classmethod
    def create_with_feedback(cls, user_id: str, suggestion_id: str, action: InteractionAction, feedback: str = None):
        """
        Create an interaction with optional feedback.
        
        Args:
            user_id: User ID
            suggestion_id: Suggestion ID
            action: Interaction action
            feedback: Optional feedback text
            
        Returns:
            Interaction instance
        """
        return cls(
            user_id=user_id,
            suggestion_id=suggestion_id,
            action=action,
            feedback=feedback
        )
    
    @property
    def is_positive(self) -> bool:
        """Check if interaction is positive (accepted or executed)."""
        return self.action in [InteractionAction.ACCEPTED, InteractionAction.EXECUTED]
    
    @property
    def is_negative(self) -> bool:
        """Check if interaction is negative (rejected or dismissed)."""
        return self.action in [InteractionAction.REJECTED, InteractionAction.DISMISSED]