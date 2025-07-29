#\!/usr/bin/env python3
"""
Adiciona 15 transações variadas para o usuário allanbruno.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta, timezone
from decimal import Decimal
from app.database import SessionLocal
from app.models import User, Transaction
import uuid
import random

def add_transactions():
    db = SessionLocal()
    
    try:
        # Buscar usuário allanbruno
        user = db.query(User).filter(User.username == "allanbruno").first()
        if not user:
            print("❌ Usuário 'allanbruno' não encontrado\!")
            return
        
        print(f"✅ Usuário encontrado: {user.username}")
        
        # Criar 15 transações variadas
        now = datetime.now(timezone.utc)
        transactions_data = [
            # Alimentação
            {
                "type": "expense",
                "amount": Decimal("45.90"),
                "date": now - timedelta(days=1),
                "category": "alimentacao",
                "location": "São Paulo, SP",
                "description": "Almoço - Restaurante Italiano"
            },
            {
                "type": "expense",
                "amount": Decimal("32.50"),
                "date": now - timedelta(days=2),
                "category": "alimentacao",
                "location": "São Paulo, SP",
                "description": "Café da manhã - Padaria Bella Vista"
            },
            {
                "type": "expense",
                "amount": Decimal("89.00"),
                "date": now - timedelta(days=3),
                "category": "alimentacao",
                "location": "São Paulo, SP",
                "description": "Jantar - Churrascaria"
            },
            
            # Transporte
            {
                "type": "expense",
                "amount": Decimal("250.00"),
                "date": now - timedelta(days=4),
                "category": "transporte",
                "location": "Posto Shell - Marginal",
                "description": "Combustível - Gasolina"
            },
            {
                "type": "expense",
                "amount": Decimal("45.00"),
                "date": now - timedelta(days=5),
                "category": "transporte",
                "location": "São Paulo, SP",
                "description": "Uber - Viagens diversas"
            },
            
            # Saúde
            {
                "type": "expense",
                "amount": Decimal("350.00"),
                "date": now - timedelta(days=6),
                "category": "saude",
                "location": "São Paulo, SP",
                "description": "Consulta médica - Cardiologista"
            },
            {
                "type": "expense",
                "amount": Decimal("89.90"),
                "date": now - timedelta(days=7),
                "category": "saude",
                "location": "Farmácia",
                "description": "Medicamentos"
            },
            
            # Lazer
            {
                "type": "expense",
                "amount": Decimal("120.00"),
                "date": now - timedelta(days=8),
                "category": "lazer",
                "location": "Shopping Iguatemi",
                "description": "Cinema - Ingressos família"
            },
            {
                "type": "expense",
                "amount": Decimal("200.00"),
                "date": now - timedelta(days=9),
                "category": "lazer",
                "location": "Teatro Municipal",
                "description": "Show musical"
            },
            
            # Compras
            {
                "type": "expense",
                "amount": Decimal("450.00"),
                "date": now - timedelta(days=10),
                "category": "compras",
                "location": "Shopping Center Norte",
                "description": "Roupas - Presente para Juju"
            },
            {
                "type": "expense",
                "amount": Decimal("299.00"),
                "date": now - timedelta(days=11),
                "category": "compras",
                "location": "Mercado Livre",
                "description": "Eletrônicos - Fone de ouvido"
            },
            
            # Serviços
            {
                "type": "expense",
                "amount": Decimal("39.90"),
                "date": now - timedelta(days=12),
                "category": "servicos",
                "location": "Online",
                "description": "Netflix - Assinatura mensal"
            },
            {
                "type": "expense",
                "amount": Decimal("89.90"),
                "date": now - timedelta(days=13),
                "category": "servicos",
                "location": "Academia",
                "description": "SmartFit - Mensalidade"
            },
            
            # Receitas
            {
                "type": "income",
                "amount": Decimal("2500.00"),
                "date": now - timedelta(days=15),
                "category": "salario",
                "location": None,
                "description": "Freelance - Projeto desenvolvimento"
            },
            
            # Investimento
            {
                "type": "savings",
                "amount": Decimal("1500.00"),
                "date": now - timedelta(days=20),
                "category": "investimento",
                "location": None,
                "description": "Aplicação Tesouro Direto"
            }
        ]
        
        # Inserir transações
        print("\n💳 Adicionando transações:")
        for trans_data in transactions_data:
            transaction = Transaction(
                id=str(uuid.uuid4()),
                user_id=user.id,
                created_at=datetime.now(timezone.utc),
                **trans_data
            )
            db.add(transaction)
            print(f"  ➕ {trans_data['description']} - R$ {trans_data['amount']:.2f} ({trans_data['type']})")
        
        db.commit()
        print(f"\n✅ {len(transactions_data)} transações adicionadas com sucesso\!")
        
        # Mostrar resumo
        total_expense = sum(t['amount'] for t in transactions_data if t['type'] == 'expense')
        total_income = sum(t['amount'] for t in transactions_data if t['type'] == 'income')
        total_savings = sum(t['amount'] for t in transactions_data if t['type'] == 'savings')
        
        print("\n📊 Resumo:")
        print(f"  - Total de despesas: R$ {total_expense:.2f}")
        print(f"  - Total de receitas: R$ {total_income:.2f}")
        print(f"  - Total investido: R$ {total_savings:.2f}")
        print(f"  - Saldo: R$ {(total_income - total_expense):.2f}")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    add_transactions()
EOF < /dev/null