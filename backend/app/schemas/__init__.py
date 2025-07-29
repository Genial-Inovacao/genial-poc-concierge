# Export all schemas for easy access
from .auth import (
    UserCreate,
    UserLogin,
    TokenResponse,
    TokenRefresh,
    UserResponse,
    PasswordChange,
    PasswordReset,
    PasswordResetConfirm
)

from .user import (
    ProfileBase,
    ProfileCreate,
    ProfileUpdate,
    ProfileResponse,
    PreferencesUpdate,
    UserWithProfile,
    UserStats
)

from .transaction import (
    TransactionBase,
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
    TransactionFilter,
    TransactionAnalytics
)

from .suggestion import (
    SuggestionBase,
    SuggestionCreate,
    SuggestionUpdate,
    SuggestionResponse,
    SuggestionInteraction,
    SuggestionFilter,
    SuggestionStats
)

from .analytics import (
    BehaviorPattern,
    UserBehaviorAnalysis,
    DashboardStats,
    EngagementMetrics,
    InsightReport
)

from .interaction import (
    InteractionBase,
    InteractionCreate,
    InteractionResponse,
    InteractionStats,
    InteractionFilter
)

__all__ = [
    # Auth schemas
    "UserCreate",
    "UserLogin",
    "TokenResponse",
    "TokenRefresh",
    "UserResponse",
    "PasswordChange",
    "PasswordReset",
    "PasswordResetConfirm",
    
    # User schemas
    "ProfileBase",
    "ProfileCreate",
    "ProfileUpdate",
    "ProfileResponse",
    "PreferencesUpdate",
    "UserWithProfile",
    "UserStats",
    
    # Transaction schemas
    "TransactionBase",
    "TransactionCreate",
    "TransactionUpdate",
    "TransactionResponse",
    "TransactionFilter",
    "TransactionAnalytics",
    
    # Suggestion schemas
    "SuggestionBase",
    "SuggestionCreate",
    "SuggestionUpdate",
    "SuggestionResponse",
    "SuggestionInteraction",
    "SuggestionFilter",
    "SuggestionStats",
    
    # Analytics schemas
    "BehaviorPattern",
    "UserBehaviorAnalysis",
    "DashboardStats",
    "EngagementMetrics",
    "InsightReport",
    
    # Interaction schemas
    "InteractionBase",
    "InteractionCreate",
    "InteractionResponse",
    "InteractionStats",
    "InteractionFilter"
]