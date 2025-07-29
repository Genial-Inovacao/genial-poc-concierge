from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime, timezone

from ..database import Base
from ..utils.database_types import GUID


class User(Base):
    """User model for authentication and profile management."""
    
    __tablename__ = "users"
    
    # Primary key
    id = Column(
        GUID(),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    
    # Authentication fields
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    # Status fields
    is_active = Column(Boolean, default=True, nullable=False)
    
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
    profile = relationship(
        "Profile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    transactions = relationship(
        "Transaction",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    suggestions = relationship(
        "Suggestion",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    interactions = relationship(
        "Interaction",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"