"""
Seed database with realistic test data for AI Concierge system.
"""
import sys
sys.path.append('.')

from datetime import datetime, timedelta, timezone, date
from decimal import Decimal
import random
import uuid
import json

from app.database import SessionLocal, engine, Base
from app.models import User, Profile, Transaction, Suggestion, Interaction
from app.models.suggestion import SuggestionType, SuggestionStatus
from app.models.interaction import InteractionAction
from app.utils.security import get_password_hash

# Priority levels
class Priority:
    LOW = 3
    MEDIUM = 5
    HIGH = 8
    URGENT = 10


# Create all tables
Base.metadata.create_all(bind=engine)

def create_test_users():
    """Create test users with complete profiles."""
    db = SessionLocal()
    
    users_data = [
        {
            "username": "carlos_silva",
            "email": "carlos.silva@email.com",
            "password": "senha123",
            "profile": {
                "name": "Carlos Eduardo Silva",
                "phone": "11987654321",
                "birth_date": date(1985, 3, 15),
                "spouse_name": "Maria Silva",
                "spouse_birth_date": date(1987, 8, 10),
                "preferences": {
                    "notifications": {"email": True, "push": True, "sms": False},
                    "categories_of_interest": ["restaurant", "gift", "travel"],
                    "preferred_times": {"morning": False, "afternoon": True, "evening": True, "night": False}
                }
            }
        },
        {
            "username": "ana_costa",
            "email": "ana.costa@email.com",
            "password": "senha123",
            "profile": {
                "name": "Ana Paula Costa",
                "phone": "21976543210",
                "birth_date": date(1990, 12, 5),
                "spouse_name": "Roberto Costa",
                "spouse_birth_date": date(1988, 7, 22),
                "preferences": {
                    "notifications": {"email": True, "push": False, "sms": True},
                    "categories_of_interest": ["health", "finance", "shopping"],
                    "preferred_times": {"morning": True, "afternoon": False, "evening": True, "night": False}
                }
            }
        },
        {
            "username": "pedro_santos",
            "email": "pedro.santos@email.com",
            "password": "senha123",
            "profile": {
                "name": "Pedro Henrique Santos",
                "phone": "31965432109",
                "birth_date": date(1982, 6, 30),
                "spouse_name": "Juliana Santos",
                "spouse_birth_date": date(1984, 2, 14),  # Valentine's Day!
                "preferences": {
                    "notifications": {"email": True, "push": True, "sms": True},
                    "categories_of_interest": ["restaurant", "entertainment", "travel"],
                    "preferred_times": {"morning": True, "afternoon": True, "evening": False, "night": False}
                }
            }
        }
    ]
    
    created_users = []
    
    for user_data in users_data:
        # Check if user already exists
        existing = db.query(User).filter(User.username == user_data["username"]).first()
        if existing:
            print(f"User {user_data['username']} already exists")
            created_users.append(existing)
            continue
        
        # Create user
        user = User(
            username=user_data["username"],
            email=user_data["email"],
            password_hash=get_password_hash(user_data["password"]),
            is_active=True
        )
        db.add(user)
        db.flush()
        
        # Create profile
        profile_data = user_data["profile"]
        profile = Profile(
            user_id=user.id,
            name=profile_data["name"],
            phone=profile_data["phone"],
            birth_date=profile_data["birth_date"],
            spouse_name=profile_data["spouse_name"],
            spouse_birth_date=profile_data["spouse_birth_date"],
            preferences_json={
                **profile_data["preferences"],
                "suggestion_categories": {
                    "anniversary": True,
                    "purchase": True,
                    "routine": True,
                    "seasonal": True
                },
                "quiet_hours": {"enabled": False, "start": "22:00", "end": "08:00"},
                "suggestion_frequency": "normal",
                "max_daily_suggestions": 5
            }
        )
        db.add(profile)
        created_users.append(user)
        print(f"Created user: {user.username}")
    
    db.commit()
    return created_users


def create_transaction_history(usernames):
    """Create realistic transaction history for users."""
    db = SessionLocal()
    
    # Base date - start 6 months ago
    base_date = datetime.now(timezone.utc) - timedelta(days=180)
    
    for username in usernames:
        user = db.query(User).filter(User.username == username).first()
        if not user or not user.profile:
            continue
            
        print(f"\nCreating transactions for {user.username}...")
        
        # Monthly recurring transactions
        for month in range(6):
            month_date = base_date + timedelta(days=month*30)
            
            # 1. Monthly gym subscription
            db.add(Transaction(
                user_id=user.id,
                type="subscription",
                amount=Decimal("89.90"),
                category="fitness",
                description="SmartFit Academia",
                date=month_date.replace(day=5)  # Always on 5th
            ))
            
            # 2. Weekly grocery shopping (4 per month)
            for week in range(4):
                grocery_date = month_date + timedelta(days=week*7)
                if grocery_date.weekday() == 6:  # Sunday
                    amount = Decimal(random.uniform(150, 350))
                    db.add(Transaction(
                        user_id=user.id,
                        type="purchase",
                        amount=amount,
                        category="grocery",
                        description="Supermercado Pão de Açúcar",
                        date=grocery_date
                    ))
            
            # 3. Monthly restaurant (first Friday)
            first_friday = month_date.replace(day=1)
            while first_friday.weekday() != 4:  # Find first Friday
                first_friday += timedelta(days=1)
            
            db.add(Transaction(
                user_id=user.id,
                type="purchase",
                amount=Decimal(random.uniform(180, 280)),
                category="restaurant",
                description="Outback Steakhouse",
                date=first_friday
            ))
        
        # Special date transactions (anniversaries)
        if user.profile.spouse_birth_date:
            # Find spouse birthdays in the last 3 years
            for year_offset in range(3):
                birthday = user.profile.spouse_birth_date.replace(
                    year=datetime.now().year - year_offset
                )
                if birthday < datetime.now(timezone.utc).date():
                    # Restaurant on birthday
                    db.add(Transaction(
                        user_id=user.id,
                        type="purchase",
                        amount=Decimal("350.00"),
                        category="restaurant",
                        description="Fasano Restaurant",
                        date=datetime.combine(birthday, datetime.min.time()).replace(tzinfo=timezone.utc)
                    ))
                    
                    # Flowers day before
                    db.add(Transaction(
                        user_id=user.id,
                        type="purchase",
                        amount=Decimal("150.00"),
                        category="gift",
                        description="Giuliana Flores - Buquê Rosas Vermelhas",
                        date=datetime.combine(birthday - timedelta(days=1), datetime.min.time()).replace(tzinfo=timezone.utc),
                            ))
                    
                    # Gift purchase
                    db.add(Transaction(
                        user_id=user.id,
                        type="purchase",
                        amount=Decimal(random.uniform(300, 800)),
                        category="shopping",
                        description="Shopping Iguatemi - Presente",
                        date=datetime.combine(birthday - timedelta(days=3), datetime.min.time()).replace(tzinfo=timezone.utc),
                            ))
        
        # Random transactions
        for _ in range(30):
            random_date = base_date + timedelta(days=random.randint(0, 180))
            category = random.choice(["restaurant", "shopping", "entertainment", "transport", "health"])
            
            descriptions = {
                "restaurant": ["McDonald's", "Subway", "Starbucks", "Pizza Hut", "Sushi Yamato"],
                "shopping": ["Amazon.com.br", "Mercado Livre", "Zara", "C&A", "Renner"],
                "entertainment": ["Netflix", "Spotify", "Cinema Kinoplex", "Teatro Municipal"],
                "transport": ["Uber", "99 Taxi", "Shell Posto", "Ipiranga Posto"],
                "health": ["Drogaria São Paulo", "Droga Raia", "Consulta Dr. Silva"]
            }
            
            db.add(Transaction(
                user_id=user.id,
                type="purchase",
                amount=Decimal(random.uniform(20, 200)),
                category=category,
                description=random.choice(descriptions[category]),
                date=random_date,
            ))
    
    db.commit()
    print("Transaction history created!")


def create_ai_suggestions(usernames):
    """Create AI-generated suggestions based on patterns."""
    db = SessionLocal()
    today = datetime.now(timezone.utc)
    
    for username in usernames:
        user = db.query(User).filter(User.username == username).first()
        if not user or not user.profile:
            continue
            
        print(f"\nCreating AI suggestions for {user.username}...")
        
        # 1. Upcoming spouse birthday suggestion
        if user.profile.spouse_birth_date:
            days_until = (user.profile.spouse_birth_date.replace(year=today.year) - today.date()).days
            
            if 0 < days_until <= 7:
                # Restaurant reservation suggestion
                db.add(Suggestion(
                    user_id=user.id,
                    type=SuggestionType.ANNIVERSARY,
                    content=f"O aniversário de {user.profile.spouse_name} está chegando ({user.profile.spouse_birth_date.strftime('%d/%m')}). "
                           f"Deseja que eu reserve o Fasano Restaurant como nos anos anteriores?",
                    priority=Priority.HIGH,
                    status=SuggestionStatus.PENDING,
                    scheduled_date=datetime.combine(user.profile.spouse_birth_date.replace(year=today.year), datetime.min.time()).replace(tzinfo=timezone.utc),
                    context_data=json.dumps({
                        "person": user.profile.spouse_name,
                        "occasion": "birthday",
                        "restaurant": "Fasano Restaurant",
                        "average_spend": 350.00
                    })
                ))
                
                # Flower suggestion
                db.add(Suggestion(
                    user_id=user.id,
                    type=SuggestionType.PURCHASE,
                    content=f"Posso providenciar o envio de flores para {user.profile.spouse_name}? "
                           "Nos últimos anos você enviou rosas vermelhas.",
                    priority=Priority.MEDIUM,
                    status=SuggestionStatus.PENDING,
                    scheduled_date=datetime.combine(user.profile.spouse_birth_date.replace(year=today.year) - timedelta(days=1), datetime.min.time()).replace(tzinfo=timezone.utc),
                    context_data=json.dumps({
                        "person": user.profile.spouse_name,
                        "item": "flowers",
                        "type": "Rosas Vermelhas",
                        "vendor": "Giuliana Flores"
                    })
                ))
        
        # 2. Monthly routine suggestions
        # Gym renewal
        db.add(Suggestion(
            user_id=user.id,
            type=SuggestionType.ROUTINE,
            content="Sua mensalidade da SmartFit vence em 2 dias. A renovação automática está ativa.",
            priority=Priority.LOW,
            status=SuggestionStatus.PENDING,
            scheduled_date=today + timedelta(days=2),
            context_data=json.dumps({
                "service": "SmartFit Academia",
                "amount": 89.90,
                "frequency": "monthly"
            })
        ))
        
        # First Friday restaurant
        first_friday = today.replace(day=1)
        while first_friday.weekday() != 4:
            first_friday += timedelta(days=1)
        
        if (first_friday.date() - today.date()).days in range(1, 4):
            db.add(Suggestion(
                user_id=user.id,
                type=SuggestionType.ROUTINE,
                content="Sexta-feira é o primeiro final de semana do mês. "
                       "Reservo sua mesa no Outback Steakhouse como de costume?",
                priority=Priority.MEDIUM,
                status=SuggestionStatus.PENDING,
                scheduled_date=first_friday,
                context_data=json.dumps({
                    "restaurant": "Outback Steakhouse",
                    "pattern": "first_friday",
                    "average_spend": 230.00
                })
            ))
        
        # 3. Seasonal suggestion
        if today.month == 12:
            db.add(Suggestion(
                user_id=user.id,
                type=SuggestionType.SEASONAL,
                content="Dezembro chegou! Gostaria de sugestões para presentes de Natal "
                       "baseadas no seu histórico de compras?",
                priority=Priority.LOW,
                status=SuggestionStatus.PENDING,
                scheduled_date=today,
                context_data=json.dumps({
                    "season": "christmas",
                    "year": today.year
                })
            ))
    
    db.commit()
    print("AI suggestions created!")


def create_interactions(usernames):
    """Create user interactions with suggestions."""
    db = SessionLocal()
    
    for username in usernames:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            continue
        print(f"\nCreating interactions for {user.username}...")
        
        # Get user's suggestions
        suggestions = db.query(Suggestion).filter(
            Suggestion.user_id == user.id
        ).limit(5).all()
        
        for i, suggestion in enumerate(suggestions):
            # Simulate different user behaviors
            if i == 0:  # Accept first suggestion
                interaction = Interaction(
                    user_id=user.id,
                    suggestion_id=suggestion.id,
                    action=InteractionAction.ACCEPTED,
                    feedback="Perfeito! Pode fazer a reserva.",
                    timestamp=datetime.now(timezone.utc) - timedelta(hours=2)
                )
                suggestion.status = SuggestionStatus.ACCEPTED
                
            elif i == 1:  # View second
                interaction = Interaction(
                    user_id=user.id,
                    suggestion_id=suggestion.id,
                    action=InteractionAction.VIEWED,
                    timestamp=datetime.now(timezone.utc) - timedelta(hours=1)
                )
                
            elif i == 2:  # Snooze third
                interaction = Interaction(
                    user_id=user.id,
                    suggestion_id=suggestion.id,
                    action=InteractionAction.SNOOZED,
                    feedback="Lembre-me amanhã",
                    timestamp=datetime.now(timezone.utc) - timedelta(minutes=30)
                )
                suggestion.status = SuggestionStatus.SNOOZED
                
            else:  # Leave others pending
                continue
            
            db.add(interaction)
    
    db.commit()
    print("Interactions created!")


def main():
    """Run all seed functions."""
    print("Starting database seed...")
    
    # Create test users
    users = create_test_users()
    
    # Work with usernames to avoid session issues
    usernames = ["carlos_silva", "ana_costa", "pedro_santos"]
    
    for username in usernames:
        db = SessionLocal()
        user = db.query(User).filter(User.username == username).first()
        
        if user:
            # Check if user already has transactions
            existing_transactions = db.query(Transaction).filter(
                Transaction.user_id == user.id
            ).count()
            
            if existing_transactions == 0:
                print(f"\nCreating data for user: {username}")
                db.close()
                
                # Create data with fresh sessions
                create_transaction_history([username])
                create_ai_suggestions([username])
                create_interactions([username])
            else:
                print(f"User {username} already has data, skipping...")
                db.close()
        else:
            print(f"User {username} not found!")
            db.close()
    
    print("\n✅ Database seeded successfully!")
    print("\nTest users created:")
    print("- carlos_silva / senha123")
    print("- ana_costa / senha123")
    print("- pedro_santos / senha123")
    print("\nYou can now login with any of these users to see the AI suggestions!")


if __name__ == "__main__":
    main()