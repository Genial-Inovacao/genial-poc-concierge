#!/usr/bin/env python3
"""
Trigger manual para análise de transações e geração de sugestões com LLM.

Este script permite executar manualmente a análise de IA para um usuário específico,
gerando sugestões baseadas em suas transações recentes.

Uso:
    python trigger_manual_llm.py [username]
    
    Se username não for fornecido, analisa todos os usuários ativos.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import User, Transaction, Suggestion, SuggestionType, SuggestionStatus
from app.services.ai_engine import AIEngine
from app.database import SessionLocal
import json


def print_separator():
    """Imprime separador visual."""
    print("=" * 80)


def print_transaction_summary(transactions):
    """Imprime resumo das transações."""
    if not transactions:
        print("   📊 Nenhuma transação encontrada")
        return
    
    # Agregar por categoria
    category_totals = {}
    type_totals = {}
    
    for t in transactions:
        # Por categoria
        if t.category not in category_totals:
            category_totals[t.category] = {"count": 0, "total": 0}
        category_totals[t.category]["count"] += 1
        category_totals[t.category]["total"] += float(t.amount)
        
        # Por tipo
        if t.type not in type_totals:
            type_totals[t.type] = {"count": 0, "total": 0}
        type_totals[t.type]["count"] += 1
        type_totals[t.type]["total"] += float(t.amount)
    
    print(f"   📊 Total de transações: {len(transactions)}")
    print("\n   💰 Por tipo:")
    for type_name, data in sorted(type_totals.items()):
        print(f"      - {type_name}: {data['count']} transações, R$ {data['total']:.2f}")
    
    print("\n   📂 Por categoria (top 5):")
    sorted_categories = sorted(category_totals.items(), key=lambda x: x[1]["total"], reverse=True)[:5]
    for cat, data in sorted_categories:
        print(f"      - {cat}: {data['count']} transações, R$ {data['total']:.2f}")


def analyze_single_user(db, username):
    """Analisa um usuário específico."""
    print(f"\n🔍 Buscando usuário: {username}")
    
    user = db.query(User).filter(User.username == username).first()
    if not user:
        print(f"❌ Usuário '{username}' não encontrado!")
        return False
    
    print(f"✅ Usuário encontrado: {user.username} ({user.email})")
    
    # Verificar perfil
    if not user.profile:
        print("⚠️  Usuário sem perfil configurado")
    else:
        profile = user.profile
        print(f"👤 Perfil: {profile.name}")
        if profile.birth_date:
            print(f"   - Aniversário: {profile.birth_date.strftime('%d/%m')}")
        if profile.spouse_name:
            print(f"   - Cônjuge: {profile.spouse_name}")
            if profile.spouse_birth_date:
                print(f"   - Aniversário cônjuge: {profile.spouse_birth_date.strftime('%d/%m')}")
    
    # Buscar transações recentes
    print("\n📈 Transações recentes (últimos 90 dias):")
    from datetime import timedelta
    ninety_days_ago = datetime.now(timezone.utc) - timedelta(days=90)
    recent_transactions = db.query(Transaction).filter(
        Transaction.user_id == user.id,
        Transaction.date >= ninety_days_ago
    ).order_by(Transaction.date.desc()).all()
    
    print_transaction_summary(recent_transactions)
    
    # Buscar sugestões existentes
    existing_pending = db.query(Suggestion).filter(
        Suggestion.user_id == user.id,
        Suggestion.status == SuggestionStatus.PENDING
    ).count()
    
    print(f"\n💡 Sugestões pendentes atuais: {existing_pending}")
    
    # Executar análise de IA
    print("\n🤖 Executando análise de IA...")
    print_separator()
    
    try:
        engine = AIEngine(db)
        suggestions = engine.analyze_user(user)
        
        if not suggestions:
            print("⚠️  Nenhuma nova sugestão gerada")
            return True
        
        print(f"\n✨ {len(suggestions)} sugestões geradas:\n")
        
        # Salvar sugestões
        saved_count = 0
        for i, suggestion_data in enumerate(suggestions, 1):
            # Verificar se já existe sugestão similar
            existing = db.query(Suggestion).filter(
                Suggestion.user_id == user.id,
                Suggestion.content == suggestion_data['content'],
                Suggestion.status.in_([SuggestionStatus.PENDING, SuggestionStatus.ACCEPTED, SuggestionStatus.SNOOZED])
            ).first()
            
            if existing:
                print(f"   {i}. ⏭️  Sugestão similar já existe (ignorada)")
                continue
            
            # Criar nova sugestão
            # IMPORTANTE: Sempre salvar como strings minúsculas no banco
            if hasattr(suggestion_data.get('type'), 'value'):
                # É um objeto Enum, pegar o valor
                suggestion_data['type'] = suggestion_data['type'].value
            else:
                # É uma string, garantir que seja minúscula
                suggestion_data['type'] = str(suggestion_data['type']).lower()
            
            # Garantir que status seja 'pending' (minúsculo)
            if 'status' not in suggestion_data:
                suggestion_data['status'] = 'pending'
            elif hasattr(suggestion_data.get('status'), 'value'):
                suggestion_data['status'] = suggestion_data['status'].value
            else:
                suggestion_data['status'] = str(suggestion_data['status']).lower()
            
            new_suggestion = Suggestion(
                user_id=user.id,
                **suggestion_data
            )
            db.add(new_suggestion)
            saved_count += 1
            
            # Exibir detalhes
            type_str = suggestion_data['type'].value if hasattr(suggestion_data['type'], 'value') else str(suggestion_data['type'])
            print(f"   {i}. [{type_str}] (Prioridade: {suggestion_data['priority']})")
            print(f"      📝 {suggestion_data['content']}")
            print(f"      📅 Agendada para: {suggestion_data['scheduled_date'].strftime('%d/%m/%Y %H:%M')}")
            
            # Mostrar contexto se disponível
            if suggestion_data.get('context_data'):
                try:
                    context = json.loads(suggestion_data['context_data'])
                    if context.get('reasoning'):
                        print(f"      💭 Razão: {context['reasoning']}")
                    if context.get('generated_by') == 'claude':
                        print(f"      🤖 Gerada por: Claude ({context.get('model', 'unknown')})")
                except:
                    pass
            print()
        
        # Salvar no banco
        if saved_count > 0:
            db.commit()
            print(f"✅ {saved_count} novas sugestões salvas no banco de dados")
        else:
            print("ℹ️  Todas as sugestões geradas já existiam")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante análise: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return False


def analyze_all_users(db):
    """Analisa todos os usuários ativos."""
    print("\n📋 Analisando todos os usuários ativos...")
    
    users = db.query(User).filter(User.is_active == True).all()
    print(f"👥 {len(users)} usuários ativos encontrados")
    
    success_count = 0
    error_count = 0
    
    for user in users:
        print_separator()
        if analyze_single_user(db, user.username):
            success_count += 1
        else:
            error_count += 1
    
    print_separator()
    print(f"\n📊 Resumo final:")
    print(f"   ✅ Sucesso: {success_count} usuários")
    print(f"   ❌ Erros: {error_count} usuários")


def main():
    """Função principal."""
    print("🚀 Trigger Manual de Análise LLM")
    print("================================")
    
    db = SessionLocal()
    
    try:
        if len(sys.argv) > 1:
            # Analisar usuário específico
            username = sys.argv[1]
            analyze_single_user(db, username)
        else:
            # Analisar todos os usuários
            print("\nNenhum usuário especificado. Analisando todos os usuários ativos...")
            print("Para analisar um usuário específico, use: python trigger_manual_llm.py [username]")
            
            response = input("\nDeseja continuar? (s/n): ")
            if response.lower() == 's':
                analyze_all_users(db)
            else:
                print("Operação cancelada.")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Operação interrompida pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()
        print("\n✅ Conexão com banco de dados fechada")


if __name__ == "__main__":
    main()