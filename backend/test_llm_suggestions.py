"""
Test script to demonstrate LLM suggestion generation.
Run this after configuring your ANTHROPIC_API_KEY in .env
"""
import asyncio
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User, Transaction
from app.services.ai_engine import AIEngine
from app.services.llm_service import llm_service
from app.config import settings


def test_llm_service():
    """Test the LLM service directly."""
    print("=" * 50)
    print("Testing LLM Service")
    print("=" * 50)
    
    if not settings.anthropic_api_key:
        print("❌ ANTHROPIC_API_KEY not configured!")
        print("Please add your API key to .env file")
        return
    
    print(f"✅ API Key configured")
    print(f"Model: {settings.llm_model}")
    print(f"Use LLM: {settings.use_llm_for_suggestions}")
    
    db = SessionLocal()
    
    try:
        # Get test user
        user = db.query(User).filter(User.username == "allanbruno").first()
        if not user:
            print("❌ User 'allanbruno' not found!")
            return
            
        print(f"\nTesting with user: {user.username}")
        
        # Get recent transactions
        transactions = db.query(Transaction).filter(
            Transaction.user_id == user.id,
            Transaction.date >= datetime.now(timezone.utc) - timedelta(days=30)
        ).limit(10).all()
        
        print(f"Found {len(transactions)} recent transactions")
        
        # Test LLM suggestion generation
        print("\n🤖 Generating suggestions with Claude...")
        
        async def generate():
            return await llm_service.generate_suggestions(
                user, 
                transactions, 
                [], 
                max_suggestions=3
            )
        
        suggestions = asyncio.run(generate())
        
        print(f"\n✅ Generated {len(suggestions)} suggestions:\n")
        
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. Type: {suggestion['type']}")
            print(f"   Priority: {suggestion['priority']}/10")
            print(f"   Content: {suggestion['content']}")
            print()
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()


def compare_rule_vs_llm():
    """Compare rule-based vs LLM suggestions."""
    print("\n" + "=" * 50)
    print("Comparing Rule-based vs LLM Suggestions")
    print("=" * 50)
    
    db = SessionLocal()
    
    try:
        user = db.query(User).filter(User.username == "allanbruno").first()
        if not user:
            print("❌ User 'allanbruno' not found!")
            return
        
        # Test rule-based
        print("\n📋 Rule-based suggestions:")
        settings.use_llm_for_suggestions = False
        engine_rules = AIEngine(db)
        rule_suggestions = engine_rules.analyze_user(user)
        
        for suggestion in rule_suggestions[:3]:
            print(f"- {suggestion['content'][:100]}...")
        
        # Test LLM-based
        if settings.anthropic_api_key:
            print("\n🤖 LLM-based suggestions:")
            settings.use_llm_for_suggestions = True
            engine_llm = AIEngine(db)
            llm_suggestions = engine_llm.analyze_user(user)
            
            for suggestion in llm_suggestions[:3]:
                print(f"- {suggestion['content'][:100]}...")
        else:
            print("\n⚠️  Skipping LLM test - no API key configured")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()
        # Reset to original setting
        settings.use_llm_for_suggestions = True


def test_error_handling():
    """Test error handling and fallback."""
    print("\n" + "=" * 50)
    print("Testing Error Handling")
    print("=" * 50)
    
    # Temporarily set invalid API key
    original_key = settings.anthropic_api_key
    settings.anthropic_api_key = "invalid-key-test"
    
    db = SessionLocal()
    
    try:
        user = db.query(User).filter(User.username == "allanbruno").first()
        if not user:
            print("❌ User 'allanbruno' not found!")
            return
        
        print("Testing with invalid API key...")
        engine = AIEngine(db)
        suggestions = engine.analyze_user(user)
        
        print(f"✅ Fallback worked! Generated {len(suggestions)} suggestions")
        print("System correctly fell back to rule-based suggestions")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        # Restore original key
        settings.anthropic_api_key = original_key
        db.close()


if __name__ == "__main__":
    print("🚀 AI Concierge LLM Integration Test\n")
    
    # Test 1: Direct LLM service
    test_llm_service()
    
    # Test 2: Compare outputs
    compare_rule_vs_llm()
    
    # Test 3: Error handling
    test_error_handling()
    
    print("\n✅ Tests completed!")
    print("\nNext steps:")
    print("1. Add your ANTHROPIC_API_KEY to .env")
    print("2. Run: python test_llm_suggestions.py")
    print("3. Check the generated suggestions")