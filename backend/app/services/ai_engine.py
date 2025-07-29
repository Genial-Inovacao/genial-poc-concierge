"""
Basic AI Engine for proactive suggestions.

This module contains the initial implementation of the AI engine
that analyzes user data and generates proactive suggestions.
"""
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func

from ..models import User, Profile, Transaction, Suggestion, SuggestionType, SuggestionStatus

# Priority levels
class Priority:
    LOW = 3
    MEDIUM = 5
    HIGH = 8
    URGENT = 10
from ..database import SessionLocal


class AIEngine:
    """Basic AI Engine for generating proactive suggestions."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def analyze_user(self, user: User) -> List[Dict]:
        """
        Analyze user data and generate suggestions.
        
        Args:
            user: User to analyze
            
        Returns:
            List of suggestion dictionaries
        """
        suggestions = []
        
        # Check for upcoming special dates
        date_suggestions = self._analyze_special_dates(user)
        suggestions.extend(date_suggestions)
        
        # Analyze transaction patterns
        pattern_suggestions = self._analyze_transaction_patterns(user)
        suggestions.extend(pattern_suggestions)
        
        return suggestions
    
    def _analyze_special_dates(self, user: User) -> List[Dict]:
        """Analyze upcoming birthdays and anniversaries."""
        suggestions = []
        today = datetime.now(timezone.utc).date()
        
        if not user.profile:
            return suggestions
        
        # Check spouse birthday
        if user.profile.spouse_birth_date and user.profile.spouse_name:
            days_until = self._days_until_birthday(user.profile.spouse_birth_date)
            
            if 0 < days_until <= 7:  # Within next week
                # Check if already suggested
                existing = self.db.query(Suggestion).filter(
                    and_(
                        Suggestion.user_id == user.id,
                        Suggestion.type == SuggestionType.ANNIVERSARY,
                        Suggestion.status.in_([SuggestionStatus.PENDING, SuggestionStatus.ACCEPTED]),
                        Suggestion.scheduled_date == user.profile.spouse_birth_date.replace(year=today.year)
                    )
                ).first()
                
                if not existing:
                    # Look for restaurant patterns around this date
                    restaurant_suggestion = self._find_anniversary_restaurant_pattern(user, user.profile.spouse_birth_date)
                    
                    suggestions.append({
                        "type": SuggestionType.ANNIVERSARY,
                        "content": f"O aniversário de {user.profile.spouse_name} está chegando ({user.profile.spouse_birth_date.strftime('%d/%m')}). " +
                                  (f"Deseja que eu reserve o {restaurant_suggestion}?" if restaurant_suggestion 
                                   else "Gostaria de fazer uma reserva em algum restaurante especial?"),
                        "priority": Priority.HIGH if days_until <= 3 else Priority.MEDIUM,
                        "scheduled_date": user.profile.spouse_birth_date.replace(year=today.year),
                        "context_data": str({
                            "person": user.profile.spouse_name,
                            "occasion": "birthday",
                            "days_until": days_until,
                            "suggested_restaurant": restaurant_suggestion
                        })
                    })
                    
                    # Flower suggestion based on past behavior
                    if self._has_bought_flowers_for_occasions(user):
                        suggestions.append({
                            "type": SuggestionType.PURCHASE,
                            "content": f"Nos últimos anos você enviou flores para {user.profile.spouse_name}. " +
                                      "Posso providenciar um buquê especial?",
                            # "category": "gift",
                            "priority": Priority.MEDIUM,
                            "scheduled_date": (user.profile.spouse_birth_date.replace(year=today.year) - timedelta(days=1)),
                            "context_data": str( {
                                "person": user.profile.spouse_name,
                                "occasion": "birthday",
                                "item": "flowers"
                            })
                        })
        
        # Check user's own birthday
        if user.profile.birth_date:
            days_until = self._days_until_birthday(user.profile.birth_date)
            
            if days_until == 1:  # Tomorrow
                suggestions.append({
                    "type": SuggestionType.SEASONAL,
                    "content": "Amanhã é seu aniversário! 🎉 Gostaria de algumas sugestões para comemorar?",
                    # "category": "personal",
                    "priority": Priority.LOW,
                    "scheduled_date": user.profile.birth_date.replace(year=today.year),
                    "context_data": str({
                        "occasion": "user_birthday"
                    })
                })
        
        return suggestions
    
    def _analyze_transaction_patterns(self, user: User) -> List[Dict]:
        """Analyze transaction patterns to identify routines."""
        suggestions = []
        today = datetime.now(timezone.utc).date()
        thirty_days_ago = today - timedelta(days=30)
        
        # Find recurring monthly patterns
        monthly_patterns = self.db.query(
            Transaction.category,
            Transaction.description,
            func.count(Transaction.id).label('frequency')
        ).filter(
            and_(
                Transaction.user_id == user.id,
                Transaction.date >= datetime.now(timezone.utc) - timedelta(days=180)  # Last 6 months
            )
        ).group_by(
            Transaction.category,
            Transaction.description
        ).having(
            func.count(Transaction.id) >= 3  # At least 3 times
        ).all()
        
        for category, description, frequency in monthly_patterns:
            # Check if it's time for this recurring transaction
            last_transaction = self.db.query(Transaction).filter(
                and_(
                    Transaction.user_id == user.id,
                    Transaction.category == category,
                    Transaction.description == description
                )
            ).order_by(Transaction.date.desc()).first()
            
            if last_transaction:
                days_since = (today - last_transaction.date.date()).days
                avg_interval = 180 / frequency  # Average days between transactions
                
                if days_since >= (avg_interval - 3):  # Within 3 days of expected
                    # Check if already suggested recently
                    recent_suggestion = self.db.query(Suggestion).filter(
                        and_(
                            Suggestion.user_id == user.id,
                            Suggestion.type == SuggestionType.ROUTINE,
                            Suggestion.created_at >= datetime.now(timezone.utc) - timedelta(days=7),
                            Suggestion.metadata_json.contains({"description": description})
                        )
                    ).first()
                    
                    if not recent_suggestion:
                        suggestions.append({
                            "type": SuggestionType.ROUTINE,
                            "content": f"Está na hora de {self._humanize_transaction(category, description)}? " +
                                      f"Você costuma fazer isso a cada {int(avg_interval)} dias.",
                            # "category": category,
                            "priority": Priority.LOW,
                            "scheduled_date": today,
                            "context_data": str( {
                                "pattern": "recurring",
                                # "category": category,
                                "description": description,
                                "frequency": frequency,
                                "average_interval_days": avg_interval,
                                "days_since_last": days_since
                            })
                        })
        
        return suggestions
    
    def _days_until_birthday(self, birth_date) -> int:
        """Calculate days until next birthday."""
        today = datetime.now(timezone.utc).date()
        this_year_birthday = birth_date.replace(year=today.year)
        
        if this_year_birthday < today:
            # Birthday passed this year, check next year
            next_birthday = birth_date.replace(year=today.year + 1)
        else:
            next_birthday = this_year_birthday
        
        return (next_birthday - today).days
    
    def _find_anniversary_restaurant_pattern(self, user: User, special_date) -> Optional[str]:
        """Find restaurants visited around special dates in the past."""
        # Look for restaurant transactions within 3 days of the special date in previous years
        restaurants = self.db.query(
            Transaction.description,
            func.count(Transaction.id).label('visits')
        ).filter(
            and_(
                Transaction.user_id == user.id,
                Transaction.category == 'restaurant',
                or_(
                    *[
                        and_(
                            Transaction.date >= datetime(year, special_date.month, special_date.day) - timedelta(days=3),
                            Transaction.date <= datetime(year, special_date.month, special_date.day) + timedelta(days=3)
                        )
                        for year in range(datetime.now().year - 3, datetime.now().year)
                    ]
                )
            )
        ).group_by(Transaction.description).order_by(func.count(Transaction.id).desc()).first()
        
        return restaurants[0] if restaurants and restaurants[1] >= 2 else None
    
    def _has_bought_flowers_for_occasions(self, user: User) -> bool:
        """Check if user has history of buying flowers for special occasions."""
        flower_purchases = self.db.query(Transaction).filter(
            and_(
                Transaction.user_id == user.id,
                or_(
                    Transaction.category == 'flowers',
                    Transaction.description.ilike('%flor%'),
                    Transaction.description.ilike('%flower%')
                )
            )
        ).count()
        
        return flower_purchases >= 2
    
    def _humanize_transaction(self, category: str, description: str) -> str:
        """Convert transaction data to human-readable text."""
        humanized = {
            "restaurant": f"jantar no {description}",
            "grocery": f"fazer compras no {description}",
            "gas": f"abastecer no {description}",
            "subscription": f"renovar sua assinatura {description}",
            "gym": "renovar a mensalidade da academia",
        }
        
        return humanized.get(category, f"{category} - {description}")


def run_ai_analysis_for_all_users():
    """Run AI analysis for all active users."""
    db = SessionLocal()
    
    try:
        # Get all active users
        users = db.query(User).filter(User.is_active == True).all()
        
        engine = AIEngine(db)
        
        for user in users:
            print(f"\nAnalyzing user: {user.username}")
            
            # Generate suggestions
            suggestions = engine.analyze_user(user)
            
            # Save suggestions to database
            for suggestion_data in suggestions:
                suggestion = Suggestion(
                    user_id=user.id,
                    **suggestion_data
                )
                db.add(suggestion)
                print(f"  - Generated: {suggestion_data['content'][:60]}...")
            
        db.commit()
        print(f"\nAnalysis complete. Processed {len(users)} users.")
        
    except Exception as e:
        print(f"Error during AI analysis: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    run_ai_analysis_for_all_users()