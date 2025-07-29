from datetime import datetime, timezone, timedelta
from decimal import Decimal
import random
from sqlalchemy.orm import Session
from app.database import get_db, engine
from app.models import User, Transaction

# Transaction categories and types
CATEGORIES = ['alimentacao', 'transporte', 'lazer', 'saude', 'educacao', 'compras', 'servicos']
TYPES = ['expense', 'savings', 'income']

def create_transactions_for_allanbruno():
    db = next(get_db())
    
    # Find allanbruno user
    user = db.query(User).filter(User.username == "allanbruno").first()
    if not user:
        print("User allanbruno not found!")
        return
    
    print(f"Creating transactions for user: {user.username}")
    
    # Create transactions for the last 90 days
    now = datetime.now(timezone.utc)
    transactions = []
    
    # Regular monthly expenses
    for i in range(3):  # Last 3 months
        month_offset = now - timedelta(days=30 * i)
        
        # Rent
        transactions.append(Transaction(
            user_id=user.id,
            type='expense',
            amount=Decimal('2500.00'),
            date=month_offset.replace(day=5),
            category='servicos',
            description='Aluguel do apartamento',
            location='São Paulo, SP'
        ))
        
        # Internet
        transactions.append(Transaction(
            user_id=user.id,
            type='expense',
            amount=Decimal('120.00'),
            date=month_offset.replace(day=10),
            category='servicos',
            description='Internet fibra 500MB',
            location='São Paulo, SP'
        ))
        
        # Gym
        transactions.append(Transaction(
            user_id=user.id,
            type='expense',
            amount=Decimal('180.00'),
            date=month_offset.replace(day=1),
            category='saude',
            description='Academia SmartFit',
            location='São Paulo, SP'
        ))
    
    # Recent transactions (last 30 days)
    for i in range(30):
        date = now - timedelta(days=i)
        
        # Daily coffee
        if random.random() > 0.3:  # 70% chance of buying coffee
            transactions.append(Transaction(
                user_id=user.id,
                type='expense',
                amount=Decimal(f'{random.uniform(12, 25):.2f}'),
                date=date.replace(hour=8, minute=random.randint(0, 59)),
                category='alimentacao',
                description='Café da manhã - Starbucks',
                location='São Paulo, SP'
            ))
        
        # Lunch (weekdays)
        if date.weekday() < 5 and random.random() > 0.2:
            transactions.append(Transaction(
                user_id=user.id,
                type='expense',
                amount=Decimal(f'{random.uniform(25, 45):.2f}'),
                date=date.replace(hour=12, minute=random.randint(0, 59)),
                category='alimentacao',
                description=random.choice(['iFood', 'Restaurante', 'Padaria', 'Sushi']),
                location='São Paulo, SP'
            ))
        
        # Random expenses
        if random.random() > 0.7:
            category = random.choice(['transporte', 'lazer', 'compras'])
            if category == 'transporte':
                descriptions = ['Uber', 'Gasolina', '99', 'Metrô']
                amount_range = (15, 60)
            elif category == 'lazer':
                descriptions = ['Cinema', 'Netflix', 'Spotify', 'Bar', 'Restaurante']
                amount_range = (20, 150)
            else:  # compras
                descriptions = ['Mercado', 'Farmácia', 'Amazon', 'Roupas']
                amount_range = (30, 300)
            
            transactions.append(Transaction(
                user_id=user.id,
                type='expense',
                amount=Decimal(f'{random.uniform(*amount_range):.2f}'),
                date=date.replace(hour=random.randint(10, 22), minute=random.randint(0, 59)),
                category=category,
                description=random.choice(descriptions),
                location='São Paulo, SP'
            ))
    
    # Some savings
    for i in range(2):  # Last 2 months
        month_offset = now - timedelta(days=30 * i)
        transactions.append(Transaction(
            user_id=user.id,
            type='savings',
            amount=Decimal('500.00'),
            date=month_offset.replace(day=25),
            category='investimento',
            description='Poupança mensal',
            location='São Paulo, SP'
        ))
    
    # Income (salary)
    for i in range(3):  # Last 3 months
        month_offset = now - timedelta(days=30 * i)
        transactions.append(Transaction(
            user_id=user.id,
            type='income',
            amount=Decimal('8500.00'),
            date=month_offset.replace(day=28),
            category='salario',
            description='Salário mensal',
            location='São Paulo, SP'
        ))
    
    # Add all transactions
    for transaction in transactions:
        db.add(transaction)
    
    db.commit()
    print(f"Created {len(transactions)} transactions for allanbruno")
    
    # Show summary
    total_expenses = sum(t.amount for t in transactions if t.type == 'expense')
    total_savings = sum(t.amount for t in transactions if t.type == 'savings')
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    
    print(f"\nSummary:")
    print(f"Total expenses: R$ {total_expenses:.2f}")
    print(f"Total savings: R$ {total_savings:.2f}")
    print(f"Total income: R$ {total_income:.2f}")
    print(f"Net: R$ {(total_income - total_expenses + total_savings):.2f}")

if __name__ == "__main__":
    create_transactions_for_allanbruno()