from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from typing import Dict, Any
from datetime import datetime, timezone, timedelta
import json

from ..database import get_db
from ..models import User, Profile, Transaction, Suggestion, Interaction
from ..schemas import (
    ProfileCreate,
    ProfileUpdate,
    ProfileResponse,
    PreferencesUpdate,
    UserWithProfile,
    UserStats,
    UserResponse
)
from ..services.auth import get_current_active_user
from ..services.ai_engine import AIEngine

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user basic information.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User information
    """
    return current_user


@router.get("/me/profile", response_model=UserWithProfile)
async def get_user_profile(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get current user with profile information.
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        User with profile information
    """
    # Load profile relationship
    user_with_profile = db.query(User).filter(
        User.id == current_user.id
    ).first()
    
    return user_with_profile


@router.post("/me/profile", response_model=ProfileResponse)
async def create_user_profile(
    profile_data: ProfileCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create or update user profile.
    
    Args:
        profile_data: Profile data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Created/updated profile
    """
    # Check if profile already exists
    existing_profile = db.query(Profile).filter(
        Profile.user_id == current_user.id
    ).first()
    
    if existing_profile:
        # Update existing profile
        for field, value in profile_data.dict(exclude_unset=True).items():
            setattr(existing_profile, field, value)
        existing_profile.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(existing_profile)
        return existing_profile
    else:
        # This shouldn't happen as profile is created during registration
        # But handle it just in case
        new_profile = Profile(
            user_id=current_user.id,
            **profile_data.dict()
        )
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
        return new_profile


@router.put("/me/profile", response_model=ProfileResponse)
async def update_user_profile(
    profile_data: ProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update user profile.
    
    Args:
        profile_data: Profile update data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Updated profile
    """
    # Get existing profile
    profile = db.query(Profile).filter(
        Profile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    # Debug log
    update_dict = profile_data.dict(exclude_unset=True)
    print(f"Updating profile for user {current_user.username}: {update_dict}")
    
    # Track important changes
    important_changes = []
    
    # Check for important field changes
    for field, new_value in update_dict.items():
        old_value = getattr(profile, field)
        
        # Detect significant changes
        if field in ['birth_date', 'spouse_name', 'spouse_birth_date'] and old_value != new_value:
            important_changes.append({
                'field': field,
                'old_value': str(old_value) if old_value else None,
                'new_value': str(new_value) if new_value else None
            })
        
        print(f"Setting {field} = {new_value}")
        setattr(profile, field, new_value)
    
    profile.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(profile)
    
    # Create audit transaction if important fields changed
    if important_changes:
        audit_transaction = Transaction(
            user_id=current_user.id,
            type='system',
            amount=0,
            date=datetime.now(timezone.utc),
            category='profile_update',
            description='Atualização de perfil',
            metadata_json=json.dumps({
                'changes': important_changes,
                'timestamp': datetime.now(timezone.utc).isoformat()
            })
        )
        db.add(audit_transaction)
        db.commit()
        
        # Trigger AI analysis for new suggestions
        try:
            ai_engine = AIEngine(db)
            new_suggestions = ai_engine.analyze_user(current_user)
            
            # Save new suggestions
            for suggestion_data in new_suggestions:
                # Check if similar suggestion already exists
                existing = db.query(Suggestion).filter(
                    Suggestion.user_id == current_user.id,
                    Suggestion.content == suggestion_data['content'],
                    Suggestion.status.in_(['pending', 'accepted'])
                ).first()
                
                if not existing:
                    suggestion = Suggestion(
                        user_id=current_user.id,
                        **suggestion_data
                    )
                    db.add(suggestion)
            
            db.commit()
            print(f"Generated {len(new_suggestions)} new suggestions after profile update")
        except Exception as e:
            print(f"Error running AI analysis after profile update: {e}")
    
    # Debug after save
    print(f"Profile after save - name: {profile.name}, phone: {profile.phone}")
    
    return profile


@router.get("/me/preferences", response_model=Dict[str, Any])
async def get_user_preferences(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get user preferences.
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        User preferences
    """
    profile = db.query(Profile).filter(
        Profile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    return profile.preferences_json


@router.put("/me/preferences", response_model=Dict[str, Any])
async def update_user_preferences(
    preferences: PreferencesUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update user preferences.
    
    Args:
        preferences: Preferences update data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Updated preferences
    """
    profile = db.query(Profile).filter(
        Profile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    # Update preferences
    current_prefs = profile.preferences_json.copy()
    old_prefs = current_prefs.copy()
    
    # Update only provided fields
    update_data = preferences.dict(exclude_unset=True)
    for key, value in update_data.items():
        if isinstance(value, dict) and key in current_prefs:
            # Merge nested dictionaries
            current_prefs[key].update(value)
        else:
            current_prefs[key] = value
    
    # Force SQLAlchemy to detect the change in JSON column
    profile.preferences_json = current_prefs
    flag_modified(profile, 'preferences_json')
    profile.updated_at = datetime.now(timezone.utc)
    
    # Debug log
    print(f"Updating preferences for user {current_user.username}: {current_prefs}")
    
    db.commit()
    db.refresh(profile)
    
    # Check if important preferences changed
    important_pref_changes = []
    if old_prefs.get('categories_of_interest') != current_prefs.get('categories_of_interest'):
        important_pref_changes.append('categories_of_interest')
    if old_prefs.get('preferred_times') != current_prefs.get('preferred_times'):
        important_pref_changes.append('preferred_times')
    if old_prefs.get('notification_preferences') != current_prefs.get('notification_preferences'):
        important_pref_changes.append('notification_preferences')
    
    # Create audit transaction and trigger AI if preferences changed significantly
    if important_pref_changes:
        audit_transaction = Transaction(
            user_id=current_user.id,
            type='system',
            amount=0,
            date=datetime.now(timezone.utc),
            category='preferences_update',
            description='Atualização de preferências',
            metadata_json=json.dumps({
                'changed_preferences': important_pref_changes,
                'timestamp': datetime.now(timezone.utc).isoformat()
            })
        )
        db.add(audit_transaction)
        db.commit()
        
        # Trigger AI analysis
        try:
            ai_engine = AIEngine(db)
            new_suggestions = ai_engine.analyze_user(current_user)
            
            for suggestion_data in new_suggestions:
                existing = db.query(Suggestion).filter(
                    Suggestion.user_id == current_user.id,
                    Suggestion.content == suggestion_data['content'],
                    Suggestion.status.in_(['pending', 'accepted'])
                ).first()
                
                if not existing:
                    suggestion = Suggestion(
                        user_id=current_user.id,
                        **suggestion_data
                    )
                    db.add(suggestion)
            
            db.commit()
            print(f"Generated {len(new_suggestions)} new suggestions after preferences update")
        except Exception as e:
            print(f"Error running AI analysis after preferences update: {e}")
    
    return profile.preferences_json


@router.get("/me/stats", response_model=UserStats)
async def get_user_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get user statistics.
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        User statistics
    """
    # Calculate days active
    # Ensure both datetimes are timezone-aware
    now = datetime.now(timezone.utc)
    created_at = current_user.created_at
    if created_at.tzinfo is None:
        # If created_at is naive, assume it's UTC
        created_at = created_at.replace(tzinfo=timezone.utc)
    days_active = (now - created_at).days + 1
    
    # Get interaction counts
    total_interactions = db.query(Interaction).filter(
        Interaction.user_id == current_user.id
    ).count()
    
    # Get suggestion counts
    total_suggestions = db.query(Suggestion).filter(
        Suggestion.user_id == current_user.id
    ).count()
    
    accepted_suggestions = db.query(Suggestion).filter(
        Suggestion.user_id == current_user.id,
        Suggestion.status == "accepted"
    ).count()
    
    rejected_suggestions = db.query(Suggestion).filter(
        Suggestion.user_id == current_user.id,
        Suggestion.status == "rejected"
    ).count()
    
    executed_suggestions = db.query(Suggestion).filter(
        Suggestion.user_id == current_user.id,
        Suggestion.status == "executed"
    ).count()
    
    # Calculate acceptance rate
    if total_suggestions > 0:
        acceptance_rate = (accepted_suggestions + executed_suggestions) / total_suggestions
    else:
        acceptance_rate = 0.0
    
    # Get most common suggestion type
    from sqlalchemy import func
    most_common_type_result = db.query(
        Suggestion.type,
        func.count(Suggestion.type).label('count')
    ).filter(
        Suggestion.user_id == current_user.id
    ).group_by(
        Suggestion.type
    ).order_by(
        func.count(Suggestion.type).desc()
    ).first()
    
    most_common_suggestion_type = most_common_type_result[0] if most_common_type_result else None
    
    # Get last activity
    last_interaction = db.query(Interaction).filter(
        Interaction.user_id == current_user.id
    ).order_by(
        Interaction.timestamp.desc()
    ).first()
    
    last_activity = last_interaction.timestamp if last_interaction else current_user.created_at
    
    return UserStats(
        days_active=days_active,
        total_interactions=total_interactions,
        total_suggestions=total_suggestions,
        accepted_suggestions=accepted_suggestions,
        rejected_suggestions=rejected_suggestions,
        executed_suggestions=executed_suggestions,
        acceptance_rate=acceptance_rate,
        most_common_suggestion_type=most_common_suggestion_type,
        last_activity=last_activity
    )


@router.delete("/me", response_model=Dict[str, str])
async def delete_user_account(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete user account and all associated data.
    
    This is a dangerous operation that will delete:
    - User account
    - Profile
    - All transactions
    - All suggestions
    - All interactions
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Success message
    """
    try:
        # Delete user (cascades will handle related data)
        db.delete(current_user)
        db.commit()
        
        return {"message": "Account successfully deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete account"
        )