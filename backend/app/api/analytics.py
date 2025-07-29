from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, extract
from typing import Optional
from datetime import datetime, timezone, timedelta
from uuid import UUID

from ..database import get_db
from ..models import User, Transaction, Suggestion, Interaction, SuggestionStatus, InteractionAction
from ..schemas import (
    UserBehaviorAnalysis,
    DashboardStats,
    EngagementMetrics,
    BehaviorPattern
)
from ..services.auth import get_current_active_user

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get dashboard statistics for the current user.
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Dashboard statistics
    """
    now = datetime.now(timezone.utc)
    
    # Calculate days active
    created_at = current_user.created_at
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)
    days_active = (now - created_at).days + 1
    
    # Get last activity
    last_interaction = db.query(Interaction).filter(
        Interaction.user_id == current_user.id
    ).order_by(Interaction.timestamp.desc()).first()
    
    last_activity = last_interaction.timestamp if last_interaction else created_at
    
    # Calculate activity streak (simplified - days with at least one interaction)
    seven_days_ago = now - timedelta(days=7)
    daily_activities = db.query(
        func.date(Interaction.timestamp).label('day')
    ).filter(
        and_(
            Interaction.user_id == current_user.id,
            Interaction.timestamp >= seven_days_ago
        )
    ).group_by(func.date(Interaction.timestamp)).count()
    
    activity_streak = daily_activities  # Simplified streak calculation
    
    # Pending suggestions
    pending_suggestions = db.query(Suggestion).filter(
        Suggestion.user_id == current_user.id,
        Suggestion.status == SuggestionStatus.PENDING
    ).count()
    
    # Suggestions this week
    week_start = now - timedelta(days=now.weekday())
    suggestions_this_week = db.query(Suggestion).filter(
        and_(
            Suggestion.user_id == current_user.id,
            Suggestion.created_at >= week_start
        )
    ).count()
    
    # Suggestion acceptance rate
    total_suggestions = db.query(Suggestion).filter(
        Suggestion.user_id == current_user.id
    ).count()
    
    accepted_or_executed = db.query(Suggestion).filter(
        Suggestion.user_id == current_user.id,
        Suggestion.status.in_([SuggestionStatus.ACCEPTED, SuggestionStatus.EXECUTED])
    ).count()
    
    suggestion_acceptance_rate = accepted_or_executed / total_suggestions if total_suggestions > 0 else 0.0
    
    # Transaction stats for current month
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    month_transactions = db.query(
        func.count(Transaction.id).label('count'),
        func.sum(Transaction.amount).label('total')
    ).filter(
        and_(
            Transaction.user_id == current_user.id,
            Transaction.date >= month_start
        )
    ).first()
    
    total_transactions = month_transactions.count or 0
    total_spent_this_month = month_transactions.total or 0
    
    # Average daily spend (last 30 days)
    thirty_days_ago = now - timedelta(days=30)
    daily_avg = db.query(
        func.avg(Transaction.amount).label('avg')
    ).filter(
        and_(
            Transaction.user_id == current_user.id,
            Transaction.date >= thirty_days_ago
        )
    ).scalar() or 0
    
    # Next important date
    profile = current_user.profile
    next_important_date = None
    
    if profile:
        # Check for upcoming birthdays
        today = now.date()
        dates_to_check = []
        
        if profile.birth_date:
            next_birthday = profile.birth_date.replace(year=today.year)
            if next_birthday < today:
                next_birthday = next_birthday.replace(year=today.year + 1)
            dates_to_check.append({
                "date": next_birthday,
                "type": "birthday",
                "description": "Your birthday"
            })
        
        if profile.spouse_birth_date:
            next_spouse_birthday = profile.spouse_birth_date.replace(year=today.year)
            if next_spouse_birthday < today:
                next_spouse_birthday = next_spouse_birthday.replace(year=today.year + 1)
            dates_to_check.append({
                "date": next_spouse_birthday,
                "type": "anniversary",
                "description": f"{profile.spouse_name}'s birthday" if profile.spouse_name else "Spouse's birthday"
            })
        
        # Find the nearest date
        if dates_to_check:
            dates_to_check.sort(key=lambda x: x["date"])
            next_important_date = dates_to_check[0]
    
    # Top recommendations (simplified for now)
    top_recommendations = []
    if pending_suggestions > 0:
        top_suggestions = db.query(Suggestion).filter(
            Suggestion.user_id == current_user.id,
            Suggestion.status == SuggestionStatus.PENDING
        ).order_by(
            Suggestion.priority.desc(),
            Suggestion.scheduled_date.asc()
        ).limit(3).all()
        
        top_recommendations = [s.content for s in top_suggestions]
    
    # Savings opportunities (simplified)
    savings_opportunities = []
    
    # Check for high spending categories
    if total_spent_this_month > 0:
        category_spending = db.query(
            Transaction.category,
            func.sum(Transaction.amount).label('total')
        ).filter(
            and_(
                Transaction.user_id == current_user.id,
                Transaction.date >= month_start
            )
        ).group_by(Transaction.category).order_by(
            func.sum(Transaction.amount).desc()
        ).limit(3).all()
        
        for category, total in category_spending:
            # Simple rule: if spending > 20% of total, suggest reduction
            percentage = (total / total_spent_this_month) * 100
            if percentage > 20:
                savings_opportunities.append({
                    "category": category,
                    "current_spending": float(total),
                    "percentage": percentage,
                    "suggestion": f"Consider reducing {category} spending by 10%"
                })
    
    return DashboardStats(
        days_active=days_active,
        last_activity=last_activity,
        activity_streak=activity_streak,
        pending_suggestions=pending_suggestions,
        suggestions_this_week=suggestions_this_week,
        suggestion_acceptance_rate=suggestion_acceptance_rate,
        total_transactions=total_transactions,
        total_spent_this_month=total_spent_this_month,
        average_daily_spend=daily_avg,
        next_important_date=next_important_date,
        top_recommendations=top_recommendations,
        savings_opportunities=savings_opportunities
    )


@router.get("/behavior-patterns", response_model=UserBehaviorAnalysis)
async def get_behavior_patterns(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get user behavior analysis and patterns.
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        User behavior analysis
    """
    now = datetime.now(timezone.utc)
    
    # Analyze spending patterns
    patterns = []
    
    # Pattern 1: Recurring purchases
    thirty_days_ago = now - timedelta(days=30)
    
    # Find categories with multiple purchases
    recurring_categories = db.query(
        Transaction.category,
        func.count(Transaction.id).label('count'),
        func.avg(Transaction.amount).label('avg_amount')
    ).filter(
        and_(
            Transaction.user_id == current_user.id,
            Transaction.date >= thirty_days_ago
        )
    ).group_by(Transaction.category).having(
        func.count(Transaction.id) >= 3  # At least 3 times in 30 days
    ).all()
    
    for category, count, avg_amount in recurring_categories:
        frequency = count / 30  # Purchases per day
        if frequency >= 0.1:  # At least once every 10 days
            patterns.append(BehaviorPattern(
                pattern_type="spending",
                description=f"Regular {category} purchases",
                confidence=min(0.9, frequency),
                occurrences=count,
                last_observed=now,
                recommendations=[
                    f"Set up automatic reminders for {category} purchases",
                    f"Consider bulk buying to save on {category}"
                ]
            ))
    
    # Pattern 2: Peak spending times
    activity_by_hour = db.query(
        extract('hour', Transaction.date).label('hour'),
        func.count(Transaction.id).label('count')
    ).filter(
        Transaction.user_id == current_user.id
    ).group_by(
        extract('hour', Transaction.date)
    ).all()
    
    activity_times = {int(hour): count for hour, count in activity_by_hour if hour is not None}
    
    # Find peak hours
    if activity_times:
        peak_hour = max(activity_times, key=activity_times.get)
        patterns.append(BehaviorPattern(
            pattern_type="routine",
            description=f"Most active at {peak_hour}:00",
            confidence=0.8,
            occurrences=activity_times[peak_hour],
            last_observed=now,
            recommendations=[
                f"Schedule important reminders around {peak_hour}:00",
                "Adjust notification preferences for optimal timing"
            ]
        ))
    
    # Spending habits summary
    spending_by_category = db.query(
        Transaction.category,
        func.sum(Transaction.amount).label('total')
    ).filter(
        and_(
            Transaction.user_id == current_user.id,
            Transaction.date >= thirty_days_ago
        )
    ).group_by(Transaction.category).all()
    
    spending_habits = {cat: float(total) for cat, total in spending_by_category}
    
    # Preferred categories (top 3)
    preferred_categories = sorted(spending_habits.keys(), key=lambda x: spending_habits[x], reverse=True)[:3]
    
    # Suggestion responsiveness
    suggestion_types = db.query(Suggestion.type).filter(
        Suggestion.user_id == current_user.id
    ).distinct().all()
    
    suggestion_responsiveness = {}
    for (stype,) in suggestion_types:
        total = db.query(Suggestion).filter(
            Suggestion.user_id == current_user.id,
            Suggestion.type == stype
        ).count()
        
        accepted = db.query(Suggestion).filter(
            Suggestion.user_id == current_user.id,
            Suggestion.type == stype,
            Suggestion.status.in_([SuggestionStatus.ACCEPTED, SuggestionStatus.EXECUTED])
        ).count()
        
        if total > 0:
            suggestion_responsiveness[str(stype)] = accepted / total
    
    return UserBehaviorAnalysis(
        user_id=str(current_user.id),
        analysis_date=now,
        patterns=patterns,
        spending_habits=spending_habits,
        activity_times=activity_times,
        preferred_categories=preferred_categories,
        suggestion_responsiveness=suggestion_responsiveness
    )


@router.get("/engagement", response_model=EngagementMetrics)
async def get_engagement_metrics(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get user engagement metrics.
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Engagement metrics
    """
    now = datetime.now(timezone.utc)
    thirty_days_ago = now - timedelta(days=30)
    
    # Daily active rate (days with activity in last 30 days)
    active_days = db.query(
        func.date(Interaction.timestamp).label('day')
    ).filter(
        and_(
            Interaction.user_id == current_user.id,
            Interaction.timestamp >= thirty_days_ago
        )
    ).group_by(func.date(Interaction.timestamp)).count()
    
    daily_active_rate = active_days / 30.0
    
    # Average response time to suggestions
    response_times = db.query(
        Suggestion.created_at,
        Interaction.timestamp
    ).join(
        Interaction,
        and_(
            Interaction.suggestion_id == Suggestion.id,
            Interaction.action.in_([InteractionAction.ACCEPTED, InteractionAction.REJECTED])
        )
    ).filter(
        Suggestion.user_id == current_user.id
    ).all()
    
    if response_times:
        total_hours = sum(
            (interaction_time - suggestion_time).total_seconds() / 3600
            for suggestion_time, interaction_time in response_times
        )
        average_response_time = total_hours / len(response_times)
    else:
        average_response_time = 0.0
    
    # Feature usage
    feature_usage = {
        "suggestions": db.query(Interaction).filter(
            Interaction.user_id == current_user.id,
            Interaction.suggestion_id.isnot(None)
        ).count(),
        "transactions": db.query(Transaction).filter(
            Transaction.user_id == current_user.id
        ).count(),
        "profile_updates": 1  # Simplified
    }
    
    # Peak activity hours
    hourly_activity = db.query(
        extract('hour', Interaction.timestamp).label('hour'),
        func.count(Interaction.id).label('count')
    ).filter(
        Interaction.user_id == current_user.id
    ).group_by(
        extract('hour', Interaction.timestamp)
    ).order_by(
        func.count(Interaction.id).desc()
    ).limit(3).all()
    
    peak_activity_hours = [int(hour) for hour, _ in hourly_activity if hour is not None]
    
    # Calculate engagement score (0-100)
    engagement_score = min(100, (
        daily_active_rate * 30 +  # Max 30 points for daily activity
        min(30, feature_usage.get("suggestions", 0) / 10 * 30) +  # Max 30 points for suggestions
        min(20, feature_usage.get("transactions", 0) / 10 * 20) +  # Max 20 points for transactions
        (20 if average_response_time < 24 else 10 if average_response_time < 48 else 0)  # Response time bonus
    ))
    
    return EngagementMetrics(
        daily_active_rate=daily_active_rate,
        average_response_time=average_response_time,
        feature_usage=feature_usage,
        peak_activity_hours=peak_activity_hours,
        engagement_score=engagement_score
    )