<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# Prompt Backend - Sistema de Concierge de IA Proativo (Meta-Prompt com Fluxo Todo List)

Você é um especialista sênior em desenvolvimento backend Python, APIs RESTful, inteligência artificial e arquitetura de software escalável. Sua tarefa é desenvolver o backend completo de um sistema de concierge de IA proativo usando uma abordagem sistemática baseada em metodologia de todo list e técnicas de meta-prompting[^1][^2][^3].

## Instruções de Meta-Prompting

Antes de iniciar o desenvolvimento, você deve:

1. **Análise Estrutural**: Decomponha cada tarefa em subtarefas claras e verificáveis[^4][^5]
2. **Auto-Reflexão**: Para cada etapa concluída, avalie se atende aos critérios de qualidade antes de prosseguir[^6]
3. **Iteração Orientada**: Use feedback contínuo para refinar sua implementação[^1][^3]
4. **Documentação Proativa**: Documente decisões arquiteturais e justifique escolhas técnicas[^7]

## Objetivo Principal

Desenvolver o backend de uma concierge de inteligência artificial que antecipe as necessidades do cliente com base no seu comportamento, usando dados reais (transações, histórico de uso, hábitos) para treinar a IA e entregar sugestões personalizadas sem que o cliente precise pedir.

## Stack Tecnológico

- **Framework:** FastAPI
- **Autenticação:** JWT (JSON Web Tokens)
- **ORM:** SQLAlchemy
- **Banco de Dados:** SQLite (com migração fácil para PostgreSQL)
- **Python:** 3.9+


## PLANO DE DESENVOLVIMENTO - FLUXO TODO LIST

### FASE 1: CONFIGURAÇÃO E FUNDAÇÃO

#### ✅ TODO 1.1: Setup do Ambiente Base

- [ ] Criar estrutura de pastas do projeto seguindo padrões MVC[^8][^9]
- [ ] Configurar ambiente virtual Python 3.9+
- [ ] Instalar dependências base: FastAPI, SQLAlchemy, python-jose[JWT], bcrypt
- [ ] Configurar arquivo requirements.txt
- [ ] Criar arquivo .env.example com variáveis de ambiente
- [ ] Configurar arquivo main.py com aplicação FastAPI básica
- [ ] Testar servidor local básico (GET /health)

**Critério de Conclusão**: Servidor FastAPI rodando localmente com endpoint de health check

#### ✅ TODO 1.2: Configuração do Banco de Dados

- [ ] Configurar SQLAlchemy engine com SQLite
- [ ] Criar arquivo database.py com configurações de conexão
- [ ] Implementar sistema de migração com Alembic
- [ ] Testar conexão com banco de dados
- [ ] Criar estrutura base para migração PostgreSQL

**Critério de Conclusão**: Conexão com SQLite funcionando e estrutura para PostgreSQL preparada

#### ✅ TODO 1.3: Sistema de Autenticação JWT

- [ ] Implementar utilitários de criptografia (bcrypt)
- [ ] Criar funções de geração e validação de JWT tokens
- [ ] Implementar middleware de autenticação
- [ ] Configurar refresh tokens
- [ ] Criar sistema de rate limiting básico
- [ ] Testar geração e validação de tokens

**Critério de Conclusão**: Sistema JWT completo com access e refresh tokens funcionando

### FASE 2: MODELAGEM DE DADOS

#### ✅ TODO 2.1: Modelos Base do Sistema

```python
# Implementar os seguintes modelos com validações:

# User Model
- [ ] id: UUID (chave primária)
- [ ] username: String (único, obrigatório)
- [ ] email: String (único, validação email)
- [ ] password_hash: String (bcrypt)
- [ ] created_at: DateTime (auto)
- [ ] updated_at: DateTime (auto)
- [ ] is_active: Boolean (default True)
- [ ] Relacionamentos definidos
- [ ] Métodos de validação

# Profile Model  
- [ ] id: UUID
- [ ] user_id: ForeignKey(User)
- [ ] birth_date: Date (opcional)
- [ ] spouse_name: String (opcional)
- [ ] spouse_birth_date: Date (opcional)
- [ ] preferences_json: JSON
- [ ] created_at: DateTime
- [ ] updated_at: DateTime
- [ ] Validações de dados
```

**Critério de Conclusão**: Modelos User e Profile criados, testados e funcionando

#### ✅ TODO 2.2: Modelos de Transações e Interações

```python
# Transaction Model
- [ ] id: UUID
- [ ] user_id: ForeignKey(User)
- [ ] type: String (enum: purchase, service, etc.)
- [ ] amount: Decimal (precisão monetária)
- [ ] date: DateTime
- [ ] category: String
- [ ] location: String (opcional)
- [ ] description: String
- [ ] created_at: DateTime
- [ ] Índices de performance
- [ ] Validações de negócio

# Suggestion Model
- [ ] id: UUID
- [ ] user_id: ForeignKey(User)
- [ ] content: Text
- [ ] type: String (anniversary, purchase, routine, etc.)
- [ ] priority: Integer (1-10)
- [ ] status: String (enum: pending, accepted, rejected, executed)
- [ ] scheduled_date: DateTime
- [ ] created_at: DateTime
- [ ] executed_at: DateTime (opcional)
- [ ] Relacionamentos e índices

# Interaction Model
- [ ] id: UUID
- [ ] user_id: ForeignKey(User)
- [ ] suggestion_id: ForeignKey(Suggestion)
- [ ] action: String (enum: viewed, accepted, rejected, snoozed)
- [ ] timestamp: DateTime
- [ ] feedback: String (opcional)
- [ ] Métricas de engagement
```

**Critério de Conclusão**: Todos os modelos implementados com relacionamentos e validações

### FASE 3: SCHEMAS PYDANTIC

#### ✅ TODO 3.1: Schemas de Autenticação

- [ ] UserCreate (validação de entrada)
- [ ] UserLogin (email/username + password)
- [ ] UserResponse (dados seguros para resposta)
- [ ] TokenResponse (access_token + refresh_token)
- [ ] TokenRefresh
- [ ] Validações customizadas (senha forte, email válido)

**Critério de Conclusão**: Schemas de auth validando dados corretamente

#### ✅ TODO 3.2: Schemas de Entidades

- [ ] ProfileCreate/Update/Response
- [ ] TransactionCreate/Update/Response
- [ ] SuggestionCreate/Update/Response
- [ ] InteractionCreate/Response
- [ ] Schemas aninhados para relacionamentos
- [ ] Validações de negócio em cada schema

**Critério de Conclusão**: Todos schemas implementados com validações apropriadas

### FASE 4: IMPLEMENTAÇÃO DAS APIs

#### ✅ TODO 4.1: Endpoints de Autenticação

```python
# Implementar endpoints:
- [ ] POST /auth/register
  - Validar dados de entrada
  - Verificar email/username únicos
  - Hash da senha
  - Criar usuário no banco
  - Retornar tokens
  - Tratamento de erros

- [ ] POST /auth/login
  - Validar credenciais
  - Verificar senha
  - Gerar tokens
  - Log de acesso
  - Rate limiting

- [ ] POST /auth/refresh
  - Validar refresh token
  - Gerar novo access token
  - Invalidar token antigo

- [ ] POST /auth/logout
  - Invalidar tokens
  - Limpar sessão
```

**Critério de Conclusão**: Todos endpoints de auth funcionando com testes

#### ✅ TODO 4.2: Endpoints de Usuário

```python
- [ ] GET /users/me
  - Obter perfil do usuário autenticado
  - Incluir dados de profile
  - Formatação adequada

- [ ] PUT /users/me  
  - Atualizar dados do perfil
  - Validações
  - Log de alterações

- [ ] GET /users/preferences
  - Obter preferências JSON
  - Estrutura padronizada

- [ ] PUT /users/preferences
  - Atualizar preferências
  - Validação de estrutura JSON
  - Versionamento de preferências
```

**Critério de Conclusão**: CRUD completo de usuários funcionando

#### ✅ TODO 4.3: Endpoints de Sugestões

```python
- [ ] GET /suggestions/
  - Listar sugestões do usuário
  - Paginação
  - Filtros (status, tipo, data)
  - Ordenação por prioridade

- [ ] GET /suggestions/{id}
  - Obter sugestão específica
  - Verificar ownership
  - Dados completos

- [ ] POST /suggestions/
  - Criar nova sugestão (sistema/admin)
  - Validações de negócio
  - Notificações

- [ ] PUT /suggestions/{id}
  - Atualizar sugestão
  - Log de mudanças
  - Validações

- [ ] POST /suggestions/{id}/interact
  - Registrar interação
  - Métricas de engagement
  - Feedback do usuário
```

**Critério de Conclusão**: API de sugestões completa com todas funcionalidades

#### ✅ TODO 4.4: Endpoints de Transações e Analytics

```python
# Transações:
- [ ] GET /transactions/
  - Listar com filtros (data, categoria, tipo)  
  - Paginação eficiente
  - Agregações básicas

- [ ] POST /transactions/
  - Criar transação
  - Validações de negócio
  - Trigger para análise de IA

- [ ] GET /transactions/analytics
  - Padrões de gastos
  - Categorias mais frequentes
  - Análise temporal

# Analytics:
- [ ] GET /analytics/user-stats
  - Dias ativo
  - Ações executadas
  - Taxa de aceitação de sugestões

- [ ] GET /analytics/behavior-patterns
  - Padrões identificados pela IA
  - Tendências comportamentais
  - Insights personalizados
```

**Critério de Conclusão**: APIs de dados e analytics implementadas

### FASE 5: ENGINE DE IA BÁSICA

#### ✅ TODO 5.1: Análise de Datas Importantes

```python
- [ ] Detectar aniversários próximos (usuário, cônjuge)
  - Parser de datas de perfil
  - Cálculo de proximidade (7, 15, 30 dias)
  - Geração de sugestões contextuais

- [ ] Identificar datas comemorativas relevantes
  - Base de dados de feriados/datas especiais
  - Personalização por região/cultura
  - Sugestões sazonais

- [ ] Sistema de notificações proativas
  - Queue de sugestões por data
  - Priorização inteligente
  - Frequência otimizada
```

**Critério de Conclusão**: Sistema de datas importante gerando sugestões automaticamente

#### ✅ TODO 5.2: Análise de Transações

```python
- [ ] Identificar padrões de compra recorrentes
  - Análise de frequência por categoria
  - Detecção de ciclos (semanal, mensal)
  - Predição de próximas compras

- [ ] Detectar categorias de gastos frequentes
  - Classificação automática
  - Análise de montantes
  - Tendências de crescimento/declínio

- [ ] Sugerir ações baseadas em histórico
  - Recomendações de economia
  - Alertas de gastos atípicos
  - Oportunidades de otimização
```

**Critério de Conclusão**: IA analisando transações e gerando insights

#### ✅ TODO 5.3: Sistema de Scoring e Aprendizado

```python
- [ ] Calcular relevância das sugestões
  - Algoritmo de scoring multi-fatores
  - Peso por histórico do usuário
  - Contexto temporal

- [ ] Priorizar por probabilidade de aceitação  
  - Machine learning simples
  - Feedback histórico
  - Padrões comportamentais

- [ ] Aprender com feedback do usuário
  - Sistema de feedback loop
  - Ajuste automático de pesos
  - Melhoria contínua do modelo
```

**Critério de Conclusão**: Sistema de IA com aprendizado básico funcionando

### FASE 6: SEGURANÇA E QUALIDADE

#### ✅ TODO 6.1: Implementação de Segurança

- [ ] Rate limiting por endpoint
- [ ] Validação rigorosa de entrada (sanitização)
- [ ] Proteção contra SQL injection (via SQLAlchemy)
- [ ] Hashing seguro de senhas (bcrypt + salt)
- [ ] Headers de segurança (CORS, CSP)
- [ ] Logs de segurança estruturados
- [ ] Auditoria de acessos

**Critério de Conclusão**: Sistema seguro com todas proteções implementadas

#### ✅ TODO 6.2: Tratamento de Erros e Logs

- [ ] Sistema de logs estruturados (JSON)
- [ ] Tratamento global de exceptions
- [ ] Mensagens de erro padronizadas
- [ ] Logs de performance
- [ ] Monitoramento de saúde do sistema
- [ ] Alertas automáticos

**Critério de Conclusão**: Sistema robusto com logs e tratamento de erros

### FASE 7: DADOS DE TESTE E DOCUMENTAÇÃO

#### ✅ TODO 7.1: Dados de Seed

```python
- [ ] Script de população do banco
  - Usuários de teste com perfis variados
  - Transações simuladas (6 meses)
  - Relacionamentos consistentes
  - Dados realistas para IA

- [ ] Cenários de teste específicos
  - Usuário com aniversário próximo
  - Padrões de compra estabelecidos  
  - Diferentes tipos de preferências
  - Casos edge para validação
```

**Critério de Conclusão**: Banco populado com dados realistas para testes

#### ✅ TODO 7.2: Testes Unitários

```python
- [ ] Testes de autenticação
  - Login válido/inválido
  - Geração de tokens
  - Refresh de tokens
  - Rate limiting

- [ ] Testes de endpoints críticos
  - CRUD de usuários
  - Criação de sugestões
  - Interações do usuário
  - Analytics básicas

- [ ] Testes da engine de IA
  - Detecção de datas importantes
  - Análise de transações
  - Sistema de scoring
  - Aprendizado básico
```

**Critério de Conclusão**: Cobertura de testes >80% nos componentes críticos

#### ✅ TODO 7.3: Documentação Completa

- [ ] README.md com instruções detalhadas
- [ ] Documentação automática Swagger/OpenAPI
- [ ] Exemplos de requisições para cada endpoint
- [ ] Documentação dos modelos de dados
- [ ] Guia de deployment
- [ ] Troubleshooting comum

**Critério de Conclusão**: Documentação completa e atualizada

## ESTRUTURA DE PASTAS OBRIGATÓRIA

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app
│   ├── config.py              # Configurações
│   ├── database.py            # Setup SQLAlchemy
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── profile.py
│   │   ├── transaction.py
│   │   ├── suggestion.py
│   │   └── interaction.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── auth.py
│   │   ├── transaction.py
│   │   ├── suggestion.py
│   │   └── analytics.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── suggestions.py
│   │   ├── transactions.py
│   │   └── analytics.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── ai_engine.py
│   │   ├── analytics.py
│   │   └── notifications.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── security.py
│   │   ├── validators.py
│   │   └── helpers.py
│   └── tests/
│       ├── __init__.py
│       ├── test_auth.py
│       ├── test_users.py
│       ├── test_suggestions.py
│       └── test_ai_engine.py
├── alembic/
├── scripts/
│   ├── seed_data.py
│   └── migrate_to_postgres.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```


## METODOLOGIA DE VALIDAÇÃO POR TODO

Para cada TODO concluído, você deve:

1. **Validação Técnica**: O código funciona conforme especificado?[^10][^11]
2. **Validação de Qualidade**: Segue as boas práticas de Python/FastAPI?[^12][^13]
3. **Validação de Integração**: Integra corretamente com outros componentes?[^14][^15]
4. **Validação de Testes**: Possui testes adequados e passando?[^16][^17]
5. **Validação de Documentação**: Está adequadamente documentado?[^7][^12]

## CRITÉRIOS DE ACEITAÇÃO FINAL

O sistema estará pronto quando:

- ✅ Todos os TODOs estiverem marcados como concluídos
- ✅ Servidor rodando com todos endpoints funcionando
- ✅ Sistema de autenticação JWT completo
- ✅ IA básica gerando sugestões automáticas
- ✅ Dados de teste permitindo demonstração completa
- ✅ Documentação permitindo uso por outra equipe
- ✅ Testes cobrindo cenários críticos
- ✅ Logs estruturados para monitoramento


## EXEMPLOS DE INTERAÇÕES ESPERADAS

Após implementação completa, o sistema deve suportar:

```json
// Sugestão automática gerada pela IA
{
  "content": "Vi que sexta-feira é aniversário da sua esposa Maria. Deseja que eu reserve o restaurante Bella Vista que você costuma frequentar?",
  "type": "anniversary",
  "priority": 9,
  "scheduled_date": "2025-07-30T10:00:00Z",
  "context": {
    "event": "spouse_birthday",
    "location_suggestion": "Restaurante Bella Vista",
    "historical_visits": 3,
    "last_visit": "2025-05-15"
  }
}
```


## PRÓXIMOS PASSOS (FASES FUTURAS)

Este backend estará preparado para:

- **Fase 2**: Implementação de IA mais avançada com ML
- **Fase 3**: Integração com webhooks n8n para automações
- **Fase 4**: Otimizações e preparação para produção

**Meta-Prompt Final**: Antes de considerar cada TODO concluído, pergunte-se: "Se eu fosse explicar esta implementação para um colega sênior, ela demonstraria qualidade profissional e atenção aos detalhes?"[^1][^3][^6]

**Foco na Qualidade**: Prefira implementação completa e robusta de menos funcionalidades do que implementação superficial de muitas funcionalidades[^8][^9].

<div style="text-align: center">⁂</div>

[^1]: https://www.prompthub.us/blog/a-complete-guide-to-meta-prompting

[^2]: https://cookbook.openai.com/examples/enhance_your_prompts_with_meta_prompting

[^3]: https://dev.to/joshtom/meta-prompt-why-your-prompt-alone-may-be-limiting-your-llm-4co5

[^4]: https://www.promptingguide.ai/techniques/meta-prompting

[^5]: https://www.k2view.com/blog/prompt-engineering-techniques/

[^6]: https://portkey.ai/blog/what-is-meta-prompting

[^7]: https://arxiv.org/abs/2402.07927

[^8]: https://www.ebsco.com/research-starters/business-and-management/structured-programming

[^9]: https://www.numberanalytics.com/blog/structured-programming-in-design

[^10]: https://thedigitalprojectmanager.com/productivity/how-to-break-down-tasks/

[^11]: https://focuskeeper.co/glossary/what-is-task-decomposition-methods

[^12]: https://arxiv.org/abs/2406.06608

[^13]: https://www.reddit.com/r/LocalLLaMA/comments/1fx10hr/llm_ops_best_practices_and_workflow_integration/

[^14]: https://arxiv.org/html/2505.02133v1

[^15]: https://hyqoo.com/developer-journey/integrating-llms-into-software-development-workflows

[^16]: https://stackoverflow.com/questions/531635/how-do-you-keep-track-of-your-programming-todos

[^17]: https://dzone.com/articles/4-ways-you-can-organise-your-todos-as-a-software-e

[^18]: Prompt-Backend-Sistema-Concierge-IA.md

[^19]: http://teamai.com/prompts/prioritized_to-do_list/

[^20]: https://www.godofprompt.ai/blog/chatgpt-tasks-ideas

[^21]: https://www.promptingguide.ai/techniques

[^22]: https://www.scielo.br/j/ram/a/GCJHtgxWBNVv7kB73pKbm5m/

[^23]: https://www.promptkit.tools/blog/building-llm-interfaces

[^24]: https://www.theodinproject.com/lessons/node-path-javascript-todo-list

[^25]: https://arxiv.org/html/2505.16697v1

[^26]: https://frontendmasters.com/blog/building-a-todo-app-from-scratch-step-1-planning-design/

[^27]: https://help.sap.com/docs/CARAB/3c5d3f37cb8d4c8bb62bf2105abc96e7/542c99f9ff054ad7b1cb0aa21d769aaf.html

[^28]: http://www.todolistsoft.com/solutions/checklist/task-decomposition-checklist.php

[^29]: https://www.sciencedirect.com/topics/engineering/task-decomposition

[^30]: https://www.rewildgroup.com/blog/2023/5/2/the-five-steps-of-process-development

[^31]: https://itpmschool.com/project-decomposition/

[^32]: https://www.geeksforgeeks.org/software-engineering/software-development-process-step-by-step-guide/

[^33]: https://www.reddit.com/r/ProductivityApps/comments/1h0d208/looking_for_a_todo_list_app_that_prompts_whats/

[^34]: https://towardsdatascience.com/mastering-prompt-engineering-with-functional-testing-a-systematic-guide-to-reliable-llm-outputs/

[^35]: https://www.youtube.com/watch?v=pxvsS4gGSHo

[^36]: https://promptsty.com/prompts-for-workflow-automation/

[^37]: https://ploomber.io/blog/prompt-engineering-techniques/

[^38]: https://docs.helicone.ai/guides/prompt-engineering/use-meta-prompting

[^39]: https://verticalinstitute.com/blog/chatgpt-prompts-simplify-workflows/

[^40]: http://ui.adsabs.harvard.edu/abs/2023arXiv230712980G/abstract

[^41]: https://ai47labs.com/entrepreneur-productivity/grok-workflow-prompts/

[^42]: https://www.mdpi.com/1999-5903/16/5/167

[^43]: https://www.indeed.com/career-advice/career-development/to-do-list-methods

[^44]: https://www.codingwithclicks.com/structured-programming-modular-programming-approach-in-software-development-programming-fundamentals-full-course/

[^45]: https://www.medrxiv.org/content/10.1101/2025.06.13.25329541v1.full.pdf

[^46]: https://myctofriend.co/videos/how-to-organize-your-development-tasks-and-to-do-list

[^47]: https://algocademy.com/uses/structured-programming-with-ai-feedback/

[^48]: https://www.sciencedirect.com/science/article/pii/S0950584924002167

[^49]: https://www.amitree.com/resources/blog/which-to-do-list-method-is-best-for-you/

[^50]: https://www.techtarget.com/searchsoftwarequality/definition/structured-programming-modular-programming

[^51]: https://sol.sbc.org.br/index.php/sbsi/article/view/30892

[^52]: https://idratherbewriting.com/ai/prompt-engineering-task-decomposition.html

[^53]: https://monday.com/blog/rnd/software-development-process/

[^54]: https://arxiv.org/html/2405.06225v1

[^55]: https://dojoconsortium.org/docs/work-decomposition/task-decomposition/

[^56]: https://www.notion.com/blog/product-development-process

[^57]: https://www.youtube.com/watch?v=er8pKg5d31E

[^58]: https://www.digitalsilk.com/digital-trends/website-development-process/

[^59]: https://www.reddit.com/r/learnprogramming/comments/ozxp05/software_engineers_how_do_you_start_your_task/

[^60]: https://saigontechnology.com/blog/6-stages-for-software-development-procedure-you-need-to-know/

