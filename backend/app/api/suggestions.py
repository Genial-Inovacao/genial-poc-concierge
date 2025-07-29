from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone, timedelta
from uuid import UUID
import json

from ..database import get_db
from ..models import User, Suggestion, Interaction, SuggestionStatus, SuggestionType, InteractionAction
from ..schemas import (
    SuggestionCreate,
    SuggestionUpdate,
    SuggestionResponse,
    SuggestionInteraction,
    SuggestionFilter,
    SuggestionStats
)
from ..services.auth import get_current_active_user

router = APIRouter(prefix="/suggestions", tags=["Suggestions"])


@router.get("/", response_model=List[SuggestionResponse])
async def list_suggestions(
    status: Optional[SuggestionStatus] = None,
    type: Optional[SuggestionType] = None,
    category: Optional[str] = None,  # Added for frontend compatibility
    dateRange: Optional[str] = None,  # Added for frontend compatibility
    priority_min: Optional[int] = Query(None, ge=1, le=10),
    priority_max: Optional[int] = Query(None, ge=1, le=10),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    List user suggestions with optional filters.
    
    Args:
        status: Filter by suggestion status
        type: Filter by suggestion type
        category: Category filter (for frontend compatibility)
        dateRange: Date range filter (today, week, month, all)
        priority_min: Minimum priority (1-10)
        priority_max: Maximum priority (1-10)
        start_date: Filter suggestions scheduled after this date
        end_date: Filter suggestions scheduled before this date
        skip: Number of items to skip (pagination)
        limit: Number of items to return
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List of suggestions
    """
    # Process dateRange parameter
    if dateRange and not start_date and not end_date:
        now = datetime.now(timezone.utc)
        if dateRange == "today":
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        elif dateRange == "week":
            start_date = now - timedelta(days=7)
            end_date = now
        elif dateRange == "month":
            start_date = now - timedelta(days=30)
            end_date = now
        # "all" means no date filter
    
    # Build query
    query = db.query(Suggestion).filter(Suggestion.user_id == current_user.id)
    
    # Apply filters
    if status:
        query = query.filter(Suggestion.status == status)
    
    if type:
        query = query.filter(Suggestion.type == type)
    
    if priority_min is not None:
        query = query.filter(Suggestion.priority >= priority_min)
    
    if priority_max is not None:
        query = query.filter(Suggestion.priority <= priority_max)
    
    if start_date:
        query = query.filter(Suggestion.scheduled_date >= start_date)
    
    if end_date:
        query = query.filter(Suggestion.scheduled_date <= end_date)
    
    # Order by priority (desc) and scheduled date (asc)
    query = query.order_by(
        Suggestion.priority.desc(),
        Suggestion.scheduled_date.asc()
    )
    
    # Apply pagination
    suggestions = query.offset(skip).limit(limit).all()
    
    # Mark as viewed
    for suggestion in suggestions:
        if suggestion.status == SuggestionStatus.PENDING:
            # Check if already viewed
            existing_view = db.query(Interaction).filter(
                and_(
                    Interaction.user_id == current_user.id,
                    Interaction.suggestion_id == suggestion.id,
                    Interaction.action == InteractionAction.VIEWED
                )
            ).first()
            
            if not existing_view:
                # Create viewed interaction
                view_interaction = Interaction(
                    user_id=current_user.id,
                    suggestion_id=suggestion.id,
                    action=InteractionAction.VIEWED
                )
                db.add(view_interaction)
    
    db.commit()
    
    return suggestions


@router.get("/stats", response_model=SuggestionStats)
async def get_suggestion_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get suggestion statistics for the current user.
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Suggestion statistics
    """
    # Get total counts by status
    total_suggestions = db.query(Suggestion).filter(
        Suggestion.user_id == current_user.id
    ).count()
    
    pending_suggestions = db.query(Suggestion).filter(
        Suggestion.user_id == current_user.id,
        Suggestion.status == SuggestionStatus.PENDING
    ).count()
    
    accepted_suggestions = db.query(Suggestion).filter(
        Suggestion.user_id == current_user.id,
        Suggestion.status == SuggestionStatus.ACCEPTED
    ).count()
    
    rejected_suggestions = db.query(Suggestion).filter(
        Suggestion.user_id == current_user.id,
        Suggestion.status == SuggestionStatus.REJECTED
    ).count()
    
    executed_suggestions = db.query(Suggestion).filter(
        Suggestion.user_id == current_user.id,
        Suggestion.status == SuggestionStatus.EXECUTED
    ).count()
    
    # Calculate rates
    acceptance_rate = (accepted_suggestions + executed_suggestions) / total_suggestions if total_suggestions > 0 else 0.0
    execution_rate = executed_suggestions / total_suggestions if total_suggestions > 0 else 0.0
    
    # Count by type
    from sqlalchemy import func
    type_counts = db.query(
        Suggestion.type,
        func.count(Suggestion.id).label('count')
    ).filter(
        Suggestion.user_id == current_user.id
    ).group_by(Suggestion.type).all()
    
    by_type = {str(t): c for t, c in type_counts}
    
    # Count by status
    status_counts = db.query(
        Suggestion.status,
        func.count(Suggestion.id).label('count')
    ).filter(
        Suggestion.user_id == current_user.id
    ).group_by(Suggestion.status).all()
    
    by_status = {str(s): c for s, c in status_counts}
    
    # Calculate average time to action
    executed_with_time = db.query(Suggestion).filter(
        Suggestion.user_id == current_user.id,
        Suggestion.status == SuggestionStatus.EXECUTED,
        Suggestion.executed_at.isnot(None)
    ).all()
    
    if executed_with_time:
        total_hours = sum(
            (s.executed_at - s.created_at).total_seconds() / 3600
            for s in executed_with_time
        )
        average_time_to_action = total_hours / len(executed_with_time)
    else:
        average_time_to_action = None
    
    return SuggestionStats(
        total_suggestions=total_suggestions,
        pending_suggestions=pending_suggestions,
        accepted_suggestions=accepted_suggestions,
        rejected_suggestions=rejected_suggestions,
        executed_suggestions=executed_suggestions,
        acceptance_rate=acceptance_rate,
        execution_rate=execution_rate,
        by_type=by_type,
        by_status=by_status,
        average_time_to_action=average_time_to_action
    )


@router.get("/{suggestion_id}", response_model=SuggestionResponse)
async def get_suggestion(
    suggestion_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific suggestion.
    
    Args:
        suggestion_id: Suggestion ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Suggestion details
        
    Raises:
        HTTPException: If suggestion not found or not owned by user
    """
    suggestion = db.query(Suggestion).filter(
        Suggestion.id == suggestion_id,
        Suggestion.user_id == current_user.id
    ).first()
    
    if not suggestion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Suggestion not found"
        )
    
    return suggestion


@router.post("/", response_model=SuggestionResponse)
async def create_suggestion(
    suggestion_data: SuggestionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new suggestion (admin/system only in production).
    
    For demo purposes, users can create their own suggestions.
    
    Args:
        suggestion_data: Suggestion data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Created suggestion
    """
    # In production, this would be restricted to admin/system only
    # For now, allow users to create their own suggestions for testing
    
    new_suggestion = Suggestion(
        user_id=current_user.id,
        content=suggestion_data.content,
        type=suggestion_data.type,
        priority=suggestion_data.priority,
        scheduled_date=suggestion_data.scheduled_date,
        context_data=suggestion_data.context_data,
        status=SuggestionStatus.PENDING
    )
    
    db.add(new_suggestion)
    db.commit()
    db.refresh(new_suggestion)
    
    return new_suggestion


@router.put("/{suggestion_id}", response_model=SuggestionResponse)
async def update_suggestion(
    suggestion_id: UUID,
    suggestion_data: SuggestionUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update a suggestion.
    
    Args:
        suggestion_id: Suggestion ID
        suggestion_data: Update data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Updated suggestion
        
    Raises:
        HTTPException: If suggestion not found or not owned by user
    """
    suggestion = db.query(Suggestion).filter(
        Suggestion.id == suggestion_id,
        Suggestion.user_id == current_user.id
    ).first()
    
    if not suggestion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Suggestion not found"
        )
    
    # Update fields
    update_dict = suggestion_data.dict(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(suggestion, field, value)
    
    db.commit()
    db.refresh(suggestion)
    
    return suggestion


@router.post("/{suggestion_id}/interact", response_model=Dict[str, str])
async def interact_with_suggestion(
    suggestion_id: UUID,
    interaction_data: SuggestionInteraction,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Interact with a suggestion (accept, reject, snooze, execute).
    
    Args:
        suggestion_id: Suggestion ID
        interaction_data: Interaction data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If suggestion not found or invalid action
    """
    suggestion = db.query(Suggestion).filter(
        Suggestion.id == suggestion_id,
        Suggestion.user_id == current_user.id
    ).first()
    
    if not suggestion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Suggestion not found"
        )
    
    # Create interaction record
    interaction = Interaction(
        user_id=current_user.id,
        suggestion_id=suggestion_id,
        feedback=interaction_data.feedback
    )
    
    # Handle different actions
    if interaction_data.action == "accept":
        suggestion.mark_as_accepted()
        interaction.action = InteractionAction.ACCEPTED
        message = "Suggestion accepted"
        
    elif interaction_data.action == "reject":
        suggestion.mark_as_rejected()
        interaction.action = InteractionAction.REJECTED
        message = "Suggestion rejected"
        
    elif interaction_data.action == "execute":
        suggestion.mark_as_executed()
        interaction.action = InteractionAction.EXECUTED
        message = "Suggestion marked as executed"
        
    elif interaction_data.action == "snooze":
        if not interaction_data.snooze_hours:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Snooze hours must be provided"
            )
        
        # Update scheduled date
        suggestion.scheduled_date = datetime.now(timezone.utc) + timedelta(hours=interaction_data.snooze_hours)
        suggestion.mark_as_snoozed()
        interaction.action = InteractionAction.SNOOZED
        
        # Store snooze duration in metadata
        interaction.extra_data = json.dumps({"snooze_hours": interaction_data.snooze_hours})
        message = f"Suggestion snoozed for {interaction_data.snooze_hours} hours"
    
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid action"
        )
    
    db.add(interaction)
    db.commit()
    
    return {"message": message, "suggestion_id": str(suggestion_id)}


@router.delete("/{suggestion_id}", response_model=Dict[str, str])
async def delete_suggestion(
    suggestion_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete a suggestion.
    
    Args:
        suggestion_id: Suggestion ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If suggestion not found or not owned by user
    """
    suggestion = db.query(Suggestion).filter(
        Suggestion.id == suggestion_id,
        Suggestion.user_id == current_user.id
    ).first()
    
    if not suggestion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Suggestion not found"
        )
    
    db.delete(suggestion)
    db.commit()
    
    return {"message": "Suggestion deleted successfully"}