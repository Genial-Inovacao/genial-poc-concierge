# Schema do Banco de Dados - Sistema Concierge IA

## Tabelas e Relacionamentos

### 1. **users**
Tabela principal de usuários do sistema.

| Coluna | Tipo | Descrição | Constraints |
|--------|------|-----------|-------------|
| id | UUID | Identificador único | PRIMARY KEY |
| username | VARCHAR(50) | Nome de usuário | UNIQUE, NOT NULL |
| email | VARCHAR(255) | Email do usuário | UNIQUE, NOT NULL |
| hashed_password | VARCHAR(255) | Senha criptografada | NOT NULL |
| is_active | BOOLEAN | Status do usuário | DEFAULT TRUE |
| created_at | TIMESTAMP | Data de criação | NOT NULL |
| updated_at | TIMESTAMP | Data de atualização | NOT NULL |

**Relacionamentos:**
- `profiles` (1:1) - Um usuário tem um perfil
- `transactions` (1:N) - Um usuário tem várias transações
- `suggestions` (1:N) - Um usuário tem várias sugestões
- `interactions` (1:N) - Um usuário tem várias interações

---

### 2. **profiles**
Informações pessoais e preferências dos usuários.

| Coluna | Tipo | Descrição | Constraints |
|--------|------|-----------|-------------|
| id | UUID | Identificador único | PRIMARY KEY |
| user_id | UUID | Referência ao usuário | FOREIGN KEY, UNIQUE, NOT NULL |
| name | VARCHAR(100) | Nome completo | NULLABLE |
| phone | VARCHAR(20) | Telefone | NULLABLE |
| birth_date | DATE | Data de nascimento | NULLABLE |
| spouse_name | VARCHAR(100) | Nome do cônjuge | NULLABLE |
| spouse_birth_date | DATE | Data nascimento cônjuge | NULLABLE |
| preferences_json | JSON | Preferências do usuário | NOT NULL |
| created_at | TIMESTAMP | Data de criação | NOT NULL |
| updated_at | TIMESTAMP | Data de atualização | NOT NULL |

**Estrutura do preferences_json:**
```json
{
  "notifications": {
    "email": true,
    "push": true,
    "sms": false
  },
  "suggestion_categories": {
    "anniversary": true,
    "purchase": true,
    "routine": true,
    "seasonal": true
  },
  "quiet_hours": {
    "enabled": false,
    "start": "22:00",
    "end": "08:00"
  },
  "suggestion_frequency": "normal",
  "max_daily_suggestions": 5,
  "categories_of_interest": ["finance", "health"],
  "preferred_times": {
    "morning": true,
    "afternoon": true,
    "evening": true,
    "night": true
  }
}
```

**Relacionamentos:**
- `users` (1:1) - Pertence a um usuário

---

### 3. **transactions**
Transações financeiras dos usuários.

| Coluna | Tipo | Descrição | Constraints |
|--------|------|-----------|-------------|
| id | UUID | Identificador único | PRIMARY KEY |
| user_id | UUID | Referência ao usuário | FOREIGN KEY, NOT NULL |
| amount | DECIMAL(10,2) | Valor da transação | NOT NULL |
| category | VARCHAR(50) | Categoria | NOT NULL |
| description | VARCHAR(500) | Descrição | NULLABLE |
| date | TIMESTAMP | Data da transação | NOT NULL |
| recurring | BOOLEAN | É recorrente? | DEFAULT FALSE |
| recurrence_pattern | VARCHAR(20) | Padrão de recorrência | NULLABLE |
| created_at | TIMESTAMP | Data de criação | NOT NULL |
| updated_at | TIMESTAMP | Data de atualização | NOT NULL |

**Valores de recurrence_pattern:**
- `daily`, `weekly`, `monthly`, `yearly`

**Relacionamentos:**
- `users` (N:1) - Pertence a um usuário
- `suggestions` (1:N) - Uma transação pode gerar sugestões

---

### 4. **suggestions**
Sugestões geradas pelo sistema para os usuários.

| Coluna | Tipo | Descrição | Constraints |
|--------|------|-----------|-------------|
| id | UUID | Identificador único | PRIMARY KEY |
| user_id | UUID | Referência ao usuário | FOREIGN KEY, NOT NULL |
| type | VARCHAR(50) | Tipo de sugestão | NOT NULL |
| content | TEXT | Conteúdo da sugestão | NOT NULL |
| category | VARCHAR(50) | Categoria | NOT NULL |
| priority | VARCHAR(20) | Prioridade | NOT NULL |
| status | VARCHAR(20) | Status atual | NOT NULL |
| scheduled_date | DATE | Data agendada | NULLABLE |
| metadata_json | JSON | Dados adicionais | NULLABLE |
| transaction_id | UUID | Transação relacionada | FOREIGN KEY, NULLABLE |
| created_at | TIMESTAMP | Data de criação | NOT NULL |
| updated_at | TIMESTAMP | Data de atualização | NOT NULL |

**Valores de type:**
- `anniversary`, `purchase`, `routine`, `seasonal`, `financial`

**Valores de priority:**
- `low`, `medium`, `high`, `urgent`

**Valores de status:**
- `pending`, `accepted`, `rejected`, `snoozed`, `executed`, `expired`

**Relacionamentos:**
- `users` (N:1) - Pertence a um usuário
- `transactions` (N:1) - Pode estar relacionada a uma transação
- `interactions` (1:N) - Uma sugestão tem várias interações

---

### 5. **interactions**
Interações dos usuários com as sugestões.

| Coluna | Tipo | Descrição | Constraints |
|--------|------|-----------|-------------|
| id | UUID | Identificador único | PRIMARY KEY |
| user_id | UUID | Referência ao usuário | FOREIGN KEY, NOT NULL |
| suggestion_id | UUID | Referência à sugestão | FOREIGN KEY, NOT NULL |
| action | VARCHAR(20) | Ação realizada | NOT NULL |
| feedback | TEXT | Feedback do usuário | NULLABLE |
| snooze_hours | INTEGER | Horas para adiar | NULLABLE |
| timestamp | TIMESTAMP | Momento da interação | NOT NULL |

**Valores de action:**
- `viewed`, `accepted`, `rejected`, `snoozed`, `executed`

**Relacionamentos:**
- `users` (N:1) - Pertence a um usuário
- `suggestions` (N:1) - Refere-se a uma sugestão

---

## Diagrama de Relacionamentos

```
┌─────────────┐
│   users     │
│─────────────│
│ id (PK)     │
│ username    │
│ email       │
│ ...         │
└─────────────┘
       │
       │ 1:1
       │
┌─────────────┐      ┌──────────────┐      ┌───────────────┐
│  profiles   │      │ transactions │      │  suggestions  │
│─────────────│      │──────────────│      │───────────────│
│ id (PK)     │      │ id (PK)      │      │ id (PK)       │
│ user_id (FK)│      │ user_id (FK) │      │ user_id (FK)  │
│ name        │      │ amount       │      │ type          │
│ ...         │      │ category     │      │ content       │
└─────────────┘      │ ...          │      │ transaction_id│
                     └──────────────┘      │    (FK)       │
                                           │ ...           │
                                           └───────────────┘
                                                    │
                                                    │ 1:N
                                                    │
                                           ┌───────────────┐
                                           │ interactions  │
                                           │───────────────│
                                           │ id (PK)       │
                                           │ user_id (FK)  │
                                           │ suggestion_id │
                                           │    (FK)       │
                                           │ action        │
                                           │ ...           │
                                           └───────────────┘
```

## Índices Recomendados

1. **users**
   - `idx_users_email` (email)
   - `idx_users_username` (username)

2. **profiles**
   - `idx_profiles_user_id` (user_id) - UNIQUE

3. **transactions**
   - `idx_transactions_user_id` (user_id)
   - `idx_transactions_date` (date)
   - `idx_transactions_category` (category)

4. **suggestions**
   - `idx_suggestions_user_id` (user_id)
   - `idx_suggestions_status` (status)
   - `idx_suggestions_scheduled_date` (scheduled_date)
   - `idx_suggestions_transaction_id` (transaction_id)

5. **interactions**
   - `idx_interactions_user_id` (user_id)
   - `idx_interactions_suggestion_id` (suggestion_id)
   - `idx_interactions_timestamp` (timestamp)

## Notas Importantes

1. **UUIDs**: Todos os IDs são UUIDs para garantir unicidade global
2. **Timestamps**: Todas as tabelas têm `created_at` e `updated_at` (exceto interactions que só tem timestamp)
3. **JSON Fields**: `preferences_json` e `metadata_json` permitem flexibilidade para dados não estruturados
4. **Soft Delete**: Não implementado - registros são mantidos com status apropriado
5. **Cascading**: Deleção de usuário remove todos os registros relacionados (CASCADE)