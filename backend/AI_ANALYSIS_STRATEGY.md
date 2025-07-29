# Estratégia de Análise de IA - Sistema Concierge

## Como a IA Analisa os Dados

### 1. **Análise de Datas Importantes**

**Dados utilizados:**
- `profiles.birth_date` - Data de nascimento do usuário
- `profiles.spouse_birth_date` - Data de nascimento do cônjuge
- `profiles.spouse_name` - Nome do cônjuge

**Como funciona:**
```python
# Exemplo de análise
def analyze_upcoming_dates():
    # Verificar aniversários nos próximos 7-30 dias
    upcoming_birthdays = check_upcoming_dates(
        user.profile.spouse_birth_date,
        days_ahead=7
    )
    
    # Gerar sugestão proativa
    if upcoming_birthday:
        create_suggestion(
            type="anniversary",
            content="Vi que sexta-feira é aniversário da sua esposa...",
            priority="high",
            scheduled_date=birthday_date - 3_days
        )
```

### 2. **Análise de Padrões de Transações**

**Dados utilizados:**
- `transactions.category` - Para identificar tipos de gastos
- `transactions.description` - Para identificar estabelecimentos específicos
- `transactions.date` - Para identificar padrões temporais
- `transactions.amount` - Para entender faixas de valores

**Padrões identificáveis:**
```python
# Restaurantes frequentes
favorite_restaurants = analyze_frequent_merchants(
    category="restaurant",
    min_frequency=3,
    time_window="6_months"
)

# Gastos em datas especiais
special_date_patterns = correlate_transactions_with_dates(
    transaction_dates,
    special_dates=[birthdays, anniversaries]
)

# Comportamento recorrente
recurring_behaviors = identify_patterns(
    category="flowers",
    near_date=spouse_birthday,
    lookback_years=3
)
```

### 3. **Análise de Comportamento Histórico**

**Dados utilizados:**
- `interactions.action` - Para entender preferências do usuário
- `interactions.feedback` - Para aprender com respostas
- `suggestions.status` - Para avaliar taxa de aceitação

**Aprendizado contínuo:**
```python
# Taxa de aceitação por tipo de sugestão
acceptance_rate = calculate_acceptance_rate(
    suggestion_type="restaurant_reservation",
    user_id=user.id
)

# Horários preferidos para interação
best_interaction_times = analyze_interaction_patterns(
    user.interactions,
    user.profile.preferred_times
)
```

## Melhorias Sugeridas no Modelo de Dados

### 1. **Nova Tabela: special_dates**
```sql
CREATE TABLE special_dates (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    date DATE NOT NULL,
    type VARCHAR(50), -- 'anniversary', 'birthday', 'holiday'
    description VARCHAR(255),
    recurring BOOLEAN DEFAULT TRUE,
    notifications_days_before INTEGER DEFAULT 7
);
```

### 2. **Nova Tabela: merchant_preferences**
```sql
CREATE TABLE merchant_preferences (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    merchant_name VARCHAR(255),
    category VARCHAR(50),
    frequency_score DECIMAL(3,2), -- 0.0 a 1.0
    last_visit DATE,
    average_spend DECIMAL(10,2),
    notes TEXT
);
```

### 3. **Adicionar à tabela transactions:**
- `merchant_name` VARCHAR(255) - Nome do estabelecimento
- `location` VARCHAR(255) - Local da transação
- `tags` JSON - Tags flexíveis ["presente", "aniversário", "rotina"]

### 4. **Adicionar à tabela suggestions:**
- `confidence_score` DECIMAL(3,2) - Confiança da IA (0.0 a 1.0)
- `reasoning` TEXT - Explicação da sugestão
- `alternative_options` JSON - Outras opções consideradas

## Fluxo de Análise da IA

### 1. **Análise Diária (Cron Job)**
```python
def daily_ai_analysis():
    for user in active_users:
        # 1. Verificar datas próximas
        check_upcoming_special_dates(user)
        
        # 2. Analisar padrões recentes
        analyze_recent_transactions(user, days=30)
        
        # 3. Identificar oportunidades
        identify_proactive_suggestions(user)
        
        # 4. Gerar sugestões ranqueadas
        generate_ranked_suggestions(user)
```

### 2. **Análise em Tempo Real**
```python
def on_new_transaction(transaction):
    # 1. Atualizar padrões
    update_user_patterns(transaction)
    
    # 2. Verificar gatilhos
    check_suggestion_triggers(transaction)
    
    # 3. Ajustar sugestões existentes
    adjust_existing_suggestions(transaction)
```

### 3. **Machine Learning Pipeline**
```python
# Features para o modelo
features = {
    # Temporais
    "days_until_birthday": calculate_days_until(spouse_birthday),
    "days_since_last_restaurant": get_days_since_category("restaurant"),
    
    # Comportamentais
    "restaurant_frequency": get_monthly_frequency("restaurant"),
    "average_gift_spending": get_avg_spending_near_dates(),
    
    # Históricos
    "acceptance_rate": get_user_acceptance_rate(),
    "preferred_suggestion_types": get_preferred_types(),
    
    # Contextuais
    "current_month": datetime.now().month,
    "is_weekend": datetime.now().weekday() >= 5,
}

# Predições
predictions = {
    "will_need_restaurant": model.predict_restaurant_need(features),
    "gift_price_range": model.predict_gift_range(features),
    "best_suggestion_time": model.predict_best_time(features),
}
```

## Exemplos Práticos de Análise

### Caso 1: Aniversário do Cônjuge
```python
# Dados analisados:
# - profiles.spouse_birth_date = "1990-07-30"
# - transactions históricos mostram:
#   - Restaurante italiano todo aniversário
#   - Flores compradas 2 dias antes
#   - Presente na faixa de R$ 500-800

# Sugestões geradas (7 dias antes):
suggestions = [
    {
        "type": "anniversary",
        "content": "O aniversário de Juliana está chegando (30/07). Deseja que eu reserve o La Bella Italia para jantar?",
        "priority": "high",
        "confidence_score": 0.95,
        "scheduled_date": "2024-07-27"
    },
    {
        "type": "purchase",
        "content": "Nos últimos anos você enviou flores. Posso providenciar um buquê de rosas vermelhas?",
        "priority": "medium",
        "confidence_score": 0.88,
        "scheduled_date": "2024-07-28"
    }
]
```

### Caso 2: Padrão de Comportamento
```python
# Dados analisados:
# - Toda primeira sexta do mês: jantar em restaurante
# - Sempre no mesmo restaurante japonês
# - Valor médio: R$ 200

# Sugestão gerada (3 dias antes):
suggestion = {
    "type": "routine",
    "content": "Sexta-feira é o primeiro final de semana do mês. Reservo sua mesa no Sushi House como de costume?",
    "priority": "medium",
    "confidence_score": 0.82,
    "reasoning": "Padrão identificado: 8 de 10 primeiras sextas nos últimos meses"
}
```

## Métricas de Sucesso da IA

1. **Taxa de Aceitação**: % de sugestões aceitas
2. **Timing Score**: Quão cedo/tarde foram as sugestões
3. **Relevância Score**: Feedback positivo do usuário
4. **Proatividade Score**: Sugestões antes do usuário pensar
5. **Economia de Tempo**: Tempo poupado do usuário

## Conclusão

O modelo de dados atual **suporta bem** os casos de uso principais:
- ✅ Identificação de datas importantes
- ✅ Análise de padrões de consumo
- ✅ Histórico de comportamento
- ✅ Preferências e feedback

Com as melhorias sugeridas, o sistema terá ainda mais capacidade de:
- 🎯 Maior precisão nas sugestões
- 🧠 Aprendizado mais detalhado
- 📊 Melhor tracking de estabelecimentos
- 🎨 Mais contexto para personalização