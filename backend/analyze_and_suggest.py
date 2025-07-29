#!/usr/bin/env python3
"""
Script avançado para análise de transações e geração de sugestões com LLM.

Funcionalidades:
- Análise detalhada de transações por período
- Geração forçada de sugestões LLM (ignora cache)
- Modo debug com informações detalhadas
- Filtros por categoria e tipo de transação

Uso:
    python analyze_and_suggest.py [username] [opções]
    
Opções:
    --days N          Analisar últimos N dias (padrão: 90)
    --force-llm       Forçar uso de LLM mesmo se desabilitado
    --debug           Modo debug com mais informações
    --dry-run         Não salvar sugestões no banco
    --category CAT    Filtrar transações por categoria
    --min-suggestions N  Gerar no mínimo N sugestões (padrão: 3)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import argparse
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from app.database import SessionLocal
from app.models import User, Transaction, Suggestion, SuggestionType, SuggestionStatus
from app.services.ai_engine import AIEngine
from app.config import settings
import json


class EnhancedAIAnalyzer:
    """Analisador avançado com mais controles."""
    
    def __init__(self, db, debug=False, force_llm=False):
        self.db = db
        self.debug = debug
        self.force_llm = force_llm
        self.ai_engine = AIEngine(db)
        
        # Forçar LLM se solicitado
        if force_llm:
            self.ai_engine.use_llm = True
    
    def analyze_transaction_patterns_detailed(self, user, transactions, days):
        """Análise detalhada de padrões de transações."""
        print(f"\n📊 Análise detalhada de {len(transactions)} transações dos últimos {days} dias:")
        
        # Estatísticas gerais
        total_expense = sum(t.amount for t in transactions if t.type == 'expense')
        total_income = sum(t.amount for t in transactions if t.type == 'income')
        total_savings = sum(t.amount for t in transactions if t.type == 'savings')
        
        print(f"\n💰 Resumo Financeiro:")
        print(f"   - Total de despesas: R$ {total_expense:.2f}")
        print(f"   - Total de receitas: R$ {total_income:.2f}")
        print(f"   - Total poupado: R$ {total_savings:.2f}")
        print(f"   - Saldo líquido: R$ {(total_income - total_expense):.2f}")
        
        # Análise por categoria
        category_analysis = {}
        for t in transactions:
            if t.category not in category_analysis:
                category_analysis[t.category] = {
                    'count': 0,
                    'total': Decimal('0'),
                    'transactions': []
                }
            category_analysis[t.category]['count'] += 1
            category_analysis[t.category]['total'] += t.amount
            category_analysis[t.category]['transactions'].append(t)
        
        print("\n📂 Análise por Categoria:")
        sorted_categories = sorted(
            category_analysis.items(), 
            key=lambda x: x[1]['total'], 
            reverse=True
        )
        
        for cat, data in sorted_categories[:10]:
            avg = data['total'] / data['count']
            print(f"   - {cat}:")
            print(f"     • Total: R$ {data['total']:.2f}")
            print(f"     • Quantidade: {data['count']} transações")
            print(f"     • Média: R$ {avg:.2f}")
            
            if self.debug:
                # Mostrar transações mais recentes desta categoria
                recent = sorted(data['transactions'], key=lambda x: x.date, reverse=True)[:3]
                for t in recent:
                    print(f"       → {t.date.strftime('%d/%m')}: {t.description} (R$ {t.amount:.2f})")
        
        # Identificar padrões temporais
        print("\n📅 Padrões Temporais:")
        
        # Gastos por dia da semana
        weekday_spending = {}
        for t in transactions:
            if t.type == 'expense':
                weekday = t.date.strftime('%A')
                if weekday not in weekday_spending:
                    weekday_spending[weekday] = Decimal('0')
                weekday_spending[weekday] += t.amount
        
        if weekday_spending:
            print("   Gastos por dia da semana:")
            for day, total in sorted(weekday_spending.items(), key=lambda x: x[1], reverse=True):
                print(f"     - {day}: R$ {total:.2f}")
        
        # Identificar gastos recorrentes
        print("\n🔄 Possíveis Gastos Recorrentes:")
        
        # Agrupar por descrição similar
        description_groups = {}
        for t in transactions:
            # Simplificar descrição para agrupamento
            key = t.description.lower().split('-')[0].strip()
            if key not in description_groups:
                description_groups[key] = []
            description_groups[key].append(t)
        
        # Identificar recorrências
        recurrent_patterns = []
        for desc, trans_list in description_groups.items():
            if len(trans_list) >= 3:  # Pelo menos 3 ocorrências
                dates = sorted([t.date for t in trans_list])
                intervals = []
                for i in range(1, len(dates)):
                    interval = (dates[i] - dates[i-1]).days
                    intervals.append(interval)
                
                if intervals:
                    avg_interval = sum(intervals) / len(intervals)
                    if avg_interval < 40:  # Recorrência mensal ou mais frequente
                        recurrent_patterns.append({
                            'description': desc,
                            'count': len(trans_list),
                            'avg_interval': avg_interval,
                            'total_spent': sum(t.amount for t in trans_list),
                            'last_date': dates[-1]
                        })
        
        # Mostrar padrões recorrentes
        for pattern in sorted(recurrent_patterns, key=lambda x: x['count'], reverse=True)[:5]:
            print(f"   - {pattern['description'].title()}:")
            print(f"     • Frequência: a cada {pattern['avg_interval']:.0f} dias")
            print(f"     • Ocorrências: {pattern['count']}x")
            print(f"     • Total gasto: R$ {pattern['total_spent']:.2f}")
            print(f"     • Última vez: {pattern['last_date'].strftime('%d/%m/%Y')}")
        
        return category_analysis, recurrent_patterns
    
    def generate_custom_suggestions(self, user, transactions, min_suggestions=3):
        """Gera sugestões customizadas com mais controle."""
        print(f"\n🤖 Gerando sugestões (mínimo: {min_suggestions})...")
        
        suggestions = []
        attempts = 0
        max_attempts = 3
        
        while len(suggestions) < min_suggestions and attempts < max_attempts:
            attempts += 1
            
            if self.debug:
                print(f"   Tentativa {attempts}/{max_attempts}...")
            
            # Gerar sugestões
            new_suggestions = self.ai_engine.analyze_user(user)
            
            # Filtrar duplicatas
            for sug in new_suggestions:
                is_duplicate = False
                for existing in suggestions:
                    if existing['content'] == sug['content']:
                        is_duplicate = True
                        break
                
                if not is_duplicate:
                    suggestions.append(sug)
            
            if self.debug:
                print(f"   → {len(new_suggestions)} sugestões geradas, {len(suggestions)} únicas até agora")
        
        return suggestions[:min_suggestions] if len(suggestions) > min_suggestions else suggestions


def main():
    """Função principal com argumentos."""
    parser = argparse.ArgumentParser(
        description='Análise avançada de transações e geração de sugestões'
    )
    parser.add_argument('username', nargs='?', help='Nome de usuário para análise')
    parser.add_argument('--days', type=int, default=90, help='Número de dias para análise')
    parser.add_argument('--force-llm', action='store_true', help='Forçar uso de LLM')
    parser.add_argument('--debug', action='store_true', help='Modo debug')
    parser.add_argument('--dry-run', action='store_true', help='Não salvar no banco')
    parser.add_argument('--category', help='Filtrar por categoria')
    parser.add_argument('--min-suggestions', type=int, default=3, help='Número mínimo de sugestões')
    
    args = parser.parse_args()
    
    print("🚀 Análise Avançada de Transações e Sugestões LLM")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        # Verificar configuração LLM
        if args.force_llm or settings.use_llm_for_suggestions:
            if settings.anthropic_api_key:
                print("✅ LLM habilitado (Claude)")
            else:
                print("⚠️  LLM solicitado mas API key não configurada!")
                if not args.force_llm:
                    print("   Usando sistema baseado em regras")
        else:
            print("ℹ️  Usando sistema baseado em regras")
        
        # Buscar usuário
        if args.username:
            user = db.query(User).filter(User.username == args.username).first()
            if not user:
                print(f"\n❌ Usuário '{args.username}' não encontrado!")
                return
            users = [user]
        else:
            users = db.query(User).filter(User.is_active == True).all()
            print(f"\n👥 {len(users)} usuários ativos encontrados")
        
        # Analisar cada usuário
        analyzer = EnhancedAIAnalyzer(db, debug=args.debug, force_llm=args.force_llm)
        
        for user in users:
            print(f"\n{'='*60}")
            print(f"👤 Analisando: {user.username}")
            
            # Buscar transações
            query = db.query(Transaction).filter(
                Transaction.user_id == user.id,
                Transaction.date >= datetime.now(timezone.utc) - timedelta(days=args.days)
            )
            
            if args.category:
                query = query.filter(Transaction.category == args.category)
            
            transactions = query.order_by(Transaction.date.desc()).all()
            
            if not transactions:
                print("   ⚠️  Nenhuma transação encontrada no período")
                continue
            
            # Análise detalhada
            category_analysis, patterns = analyzer.analyze_transaction_patterns_detailed(
                user, transactions, args.days
            )
            
            # Gerar sugestões
            suggestions = analyzer.generate_custom_suggestions(
                user, transactions, args.min_suggestions
            )
            
            print(f"\n✨ {len(suggestions)} sugestões geradas:")
            
            # Mostrar e salvar sugestões
            saved_count = 0
            for i, sug in enumerate(suggestions, 1):
                print(f"\n   {i}. [{sug['type'].value}] (Prioridade: {sug['priority']})")
                print(f"      📝 {sug['content']}")
                print(f"      📅 {sug['scheduled_date'].strftime('%d/%m/%Y')}")
                
                if args.debug and sug.get('context_data'):
                    try:
                        context = json.loads(sug['context_data'])
                        print(f"      🔍 Contexto: {json.dumps(context, indent=8)}")
                    except:
                        pass
                
                # Salvar se não for dry-run
                if not args.dry_run:
                    # Verificar duplicata
                    existing = db.query(Suggestion).filter(
                        Suggestion.user_id == user.id,
                        Suggestion.content == sug['content'],
                        Suggestion.status.in_([SuggestionStatus.PENDING, SuggestionStatus.ACCEPTED])
                    ).first()
                    
                    if not existing:
                        # Garantir que type e status sejam strings minúsculas
                        if hasattr(sug.get('type'), 'value'):
                            sug['type'] = sug['type'].value
                        sug['type'] = str(sug['type']).lower()
                        
                        if 'status' in sug:
                            if hasattr(sug.get('status'), 'value'):
                                sug['status'] = sug['status'].value
                            sug['status'] = str(sug['status']).lower()
                        else:
                            sug['status'] = 'pending'
                        
                        new_suggestion = Suggestion(user_id=user.id, **sug)
                        db.add(new_suggestion)
                        saved_count += 1
            
            if not args.dry_run and saved_count > 0:
                db.commit()
                print(f"\n✅ {saved_count} sugestões salvas no banco")
            elif args.dry_run:
                print("\n⚠️  Modo dry-run: nenhuma sugestão foi salva")
    
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()