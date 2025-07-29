from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime, date
from decimal import Decimal


class BehaviorPattern(BaseModel):
    """Schema for behavior pattern analysis."""
    pattern_type: str  # spending, routine, preference
    description: str
    confidence: float = Field(..., ge=0, le=1)  # 0-1 confidence score
    occurrences: int
    last_observed: datetime
    recommendations: List[str]


class UserBehaviorAnalysis(BaseModel):
    """Schema for comprehensive user behavior analysis."""
    user_id: str
    analysis_date: datetime
    patterns: List[BehaviorPattern]
    spending_habits: Dict[str, Any]
    activity_times: Dict[str, int]  # Hour of day -> activity count
    preferred_categories: List[str]
    suggestion_responsiveness: Dict[str, float]  # Type -> acceptance rate


class DashboardStats(BaseModel):
    """Schema for dashboard statistics."""
    # User activity
    days_active: int
    last_activity: Optional[datetime] = None
    activity_streak: int
    
    # Suggestions
    pending_suggestions: int
    suggestions_this_week: int
    suggestion_acceptance_rate: float
    
    # Transactions
    total_transactions: int
    total_spent_this_month: Decimal
    average_daily_spend: Decimal
    
    # AI insights
    next_important_date: Optional[Dict[str, Any]] = None  # date, type, description
    top_recommendations: List[str]
    savings_opportunities: List[Dict[str, Any]]


class EngagementMetrics(BaseModel):
    """Schema for user engagement metrics."""
    daily_active_rate: float  # Percentage of days active in last 30 days
    average_response_time: float  # Hours to respond to suggestions
    feature_usage: Dict[str, int]  # Feature name -> usage count
    peak_activity_hours: List[int]  # Top 3 hours of activity
    engagement_score: float  # 0-100 overall engagement score


class InsightReport(BaseModel):
    """Schema for AI-generated insight reports."""
    report_id: str
    generated_at: datetime
    period_start: date
    period_end: date
    key_insights: List[str]
    action_items: List[Dict[str, Any]]  # priority, description, deadline
    trends: Dict[str, str]  # metric -> trend (increasing/decreasing/stable)
    predictions: List[Dict[str, Any]]  # event, probability, date