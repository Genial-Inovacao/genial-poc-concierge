# 🚀 Guia Rápido - LLM no AI Concierge

## 1. Instalar Dependências

```bash
pip install httpx==0.28.1
# ou
pip install -r requirements.txt
```

## 2. Configurar API Key

### Opção A: Criar arquivo .env (recomendado)
```bash
cp .env.example .env
```

Edite `.env` e adicione sua chave:
```env
ANTHROPIC_API_KEY="sk-ant-api03-..."  # Sua chave real aqui
```

### Opção B: Variável de ambiente
```bash
export ANTHROPIC_API_KEY="sk-ant-api03-..."
```

## 3. Iniciar o Servidor

```bash
uvicorn app.main:app --reload
```

## 4. Testar LLM

### Teste Básico
```bash
python test_llm_suggestions.py
```

### Gerar Sugestões para Todos os Usuários
```bash
python run_ai_analysis.py
```

### Gerar Sugestões para Um Usuário
```bash
python run_ai_analysis.py allanbruno
```

## 5. Verificar Sugestões

1. Faça login no frontend: http://localhost:5173
2. Vá para o Dashboard
3. As novas sugestões aparecerão com conteúdo mais natural e personalizado

## 📊 Comparação de Sugestões

### Antes (Regras)
```
"O aniversário de Maria está chegando (15/08). Gostaria de fazer uma reserva em algum restaurante especial?"
```

### Depois (LLM)
```
"Bruno, percebi que o aniversário da Maria está chegando sexta-feira! 🎂 Como vocês adoraram o Fasano no último aniversário dela, posso garantir uma mesa para às 20h? Também notei que você costuma enviar flores da Giuliana Flores - quer que eu agende a entrega de um buquê de rosas vermelhas como no ano passado?"
```

## 🔧 Troubleshooting

### Erro: No module named 'httpx'
```bash
pip install httpx
```

### Erro: ANTHROPIC_API_KEY not configured
- Verifique se criou o arquivo `.env`
- Confirme que a chave está correta
- Reinicie o servidor após adicionar a chave

### Sugestões genéricas ou sem LLM
- Verifique se `USE_LLM_FOR_SUGGESTIONS=True` no `.env`
- Confirme que a API key é válida
- Verifique os logs do servidor para erros

## 💡 Dicas

1. **Modelo Recomendado**: Claude Sonnet 3.7 oferece o melhor equilíbrio
2. **Custos**: Cada análise usa ~1000 tokens (~$0.003)
3. **Frequência**: Configure `SUGGESTION_GENERATION_INTERVAL_HOURS` para controlar
4. **Debug**: Os logs mostram quando usa LLM vs regras

## 🔒 Segurança

- **NUNCA** commite sua API key real
- Mantenha `.env` no `.gitignore`
- Use variáveis de ambiente em produção
- A API key deve começar com `sk-ant-api03-`