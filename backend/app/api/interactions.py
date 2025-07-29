from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone, timedelta
from uuid import UUID

from ..database import get_db
from ..models import User, Interaction, Suggestion, InteractionAction
from ..schemas import InteractionResponse
from ..services.auth import get_current_active_user

router = APIRouter(prefix="/interactions", tags=["Interactions"])


@router.get("/", response_model=List[InteractionResponse])
async def list_interactions(
    action: Optional[InteractionAction] = None,
    suggestion_id: Optional[UUID] = None,
    date_range: Optional[str] = Query(None, pattern="^(today|week|month|year)$"),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    List user interactions with suggestions.
    
    Args:
        action: Filter by interaction action (viewed, accepted, rejected, etc.)
        suggestion_id: Filter by specific suggestion
        date_range: Predefined date range (today, week, month, year)
        start_date: Filter interactions after this date
        end_date: Filter interactions before this date
        skip: Number of items to skip (pagination)
        limit: Number of items to return
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List of interactions with suggestion details
    """
    # Process date_range parameter
    if date_range and not start_date and not end_date:
        now = datetime.now(timezone.utc)
        if date_range == "today":
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        elif date_range == "week":
            start_date = now - timedelta(days=7)
            end_date = now
        elif date_range == "month":
            start_date = now - timedelta(days=30)
            end_date = now
        elif date_range == "year":
            start_date = now - timedelta(days=365)
            end_date = now
    
    # Build query
    query = db.query(Interaction).filter(Interaction.user_id == current_user.id)
    
    # Apply filters
    if action:
        query = query.filter(Interaction.action == action)
    
    if suggestion_id:
        query = query.filter(Interaction.suggestion_id == suggestion_id)
    
    if start_date:
        query = query.filter(Interaction.timestamp >= start_date)
    
    if end_date:
        query = query.filter(Interaction.timestamp <= end_date)
    
    # Order by timestamp descending (most recent first)
    query = query.order_by(Interaction.timestamp.desc())
    
    # Apply pagination
    interactions = query.offset(skip).limit(limit).all()
    
    return interactions


@router.get("/stats")
async def get_interaction_stats(
    date_range: Optional[str] = Query("month", pattern="^(today|week|month|year|all)$"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get interaction statistics for the current user.
    
    Args:
        date_range: Date range for statistics
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Interaction statistics
    """
    # Process date range
    now = datetime.now(timezone.utc)
    start_date = None
    
    if date_range != "all":
        if date_range == "today":
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif date_range == "week":
            start_date = now - timedelta(days=7)
        elif date_range == "month":
            start_date = now - timedelta(days=30)
        elif date_range == "year":
            start_date = now - timedelta(days=365)
    
    # Build base query
    base_query = db.query(Interaction).filter(Interaction.user_id == current_user.id)
    if start_date:
        base_query = base_query.filter(Interaction.timestamp >= start_date)
    
    # Count by action
    from sqlalchemy import func
    action_counts = base_query.with_entities(
        Interaction.action,
        func.count(Interaction.id).label('count')
    ).group_by(Interaction.action).all()
    
    by_action = {str(action): count for action, count in action_counts}
    
    # Total interactions
    total_interactions = sum(by_action.values())
    
    # Get most recent interactions
    recent_interactions = base_query.order_by(
        Interaction.timestamp.desc()
    ).limit(5).all()
    
    return {
        "total_interactions": total_interactions,
        "by_action": by_action,
        "recent_interactions": [
            {
                "id": str(i.id),
                "action": str(i.action),
                "timestamp": i.timestamp.isoformat(),
                "suggestion_id": str(i.suggestion_id) if i.suggestion_id else None
            }
            for i in recent_interactions
        ]
    }


@router.get("/{interaction_id}", response_model=InteractionResponse)
async def get_interaction(
    interaction_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific interaction.
    
    Args:
        interaction_id: Interaction ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Interaction details
        
    Raises:
        HTTPException: If interaction not found or not owned by user
    """
    interaction = db.query(Interaction).filter(
        Interaction.id == interaction_id,
        Interaction.user_id == current_user.id
    ).first()
    
    if not interaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interaction not found"
        )
    
    return interaction