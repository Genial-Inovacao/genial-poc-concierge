# Configuração do LLM (Claude) para Sugestões Inteligentes

## Visão Geral

O sistema AI Concierge agora suporta geração de sugestões usando Claude (Anthropic) para criar sugestões mais naturais, contextuais e personalizadas.

## Como Funciona

### Sistema Híbrido
O sistema opera em modo híbrido:
1. **Análise baseada em regras**: Para sugestões críticas e sensíveis ao tempo (aniversários, pagamentos recorrentes)
2. **Análise por LLM**: Para sugestões criativas e contextuais baseadas em padrões complexos

### Fluxo de Geração

```
Usuário
  ↓
Coleta de Contexto
  ├─ Perfil (nome, idade, preferências)
  ├─ Transações (últimos 90 dias)
  └─ Sugestões anteriores (aceitas/rejeitadas)
  ↓
Análise Híbrida
  ├─ Regras: Datas importantes sempre processadas
  └─ LLM: Análise contextual profunda
  ↓
Deduplicação e Priorização
  ↓
Sugestões Personalizadas
```

## Configuração

### 1. Obter API Key da Anthropic

1. Acesse https://console.anthropic.com/
2. Crie uma conta ou faça login
3. Vá para "API Keys"
4. Crie uma nova chave
5. Copie a chave (começa com `sk-ant-`)

### 2. Configurar o Backend

1. Copie o arquivo de exemplo:
```bash
cp .env.example .env
```

2. Edite o arquivo `.env` e adicione sua API key:
```env
ANTHROPIC_API_KEY="sk-ant-api03-..."  # Sua chave aqui
```

3. Configure o modelo (opcional):
```env
# Opções de modelo (Janeiro 2025):
LLM_MODEL="claude-opus-4-20250514"       # Opus 4 - Mais avançado
LLM_MODEL="claude-sonnet-4-20250514"     # Sonnet 4 - Muito capaz
LLM_MODEL="claude-3-7-sonnet-20250219"   # Sonnet 3.7 - RECOMENDADO (padrão)
LLM_MODEL="claude-3-5-haiku-20241022"    # Haiku 3.5 - Mais econômico
```

4. Ajuste parâmetros (opcional):
```env
LLM_MAX_TOKENS=1000        # Tamanho máximo da resposta
LLM_TEMPERATURE=0.7        # Criatividade (0.0 a 1.0)
USE_LLM_FOR_SUGGESTIONS=True  # False para usar apenas regras
```

### 3. Reiniciar o Servidor

```bash
# Parar o servidor (Ctrl+C)
# Reiniciar
uvicorn app.main:app --reload
```

## Exemplos de Sugestões

### Com Regras (Sistema Anterior)
```
"O aniversário de Maria está chegando (15/08). Gostaria de fazer uma reserva em algum restaurante especial?"
```

### Com LLM (Claude)
```
"Bruno, o aniversário da Maria está chegando dia 15! 🎉 Notei que vocês adoram o Fasano - 
já foram lá 3 vezes em datas especiais. Que tal reservar uma mesa para o jantar? 
Posso também sugerir aquela floricultura do Shopping Iguatemi onde você comprou 
o último buquê."
```

## Monitoramento

### Logs do Sistema
O sistema registra:
- Quando usa LLM vs regras
- Tempo de resposta da API
- Erros e fallbacks
- Sugestões geradas

### Verificar se está funcionando:
```python
# No backend, check logs para:
"Generated 5 new suggestions using Claude"
"Error generating LLM suggestions: [erro]"
"Falling back to rule-based suggestions"
```

## Custos

### Estimativa de Uso
- **Por usuário**: ~500-1000 tokens por análise
- **Frequência**: Configurável (padrão: a cada 6 horas)
- **Custo médio**: ~$0.002-0.005 por análise

### Modelos Disponíveis (Janeiro 2025)

#### Novos Modelos (Recomendados)
- **Claude Opus 4** (`claude-opus-4-20250514`): Mais capaz, maior custo
- **Claude Sonnet 4** (`claude-sonnet-4-20250514`): Muito capaz, custo alto
- **Claude Sonnet 3.7** (`claude-3-7-sonnet-20250219`): **RECOMENDADO** - Excelente equilíbrio
- **Claude Haiku 3.5** (`claude-3-5-haiku-20241022`): Mais rápido, menor custo

#### Comparação de Capacidades
- **Opus 4**: Para análises complexas e sugestões muito sofisticadas
- **Sonnet 3.7**: Ideal para uso diário - rápido, inteligente e econômico
- **Haiku 3.5**: Para alto volume com orçamento limitado

## Troubleshooting

### API Key não funciona
```
Error: ANTHROPIC_API_KEY not configured
```
- Verifique se a chave está no `.env`
- Confirme que não há espaços extras
- Teste se o servidor carregou o .env

### Timeout ou erro de rede
```
Error calling Claude API: timeout
```
- Verifique conexão com internet
- API da Anthropic pode estar lenta
- Sistema automaticamente usa regras como fallback

### Sugestões genéricas
- Ajuste `LLM_TEMPERATURE` para 0.8-0.9
- Verifique se há dados suficientes do usuário
- Mais transações = melhor contexto

## Segurança

### Dados Enviados
O sistema envia apenas:
- Nome e idade (sem documentos)
- Padrões de transação (sem detalhes bancários)
- Preferências gerais
- Histórico de sugestões

### Dados NÃO Enviados
- Senhas ou tokens
- Números de cartão
- Documentos pessoais
- Dados bancários completos

## Desabilitar LLM

Para voltar ao sistema baseado em regras:
```env
USE_LLM_FOR_SUGGESTIONS=False
```

Ou remova a API key:
```env
ANTHROPIC_API_KEY=""
```