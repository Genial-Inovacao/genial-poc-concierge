# Regras de Inserção de Dados - AI Concierge

Este documento descreve as regras e formatos corretos para inserção de dados nas tabelas principais do sistema.

## 1. Tabela TRANSACTIONS

### Estrutura da Tabela
```sql
CREATE TABLE transactions (
    id CHAR(36) NOT NULL,           -- UUID gerado automaticamente
    user_id CHAR(36) NOT NULL,      -- UUID do usuário
    type VARCHAR(50) NOT NULL,      -- Tipo da transação (SEMPRE minúsculo)
    amount NUMERIC(10, 2) NOT NULL, -- Valor decimal
    date DATETIME NOT NULL,         -- Data da transação
    category VARCHAR(50) NOT NULL,  -- Categoria (SEMPRE minúsculo)
    location VARCHAR(255),          -- Localização (opcional)
    description VARCHAR(500) NOT NULL, -- Descrição
    created_at DATETIME NOT NULL,   -- Timestamp de criação
    metadata_json TEXT              -- Metadados extras (opcional)
);
```

### Valores Válidos

#### Types (SEMPRE minúsculo):
- `expense` - Despesa
- `income` - Receita
- `purchase` - Compra
- `savings` - Poupança/Investimento
- `subscription` - Assinatura

#### Categories (SEMPRE minúsculo):
- `alimentacao` - Alimentação
- `transporte` - Transporte
- `saude` - Saúde
- `lazer` - Lazer/Entretenimento
- `investimento` - Investimentos
- `salario` - Salário
- `servicos` - Serviços
- `compras` - Compras gerais
- `restaurant` - Restaurante
- `grocery` - Supermercado
- `fitness` - Academia/Esportes
- `health` - Saúde
- `entertainment` - Entretenimento
- `shopping` - Shopping
- `gift` - Presentes

### Exemplos de INSERT

```sql
-- 1. Despesa com alimentação
INSERT INTO transactions (id, user_id, type, amount, date, category, location, description, created_at)
VALUES (
    '550e8400-e29b-41d4-a716-446655440001',
    'user-uuid-here',
    'expense',                    -- MINÚSCULO
    89.90,
    '2024-07-29 12:30:00',
    'alimentacao',               -- MINÚSCULO
    'São Paulo, SP',
    'Almoço - Restaurante Japonês Sushi Place',
    '2024-07-29 12:30:00'
);

-- 2. Receita de salário
INSERT INTO transactions (id, user_id, type, amount, date, category, location, description, created_at)
VALUES (
    '550e8400-e29b-41d4-a716-446655440002',
    'user-uuid-here',
    'income',                    -- MINÚSCULO
    15000.00,
    '2024-07-05 09:00:00',
    'salario',                   -- MINÚSCULO
    NULL,
    'Salário mensal - Empresa XYZ',
    '2024-07-05 09:00:00'
);

-- 3. Investimento
INSERT INTO transactions (id, user_id, type, amount, date, category, location, description, created_at)
VALUES (
    '550e8400-e29b-41d4-a716-446655440003',
    'user-uuid-here',
    'savings',                   -- MINÚSCULO
    2000.00,
    '2024-07-15 10:00:00',
    'investimento',              -- MINÚSCULO
    NULL,
    'Aplicação CDB 120% CDI',
    '2024-07-15 10:00:00'
);

-- 4. Compra de presente
INSERT INTO transactions (id, user_id, type, amount, date, category, location, description, created_at)
VALUES (
    '550e8400-e29b-41d4-a716-446655440004',
    'user-uuid-here',
    'purchase',                  -- MINÚSCULO
    350.00,
    '2024-07-28 16:00:00',
    'gift',                      -- MINÚSCULO
    'Shopping Iguatemi, SP',
    'Presente aniversário esposa - Perfume',
    '2024-07-28 16:00:00'
);

-- 5. Despesa com transporte
INSERT INTO transactions (id, user_id, type, amount, date, category, location, description, created_at)
VALUES (
    '550e8400-e29b-41d4-a716-446655440005',
    'user-uuid-here',
    'expense',                   -- MINÚSCULO
    250.00,
    '2024-07-20 08:00:00',
    'transporte',                -- MINÚSCULO
    'Posto Shell - Marginal',
    'Combustível - Gasolina',
    '2024-07-20 08:00:00'
);
```

## 2. Tabela SUGGESTIONS

### Estrutura da Tabela
```sql
CREATE TABLE suggestions (
    id CHAR(36) NOT NULL,              -- UUID gerado automaticamente
    user_id CHAR(36) NOT NULL,         -- UUID do usuário
    content TEXT NOT NULL,             -- Conteúdo da sugestão
    type VARCHAR(50) NOT NULL,         -- Tipo (SEMPRE minúsculo)
    priority INTEGER NOT NULL,         -- Prioridade (1-10)
    status VARCHAR(50) NOT NULL,       -- Status (SEMPRE minúsculo)
    scheduled_date DATETIME NOT NULL,  -- Data agendada
    context_data TEXT,                 -- Contexto em JSON
    created_at DATETIME NOT NULL,      -- Timestamp de criação
    executed_at DATETIME               -- Timestamp de execução (opcional)
);
```

### Valores Válidos

#### Types (SEMPRE minúsculo):
- `anniversary` - Aniversários e datas especiais
- `purchase` - Sugestões de compra
- `routine` - Rotinas e hábitos
- `seasonal` - Sazonal/temporal
- `savings` - Economia e investimentos
- `reminder` - Lembretes gerais
- `recommendation` - Recomendações

#### Status (SEMPRE minúsculo):
- `pending` - Pendente
- `accepted` - Aceita
- `rejected` - Rejeitada
- `executed` - Executada
- `snoozed` - Adiada
- `expired` - Expirada

### Exemplos de INSERT

```sql
-- 1. Sugestão de aniversário
INSERT INTO suggestions (id, user_id, content, type, priority, status, scheduled_date, context_data, created_at)
VALUES (
    '650e8400-e29b-41d4-a716-446655440001',
    'user-uuid-here',
    'O aniversário de Maria está chegando (30/07). Deseja que eu reserve o Restaurante Fasano?',
    'anniversary',               -- MINÚSCULO
    8,                          -- Alta prioridade
    'pending',                  -- MINÚSCULO
    '2024-07-30 10:00:00',
    '{"person": "Maria", "occasion": "birthday", "days_until": 1, "suggested_restaurant": "Restaurante Fasano"}',
    '2024-07-29 10:00:00'
);

-- 2. Sugestão de rotina
INSERT INTO suggestions (id, user_id, content, type, priority, status, scheduled_date, context_data, created_at)
VALUES (
    '650e8400-e29b-41d4-a716-446655440002',
    'user-uuid-here',
    'Está na hora de abastecer no Posto Shell? Você costuma fazer isso a cada 7 dias.',
    'routine',                  -- MINÚSCULO
    5,                         -- Prioridade média
    'pending',                 -- MINÚSCULO
    '2024-07-29 08:00:00',
    '{"pattern": "recurring", "description": "Posto Shell", "frequency": 4, "average_interval_days": 7, "days_since_last": 6}',
    '2024-07-29 08:00:00'
);

-- 3. Sugestão de economia
INSERT INTO suggestions (id, user_id, content, type, priority, status, scheduled_date, context_data, created_at)
VALUES (
    '650e8400-e29b-41d4-a716-446655440003',
    'user-uuid-here',
    'Você gastou R$ 1.200 em alimentação este mês, 20% acima da média. Que tal estabelecer um limite de R$ 1.000?',
    'savings',                  -- MINÚSCULO
    6,
    'pending',                  -- MINÚSCULO
    '2024-07-29 09:00:00',
    '{"category": "alimentacao", "current_spending": 1200, "average_spending": 1000, "percentage_above": 20}',
    '2024-07-29 09:00:00'
);

-- 4. Sugestão de compra
INSERT INTO suggestions (id, user_id, content, type, priority, status, scheduled_date, context_data, created_at)
VALUES (
    '650e8400-e29b-41d4-a716-446655440004',
    'user-uuid-here',
    'Nos últimos anos você enviou flores para Maria. Posso providenciar um buquê especial?',
    'purchase',                 -- MINÚSCULO
    7,
    'pending',                  -- MINÚSCULO
    '2024-07-29 14:00:00',
    '{"person": "Maria", "occasion": "birthday", "item": "flowers", "historical_pattern": true}',
    '2024-07-29 10:00:00'
);

-- 5. Lembrete sazonal
INSERT INTO suggestions (id, user_id, content, type, priority, status, scheduled_date, context_data, created_at)
VALUES (
    '650e8400-e29b-41d4-a716-446655440005',
    'user-uuid-here',
    'O inverno está chegando! Hora de fazer a revisão do aquecedor e comprar cobertores novos?',
    'seasonal',                 -- MINÚSCULO
    4,
    'pending',                  -- MINÚSCULO
    '2024-06-01 09:00:00',
    '{"season": "winter", "suggested_actions": ["heater_maintenance", "buy_blankets"]}',
    '2024-05-25 09:00:00'
);

-- 6. Sugestão aceita e executada
INSERT INTO suggestions (id, user_id, content, type, priority, status, scheduled_date, context_data, created_at, executed_at)
VALUES (
    '650e8400-e29b-41d4-a716-446655440006',
    'user-uuid-here',
    'Renovar assinatura Netflix antes do vencimento',
    'reminder',                 -- MINÚSCULO
    5,
    'executed',                 -- MINÚSCULO
    '2024-07-15 10:00:00',
    '{"service": "Netflix", "action": "renewal", "monthly_cost": 39.90}',
    '2024-07-10 10:00:00',
    '2024-07-14 15:30:00'      -- Data de execução
);
```

## 3. Regras Importantes

### Para Transactions:
1. **SEMPRE use minúsculas** para `type` e `category`
2. O campo `description` deve ser claro e descritivo
3. Use `location` quando relevante (opcional)
4. O `amount` deve ser positivo
5. A `date` pode ser diferente de `created_at`

### Para Suggestions:
1. **SEMPRE use minúsculas** para `type` e `status`
2. `priority` deve estar entre 1 e 10 (10 = máxima prioridade)
3. `context_data` deve ser um JSON válido
4. `scheduled_date` indica quando a sugestão deve ser apresentada
5. `executed_at` só é preenchido quando `status = 'executed'`

### Trigger de IA:
- Ao inserir novas transações via API, o sistema automaticamente:
  1. Analisa o perfil do usuário
  2. Verifica padrões de gastos
  3. Identifica datas especiais
  4. Gera sugestões relevantes usando LLM (se configurado)

### Formatação JSON para context_data:
```json
{
    "key": "value",
    "number": 123,
    "boolean": true,
    "array": ["item1", "item2"],
    "nested": {
        "subkey": "subvalue"
    }
}
```

## 4. Exemplos de Queries Úteis

```sql
-- Verificar transações recentes
SELECT type, category, amount, description 
FROM transactions 
WHERE user_id = 'user-uuid-here' 
ORDER BY date DESC 
LIMIT 10;

-- Verificar sugestões pendentes
SELECT type, priority, content 
FROM suggestions 
WHERE user_id = 'user-uuid-here' 
  AND status = 'pending' 
ORDER BY priority DESC, scheduled_date ASC;

-- Estatísticas de gastos por categoria
SELECT category, SUM(amount) as total 
FROM transactions 
WHERE user_id = 'user-uuid-here' 
  AND type = 'expense' 
  AND date >= date('now', '-30 days')
GROUP BY category 
ORDER BY total DESC;
```