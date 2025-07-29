"""Debug script to check stats calculation"""
from datetime import datetime, timezone
from app.database import SessionLocal
from app.models import User, Suggestion, Interaction, InteractionAction

db = SessionLocal()

# Get user
user = db.query(User).filter(User.username == "allanbruno").first()
if user:
    print(f"User: {user.username}")
    print(f"Created at: {user.created_at}")
    print(f"Created at tzinfo: {user.created_at.tzinfo}")
    
    # Calculate days active
    now = datetime.now(timezone.utc)
    print(f"\nNow: {now}")
    print(f"Now tzinfo: {now.tzinfo}")
    
    # Make created_at timezone aware if needed
    if user.created_at.tzinfo is None:
        created_at = user.created_at.replace(tzinfo=timezone.utc)
    else:
        created_at = user.created_at
    
    days_active = (now - created_at).days + 1
    print(f"\nDays active: {days_active}")
    
    # Count actions
    total_actions = db.query(Interaction).filter(
        Interaction.user_id == user.id,
        Interaction.action != InteractionAction.VIEWED
    ).count()
    print(f"Total actions (non-viewed): {total_actions}")
    
    # Count suggestions
    total_suggestions = db.query(Suggestion).filter(
        Suggestion.user_id == user.id
    ).count()
    accepted_suggestions = db.query(Suggestion).filter(
        Suggestion.user_id == user.id,
        Suggestion.status == 'accepted'
    ).count()
    
    print(f"\nTotal suggestions: {total_suggestions}")
    print(f"Accepted suggestions: {accepted_suggestions}")
    
    acceptance_rate = (accepted_suggestions / total_suggestions * 100) if total_suggestions > 0 else 0
    print(f"Acceptance rate: {acceptance_rate:.1f}%")

db.close()