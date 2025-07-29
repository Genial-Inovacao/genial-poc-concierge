from sqlalchemy import Column, String, Date, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime, timezone

from ..database import Base
from ..utils.database_types import GUID


class Profile(Base):
    """User profile model for storing personal information and preferences."""
    
    __tablename__ = "profiles"
    
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
        unique=True,
        nullable=False,
        index=True
    )
    
    # Personal information
    name = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    birth_date = Column(Date, nullable=True)
    spouse_name = Column(String(100), nullable=True)
    spouse_birth_date = Column(Date, nullable=True)
    
    # Preferences stored as JSON
    preferences_json = Column(
        JSON,
        default=lambda: {
            "notifications": {
                "email": True,
                "push": True,
                "sms": False
            },
            "suggestion_categories": {
                "anniversary": True,
                "purchase": True,
                "routine": True,
                "seasonal": True
            },
            "quiet_hours": {
                "enabled": False,
                "start": "22:00",
                "end": "08:00"
            },
            "suggestion_frequency": "normal",  # low, normal, high
            "max_daily_suggestions": 5,
            "categories_of_interest": [],
            "preferred_times": {
                "morning": True,
                "afternoon": True,
                "evening": True,
                "night": True
            }
        },
        nullable=False
    )
    
    # Timestamp fields
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    
    # Relationships
    user = relationship("User", back_populates="profile")
    
    def __repr__(self):
        return f"<Profile(id={self.id}, user_id={self.user_id})>"
    
    @property
    def has_spouse_info(self):
        """Check if spouse information is available."""
        return bool(self.spouse_name and self.spouse_birth_date)
    
    def get_preference(self, key: str, default=None):
        """
        Get a specific preference value.
        
        Args:
            key: Dot-notation key (e.g., 'notifications.email')
            default: Default value if key not found
            
        Returns:
            Preference value or default
        """
        keys = key.split('.')
        value = self.preferences_json
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set_preference(self, key: str, value):
        """
        Set a specific preference value.
        
        Args:
            key: Dot-notation key (e.g., 'notifications.email')
            value: Value to set
        """
        keys = key.split('.')
        prefs = self.preferences_json.copy()
        
        # Navigate to the nested key
        current = prefs
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        # Set the value
        current[keys[-1]] = value
        self.preferences_json = prefs