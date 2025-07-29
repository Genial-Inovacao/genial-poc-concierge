"""
Script to run AI analysis for all users and generate new suggestions.
This can be run manually or scheduled via cron/task scheduler.
"""
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User, Suggestion
from app.services.ai_engine import AIEngine
from app.config import settings


def run_analysis_for_all_users():
    """Run AI analysis for all active users."""
    print(f"🤖 Starting AI Analysis - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"LLM Enabled: {settings.use_llm_for_suggestions}")
    print(f"LLM Model: {settings.llm_model}")
    print("-" * 50)
    
    db = SessionLocal()
    
    try:
        # Get all active users
        users = db.query(User).filter(User.is_active == True).all()
        print(f"Found {len(users)} active users")
        
        total_suggestions = 0
        
        for user in users:
            print(f"\n📊 Analyzing user: {user.username}")
            
            # Initialize AI Engine
            engine = AIEngine(db)
            
            # Generate suggestions
            new_suggestions = engine.analyze_user(user)
            
            # Save suggestions to database
            user_suggestions = 0
            for suggestion_data in new_suggestions:
                # Check if similar suggestion already exists
                existing = db.query(Suggestion).filter(
                    Suggestion.user_id == user.id,
                    Suggestion.content == suggestion_data['content'],
                    Suggestion.status.in_(['pending', 'accepted'])
                ).first()
                
                if not existing:
                    suggestion = Suggestion(
                        user_id=user.id,
                        **suggestion_data
                    )
                    db.add(suggestion)
                    user_suggestions += 1
                    print(f"  ✅ {suggestion_data['type']}: {suggestion_data['content'][:60]}...")
            
            db.commit()
            total_suggestions += user_suggestions
            print(f"  Generated {user_suggestions} new suggestions for {user.username}")
        
        print(f"\n✅ Analysis complete!")
        print(f"Total new suggestions created: {total_suggestions}")
        
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def run_analysis_for_user(username: str):
    """Run AI analysis for a specific user."""
    print(f"🤖 Running AI Analysis for user: {username}")
    
    db = SessionLocal()
    
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            print(f"❌ User '{username}' not found!")
            return
        
        engine = AIEngine(db)
        new_suggestions = engine.analyze_user(user)
        
        saved_count = 0
        for suggestion_data in new_suggestions:
            # Check for duplicates
            existing = db.query(Suggestion).filter(
                Suggestion.user_id == user.id,
                Suggestion.content == suggestion_data['content'],
                Suggestion.status.in_(['pending', 'accepted'])
            ).first()
            
            if not existing:
                suggestion = Suggestion(
                    user_id=user.id,
                    **suggestion_data
                )
                db.add(suggestion)
                saved_count += 1
                print(f"✅ Created: {suggestion_data['content'][:80]}...")
        
        db.commit()
        print(f"\n✅ Created {saved_count} new suggestions for {username}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Run for specific user
        username = sys.argv[1]
        run_analysis_for_user(username)
    else:
        # Run for all users
        run_analysis_for_all_users()