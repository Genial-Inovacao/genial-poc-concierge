"""
LLM Service for AI-powered suggestion generation using Claude (Anthropic).
"""
import json
from typing import List, Dict, Optional, Any
from datetime import datetime
import httpx
import asyncio
from decimal import Decimal

from ..config import settings
from ..models import User, Profile, Transaction, Suggestion


class LLMService:
    """Service for interacting with Claude LLM."""
    
    def __init__(self):
        self.api_key = settings.anthropic_api_key
        self.model = settings.llm_model
        self.max_tokens = settings.llm_max_tokens
        self.temperature = settings.llm_temperature
        self.base_url = "https://api.anthropic.com/v1/messages"
        
    def _prepare_user_context(self, user: User, transactions: List[Transaction], 
                            existing_suggestions: List[Suggestion]) -> str:
        """Prepare comprehensive user context for the LLM."""
        profile = user.profile
        
        # Basic profile info
        context = f"""Informações do Usuário:
- Nome: {profile.name or 'Não informado'}
- Idade: {self._calculate_age(profile.birth_date) if profile.birth_date else 'Não informada'}
- Cônjuge: {profile.spouse_name or 'Não informado'}"""

        if profile.spouse_birth_date:
            context += f" (aniversário: {profile.spouse_birth_date.strftime('%d/%m')})"
        
        # Preferences
        if profile.preferences_json:
            prefs = profile.preferences_json
            context += f"\n\nPreferências:"
            if prefs.get('categories_of_interest'):
                context += f"\n- Categorias de interesse: {', '.join(prefs['categories_of_interest'])}"
            if prefs.get('preferred_times'):
                context += f"\n- Horários preferidos: {prefs['preferred_times']}"
                
        # Recent transactions analysis
        if transactions:
            context += "\n\nPadrões de Transações Recentes:"
            
            # Group by category
            category_totals = {}
            merchant_frequency = {}
            
            for t in transactions:
                # Category spending
                if t.category not in category_totals:
                    category_totals[t.category] = 0
                category_totals[t.category] += float(t.amount)
                
                # Merchant frequency
                if t.description:
                    if t.description not in merchant_frequency:
                        merchant_frequency[t.description] = 0
                    merchant_frequency[t.description] += 1
            
            # Top categories
            top_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[:5]
            context += "\n- Principais categorias de gasto:"
            for cat, total in top_categories:
                context += f"\n  • {cat}: R$ {total:.2f}"
            
            # Frequent merchants
            frequent_merchants = sorted(merchant_frequency.items(), key=lambda x: x[1], reverse=True)[:5]
            if frequent_merchants:
                context += "\n- Estabelecimentos frequentes:"
                for merchant, count in frequent_merchants:
                    context += f"\n  • {merchant}: {count}x"
        
        # Recent suggestions and interactions
        if existing_suggestions:
            recent_accepted = [s for s in existing_suggestions if s.status == 'accepted'][-3:]
            recent_rejected = [s for s in existing_suggestions if s.status == 'rejected'][-3:]
            
            if recent_accepted:
                context += "\n\nSugestões aceitas recentemente:"
                for s in recent_accepted:
                    context += f"\n- {s.content[:100]}..."
                    
            if recent_rejected:
                context += "\n\nSugestões rejeitadas recentemente:"
                for s in recent_rejected:
                    context += f"\n- {s.content[:100]}..."
        
        # Current date context
        context += f"\n\nData atual: {datetime.now().strftime('%d/%m/%Y')}"
        context += f"\nDia da semana: {self._get_weekday_pt()}"
        
        return context
    
    def _calculate_age(self, birth_date) -> int:
        """Calculate age from birth date."""
        if not birth_date:
            return 0
        today = datetime.now().date()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    
    def _get_weekday_pt(self) -> str:
        """Get current weekday in Portuguese."""
        weekdays = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 
                   'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']
        return weekdays[datetime.now().weekday()]
    
    async def generate_suggestions(self, user: User, transactions: List[Transaction], 
                                 existing_suggestions: List[Suggestion], 
                                 max_suggestions: int = 5) -> List[Dict[str, Any]]:
        """Generate personalized suggestions using Claude."""
        
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not configured. Please set it in your .env file.")
        
        # Prepare context
        user_context = self._prepare_user_context(user, transactions, existing_suggestions)
        
        # Create the prompt
        prompt = f"""{user_context}

Com base nas informações acima, gere {max_suggestions} sugestões proativas e personalizadas para ajudar este usuário. 

Diretrizes:
1. Seja específico e mencione detalhes do contexto do usuário
2. Varie os tipos de sugestões (economia, lembretes, oportunidades, saúde, relacionamentos)
3. Considere datas importantes, padrões de gasto e preferências
4. Seja útil e prático, com ações claras
5. Use um tom amigável e personalizado
6. Evite sugestões genéricas

Retorne as sugestões em formato JSON com a seguinte estrutura:
{{
  "suggestions": [
    {{
      "type": "anniversary|purchase|routine|seasonal|saving|health",
      "content": "Texto da sugestão personalizada",
      "priority": 1-10,
      "reasoning": "Breve explicação do porquê desta sugestão",
      "category": "categoria relacionada"
    }}
  ]
}}

Gere sugestões criativas e verdadeiramente úteis para o usuário."""

        try:
            # Call Claude API
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.base_url,
                    headers={
                        "x-api-key": self.api_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "max_tokens": self.max_tokens,
                        "temperature": self.temperature,
                        "messages": [
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    },
                    timeout=30.0
                )
                
                if response.status_code != 200:
                    print(f"Claude API error: {response.status_code} - {response.text}")
                    return []
                
                # Parse response
                result = response.json()
                content = result.get("content", [{}])[0].get("text", "{}")
                
                # Extract JSON from response
                try:
                    # Find JSON in the response
                    import re
                    json_match = re.search(r'\{.*\}', content, re.DOTALL)
                    if json_match:
                        suggestions_data = json.loads(json_match.group())
                        return self._format_suggestions(suggestions_data.get("suggestions", []))
                except json.JSONDecodeError:
                    print(f"Failed to parse Claude response as JSON: {content}")
                    
        except Exception as e:
            print(f"Error calling Claude API: {e}")
            
        return []
    
    def _format_suggestions(self, raw_suggestions: List[Dict]) -> List[Dict[str, Any]]:
        """Format suggestions from Claude into our database format."""
        formatted = []
        
        type_mapping = {
            'anniversary': 'ANNIVERSARY',
            'purchase': 'PURCHASE',
            'routine': 'ROUTINE',
            'seasonal': 'SEASONAL',
            'saving': 'SAVINGS',
            'savings': 'SAVINGS',
            'health': 'ROUTINE',  # Map health to routine as we don't have health type
            'reminder': 'REMINDER',
            'recommendation': 'RECOMMENDATION'
        }
        
        for suggestion in raw_suggestions:
            try:
                suggestion_type = type_mapping.get(suggestion.get('type', '').lower(), 'ROUTINE')
                
                formatted.append({
                    'type': suggestion_type,
                    'content': suggestion.get('content', ''),
                    'priority': min(max(int(suggestion.get('priority', 5)), 1), 10),
                    'scheduled_date': datetime.now(),  # Will be refined by AI engine
                    'context_data': json.dumps({
                        'reasoning': suggestion.get('reasoning', ''),
                        'generated_by': 'claude',
                        'model': self.model,
                        'category': suggestion.get('category', 'general')
                    })
                })
            except Exception as e:
                print(f"Error formatting suggestion: {e}")
                continue
                
        return formatted
    
    async def refine_suggestion(self, suggestion: str, user_feedback: str) -> Optional[str]:
        """Refine a suggestion based on user feedback."""
        if not self.api_key:
            return None
            
        prompt = f"""Sugestão original: {suggestion}

Feedback do usuário: {user_feedback}

Refine a sugestão com base no feedback, mantendo-a útil e personalizada. 
Retorne apenas o texto refinado da sugestão, sem explicações adicionais."""

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.base_url,
                    headers={
                        "x-api-key": self.api_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "max_tokens": 200,
                        "temperature": 0.5,
                        "messages": [
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("content", [{}])[0].get("text", "").strip()
                    
        except Exception as e:
            print(f"Error refining suggestion: {e}")
            
        return None


# Singleton instance
llm_service = LLMService()