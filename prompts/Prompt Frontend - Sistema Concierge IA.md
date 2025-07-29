# Prompt Frontend - Sistema de Concierge de IA Proativo

Você é um especialista em desenvolvimento frontend, UX/UI design, e criação de interfaces intuitivas e responsivas. Sua tarefa é desenvolver o frontend completo de um sistema de concierge de IA proativo que se integre perfeitamente com o backend FastAPI.

## Objetivo Principal

Criar uma interface de usuário moderna, intuitiva e responsiva que permita aos usuários interagir com um sistema de concierge de IA proativo. A interface deve exibir sugestões personalizadas baseadas em comportamento, permitir gerenciamento de perfil e preferências, e mostrar estatísticas de uso de forma clara e atrativa.

## Stack Tecnológico Recomendado

- **Framework:** React.js ou Vue.js ou Next.js
- **Gerenciamento de Estado:** Context API, Redux ou Pinia
- **Estilização:** Tailwind CSS ou Material-UI ou Ant Design
- **HTTP Client:** Axios ou Fetch API
- **Autenticação:** JWT com interceptors
- **Build Tool:** Vite ou Create React App

## Requisitos da Fase 1

### 1. Configuração do Projeto

- Setup completo do framework escolhido
- Configuração de roteamento (React Router, Vue Router, etc.)
- Estrutura de pastas organizada e escalável
- Configuração de variáveis de ambiente
- Setup de ferramentas de desenvolvimento (ESLint, Prettier)

### 2. Sistema de Autenticação

Implementar fluxo completo de autenticação:

- **Tela de Login:**
  - Formulário com validação (email/username e senha)
  - Mensagens de erro claras
  - Opção "Lembrar de mim"
  - Link para cadastro

- **Tela de Cadastro:**
  - Formulário com campos: nome, email, senha, confirmar senha
  - Validação em tempo real
  - Indicador de força da senha
  - Termos de uso (checkbox)

- **Gerenciamento de Tokens:**
  - Armazenamento seguro de JWT (localStorage/sessionStorage)
  - Refresh token automático
  - Interceptors para adicionar token nas requisições
  - Redirecionamento em caso de token expirado

### 3. Dashboard Principal

Criar dashboard com as seguintes seções:

- **Header:**
  - Logo do sistema
  - Saudação personalizada ("Olá, [Nome]")
  - Menu de navegação
  - Botão de logout

- **Área de Sugestões:**
  - Cards de sugestões organizados por prioridade
  - Cada card deve mostrar:
    - Ícone representativo do tipo de sugestão
    - Título da sugestão
    - Descrição detalhada
    - Data/hora relevante
    - Botões de ação (Aceitar, Rejeitar, Adiar)
  - Animações suaves para interações
  - Filtros por tipo de sugestão

- **Estatísticas Resumidas:**
  - Dias ativo na plataforma
  - Total de ações executadas
  - Taxa de aceitação de sugestões
  - Economia gerada (se aplicável)

### 4. Páginas e Componentes

#### Página de Perfil
- Visualização e edição de dados pessoais
- Upload de foto de perfil
- Informações sobre cônjuge/família
- Datas importantes (aniversários, etc.)

#### Página de Preferências
- Configurações de notificações
- Categorias de interesse
- Horários preferenciais para sugestões
- Limite de sugestões diárias

#### Página de Histórico
- Lista de todas as interações passadas
- Filtros por data, tipo, status
- Detalhes de cada sugestão e ação tomada
- Gráficos de atividade ao longo do tempo

#### Componentes Reutilizáveis
- `SuggestionCard`: Card individual de sugestão
- `UserStats`: Widget de estatísticas
- `LoadingSpinner`: Indicador de carregamento
- `ErrorMessage`: Componente de erro padronizado
- `ConfirmDialog`: Modal de confirmação
- `DatePicker`: Seletor de data customizado

### 5. Integração com Backend

Implementar serviços para todas as APIs:

```javascript
// Exemplo de estrutura de serviços
services/
├── api.js          // Configuração base do Axios
├── auth.js         // Login, registro, refresh token
├── user.js         // Perfil, preferências
├── suggestions.js  // CRUD de sugestões
├── analytics.js    // Estatísticas e análises
└── transactions.js // Histórico de transações
```

### 6. UX/UI Design

- **Design Responsivo:**
  - Mobile-first approach
  - Breakpoints para tablet e desktop
  - Menu hambúrguer para mobile

- **Tema Visual:**
  - Paleta de cores consistente
  - Modo claro como padrão
  - Tipografia legível
  - Ícones intuitivos (Font Awesome, Material Icons)

- **Feedback Visual:**
  - Loading states para todas as operações
  - Mensagens de sucesso/erro
  - Animações suaves
  - Skeleton screens durante carregamento

- **Acessibilidade:**
  - Alt text em imagens
  - Navegação por teclado
  - Contraste adequado
  - ARIA labels

### 7. Gerenciamento de Estado

Implementar gestão eficiente de estado global:

- Estado de autenticação (usuário logado, tokens)
- Lista de sugestões e filtros ativos
- Preferências do usuário
- Cache de dados para melhor performance
- Estado de loading/erro por módulo

### 8. Otimizações de Performance

- Lazy loading de componentes
- Memoização de componentes pesados
- Virtualização de listas longas
- Otimização de imagens
- Code splitting por rotas

## Estrutura de Pastas Sugerida

```
frontend/
├── public/
│   ├── index.html
│   └── assets/
├── src/
│   ├── components/
│   │   ├── common/
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── profile/
│   │   └── suggestions/
│   ├── pages/
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── Dashboard.jsx
│   │   ├── Profile.jsx
│   │   └── History.jsx
│   ├── services/
│   │   ├── api.js
│   │   └── ...
│   ├── store/
│   │   ├── auth.js
│   │   └── ...
│   ├── utils/
│   │   ├── validators.js
│   │   └── formatters.js
│   ├── styles/
│   │   └── global.css
│   ├── App.jsx
│   └── main.jsx
├── .env.example
├── package.json
└── README.md
```

## Fluxo de Usuário Esperado

1. **Primeiro Acesso:**
   - Usuário acessa a aplicação
   - É direcionado para tela de login
   - Pode criar nova conta
   - Após login, é direcionado ao dashboard

2. **Uso Diário:**
   - Dashboard mostra sugestões do dia
   - Usuário interage com sugestões
   - Pode verificar histórico e estatísticas
   - Ajusta preferências conforme necessário

3. **Interação com Sugestões:**
   - Visualiza detalhes da sugestão
   - Aceita/Rejeita/Adia
   - Vê confirmação da ação
   - Sugestão atualiza status em tempo real

## Resultado Esperado

Uma interface moderna e intuitiva que:
- Proporcione experiência fluida e agradável
- Mostre sugestões de forma clara e acionável
- Permita fácil gerenciamento de preferências
- Exiba estatísticas de forma visual e compreensível
- Funcione perfeitamente em dispositivos móveis e desktop
- Integre-se sem problemas com o backend FastAPI

## Próximos Passos (Fases Futuras)

Após completar a Fase 1, o frontend estará pronto para:
- Notificações push e em tempo real (Fase 2)
- Visualizações avançadas de dados e gráficos (Fase 2)
- Integração com PWA para funcionamento offline (Fase 3)
- Temas personalizáveis e modo escuro (Fase 4)

Foque em criar uma experiência de usuário excepcional que torne o uso da IA concierge natural e prazeroso.