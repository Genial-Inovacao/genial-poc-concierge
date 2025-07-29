# Frontend - Sistema Concierge IA

Frontend moderno e responsivo para o Sistema de Concierge de IA Proativo, desenvolvido com React, Vite e Tailwind CSS.

## Tecnologias Utilizadas

- **React 18** - Framework JavaScript para construção de interfaces
- **Vite** - Build tool rápido e moderno
- **Tailwind CSS** - Framework CSS utilitário
- **React Router v6** - Roteamento de páginas
- **Axios** - Cliente HTTP para requisições à API
- **Heroicons** - Ícones SVG otimizados
- **Context API** - Gerenciamento de estado global

## Estrutura do Projeto

```
frontend/
├── src/
│   ├── components/      # Componentes reutilizáveis
│   │   ├── auth/       # Componentes de autenticação
│   │   ├── common/     # Componentes comuns (Layout, Loading, etc)
│   │   ├── dashboard/  # Componentes do dashboard
│   │   └── suggestions/# Componentes de sugestões
│   ├── pages/          # Páginas da aplicação
│   ├── services/       # Serviços de API
│   ├── store/          # Context API e estado global
│   ├── utils/          # Utilitários e helpers
│   └── main.jsx        # Entrada da aplicação
├── public/             # Arquivos públicos
├── .env.example        # Exemplo de variáveis de ambiente
└── package.json        # Dependências e scripts
```

## Instalação e Configuração

1. **Instalar dependências:**
```bash
npm install
```

2. **Configurar variáveis de ambiente:**
```bash
cp .env.example .env
```

Edite o arquivo `.env` com as configurações corretas:
```
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=Concierge IA
```

3. **Executar em modo de desenvolvimento:**
```bash
npm run dev
```

4. **Build para produção:**
```bash
npm run build
```

## Funcionalidades Implementadas

### Autenticação
- Login com email e senha
- Registro de novos usuários
- Gerenciamento de tokens JWT
- Auto-refresh de token
- Proteção de rotas privadas

### Dashboard
- Visualização de sugestões personalizadas
- Estatísticas resumidas (dias ativo, ações executadas, taxa de aceitação, economia)
- Filtros por status, categoria e período
- Ações de aceitar, rejeitar ou adiar sugestões

### Perfil e Preferências
- Edição de dados pessoais
- Upload de foto de perfil
- Configuração de preferências de notificação
- Seleção de categorias de interesse
- Definição de horários preferenciais
- Limite diário de sugestões

### Histórico
- Visualização de todas as atividades
- Histórico de transações
- Filtros por período e tipo
- Detalhes de cada interação

## Componentes Principais

### Layout
- Navbar responsiva com menu mobile
- Navegação entre páginas
- Exibição do usuário logado

### SuggestionCard
- Exibição detalhada de sugestões
- Ícones por categoria
- Indicador de prioridade
- Botões de ação
- Modal de adiar sugestão

### StatsWidget
- Cards de estatísticas
- Ícones customizados
- Cores por tipo de métrica

## Padrões de Código

### Estado Global
Utilizamos Context API para gerenciamento de estado:
- `AuthContext`: Autenticação e dados do usuário
- `AppContext`: Sugestões, filtros e estatísticas

### Serviços de API
Todos os serviços seguem o padrão:
```javascript
const service = {
  async getItems(params) {
    const response = await api.get('/endpoint', { params });
    return response.data;
  }
};
```

### Componentes
- Componentes funcionais com hooks
- Props tipadas com destructuring
- Estados locais com useState
- Efeitos colaterais com useEffect

## Scripts Disponíveis

- `npm run dev` - Inicia servidor de desenvolvimento
- `npm run build` - Cria build de produção
- `npm run preview` - Preview da build de produção
- `npm run lint` - Executa linter (quando configurado)

## Próximos Passos

1. Implementar notificações push
2. Adicionar gráficos e visualizações avançadas
3. Criar modo escuro
4. Implementar PWA para funcionamento offline
5. Adicionar testes unitários e de integração

## Suporte

Para questões e suporte, consulte a documentação do backend ou abra uma issue no repositório.
