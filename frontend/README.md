# AI Concierge Frontend

Modern and responsive frontend for the AI-Powered Proactive Concierge System, built with React, Vite, and Tailwind CSS.

## Features

- 🎨 Modern UI with Tailwind CSS
- 🔐 JWT Authentication with auto-refresh
- 📱 Fully responsive design
- 🎯 Real-time AI suggestions display
- 📊 Interactive analytics dashboard
- 👤 User profile and preferences management
- 📜 Transaction and interaction history
- 🔍 Advanced filtering and search
- 🌐 Multi-language ready (Portuguese default)
- ⚡ Fast performance with Vite

## Technologies

- **React 18** - UI framework
- **Vite** - Fast build tool
- **Tailwind CSS** - Utility-first CSS framework
- **React Router v6** - Client-side routing
- **Axios** - HTTP client
- **Heroicons** - Beautiful hand-crafted SVG icons
- **Context API** - State management
- **Chart.js** - Data visualization (planned)

## Project Structure

```
frontend/
├── src/
│   ├── components/      # Reusable components
│   │   ├── auth/       # Authentication components
│   │   ├── common/     # Common components (Layout, Loading)
│   │   ├── dashboard/  # Dashboard components
│   │   ├── suggestions/# Suggestion cards and filters
│   │   ├── profile/    # Profile management
│   │   └── history/    # History views
│   ├── pages/          # Page components
│   │   ├── Login.jsx   # Login page
│   │   ├── Register.jsx# Registration page
│   │   ├── Dashboard.jsx# Main dashboard
│   │   ├── Profile.jsx # User profile
│   │   └── History.jsx # Transaction history
│   ├── services/       # API services
│   │   ├── api.js      # Axios instance
│   │   ├── auth.js     # Auth endpoints
│   │   ├── users.js    # User endpoints
│   │   ├── suggestions.js# Suggestion endpoints
│   │   └── transactions.js# Transaction endpoints
│   ├── store/          # Context providers
│   │   ├── AuthContext.jsx # Authentication state
│   │   └── AppContext.jsx  # Application state
│   ├── utils/          # Utility functions
│   │   ├── constants.js# App constants
│   │   └── helpers.js  # Helper functions
│   └── main.jsx        # App entry point
├── public/             # Static assets
├── .env.example        # Environment template
└── package.json        # Dependencies
```

## Installation

1. **Clone the repository:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Configure environment:**
```bash
cp .env.example .env
```

4. **Edit `.env` with your settings:**
```env
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=AI Concierge
VITE_APP_VERSION=1.0.0
```

5. **Start development server:**
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint (when configured)
- `npm run format` - Format code with Prettier (when configured)

## Features Overview

### Authentication
- Secure login with JWT tokens
- User registration with validation
- Automatic token refresh
- Protected routes
- Logout functionality
- Remember me option

### Dashboard
- **Suggestion Cards**: Display AI-generated suggestions with:
  - Priority indicators
  - Category icons
  - Quick actions (Accept/Reject/Snooze)
  - Detailed content view
- **Statistics Widgets**: 
  - Days active counter
  - Executed actions
  - Acceptance rate
  - Total savings
- **Advanced Filters**:
  - Status filter (Active/Accepted/Rejected)
  - Category filter
  - Time period selector

### Profile Management
- Edit personal information
- Update preferences:
  - Notification settings
  - Categories of interest
  - Preferred times
  - Daily suggestion limit
- Profile photo upload (planned)
- Special dates configuration

### History View
- Transaction history with filters
- Interaction timeline
- Detailed activity logs
- Export functionality (planned)

## Component Library

### Core Components

**Layout**
- Responsive navbar with mobile menu
- Footer with quick links
- Loading states
- Error boundaries

**SuggestionCard**
- Dynamic icons based on type
- Priority color coding
- Interaction buttons
- Snooze modal with date picker

**StatsWidget**
- Animated counters
- Trend indicators
- Custom icons
- Responsive grid

**FilterBar**
- Multi-select dropdowns
- Date range picker
- Quick presets
- Clear filters option

## State Management

### AuthContext
Manages authentication state:
- User data
- Auth tokens
- Login/logout methods
- Token refresh logic

### AppContext
Manages application state:
- Suggestions list
- Active filters
- User statistics
- Loading states
- Error handling

## API Integration

All API calls follow a consistent pattern:

```javascript
// Example service
export const suggestionService = {
  async getSuggestions(params) {
    const response = await api.get('/suggestions/', { params });
    return response.data;
  },
  
  async interactWithSuggestion(id, action, data) {
    const response = await api.post(`/suggestions/${id}/interact`, {
      action,
      ...data
    });
    return response.data;
  }
};
```

## Styling Guidelines

- Uses Tailwind CSS utility classes
- Custom color palette defined in `tailwind.config.js`
- Responsive breakpoints: sm, md, lg, xl
- Dark mode support (planned)
- Consistent spacing and typography

## Best Practices

1. **Component Structure**:
   - Functional components with hooks
   - Props destructuring
   - Clear prop types
   - Memoization where needed

2. **State Management**:
   - Local state for UI-only concerns
   - Context for shared state
   - Avoid prop drilling

3. **Performance**:
   - Lazy loading for routes
   - Image optimization
   - Code splitting
   - Debounced API calls

4. **Error Handling**:
   - Try-catch blocks for async operations
   - User-friendly error messages
   - Fallback UI components

## Development Workflow

1. **Feature Development**:
   - Create feature branch
   - Implement component
   - Add to appropriate page
   - Test responsiveness
   - Submit PR

2. **Testing**:
   - Manual testing on different devices
   - Cross-browser compatibility
   - API integration testing
   - Performance profiling

## Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Check if backend is running on port 8000
   - Verify VITE_API_URL in `.env`
   - Check CORS settings

2. **Authentication Errors**
   - Clear localStorage
   - Check token expiration
   - Verify API endpoints

3. **Styling Issues**
   - Run `npm run build` to regenerate CSS
   - Check Tailwind configuration
   - Clear browser cache

4. **Build Errors**
   - Delete `node_modules` and reinstall
   - Check Node.js version (16+)
   - Verify all dependencies

## Future Enhancements

1. **UI/UX**:
   - Dark mode toggle
   - Animation improvements
   - Accessibility features
   - Multi-language support

2. **Features**:
   - Push notifications
   - Offline support (PWA)
   - Data export
   - Advanced analytics charts

3. **Technical**:
   - Unit tests with Jest
   - E2E tests with Cypress
   - Performance monitoring
   - Error tracking

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open pull request

## License

MIT