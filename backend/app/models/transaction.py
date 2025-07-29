from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric, Index, Text
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime, timezone
from decimal import Decimal

from ..database import Base
from ..utils.database_types import GUID


class Transaction(Base):
    """Transaction model for tracking user financial activities."""
    
    __tablename__ = "transactions"
    
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
    
    # Transaction details
    type = Column(
        String(50),
        nullable=False,
        index=True
    )  # purchase, service, subscription, etc.
    
    amount = Column(
        Numeric(10, 2),
        nullable=False
    )
    
    date = Column(
        DateTime(timezone=True),
        nullable=False,
        index=True
    )
    
    category = Column(
        String(50),
        nullable=False,
        index=True
    )  # food, entertainment, utilities, etc.
    
    location = Column(String(255), nullable=True)
    description = Column(String(500), nullable=False)
    metadata_json = Column(Text, nullable=True)  # JSON string for additional metadata
    
    # Timestamp fields
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    
    # Relationships
    user = relationship("User", back_populates="transactions")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_user_date', 'user_id', 'date'),
        Index('idx_user_category', 'user_id', 'category'),
    )
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, type={self.type}, amount={self.amount}, category={self.category})>"
    
    @property
    def amount_float(self) -> float:
        """Get amount as float."""
        return float(self.amount)
    
    @classmethod
    def create_from_dict(cls, data: dict, user_id: str):
        """
        Create a transaction from dictionary data.
        
        Args:
            data: Dictionary with transaction data
            user_id: User ID
            
        Returns:
            Transaction instance
        """
        return cls(
            user_id=user_id,
            type=data.get('type'),
            amount=Decimal(str(data.get('amount', 0))),
            date=data.get('date', datetime.now(timezone.utc)),
            category=data.get('category'),
            location=data.get('location'),
            description=data.get('description')
        )