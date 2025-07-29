import React, { createContext, useState, useContext, useEffect } from 'react';
import suggestionsService from '../services/suggestions';
import analyticsService from '../services/analytics';

const AppContext = createContext({});

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};

export const AppProvider = ({ children }) => {
  const [suggestions, setSuggestions] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState({
    suggestions: false,
    stats: false,
  });
  const [filters, setFilters] = useState({
    status: 'pending',
    category: 'all',
    dateRange: 'upcoming',
  });

  useEffect(() => {
    loadSuggestions();
    loadStats();
  }, [filters]);

  const loadSuggestions = async () => {
    try {
      setLoading(prev => ({ ...prev, suggestions: true }));
      console.log('Loading suggestions with filters:', filters);
      const data = await suggestionsService.getSuggestions(filters);
      console.log('Suggestions response:', data);
      setSuggestions(data || []);
    } catch (err) {
      console.error('Failed to load suggestions:', err);
    } finally {
      setLoading(prev => ({ ...prev, suggestions: false }));
    }
  };

  const loadStats = async () => {
    try {
      setLoading(prev => ({ ...prev, stats: true }));
      const data = await analyticsService.getDashboardStats();
      setStats(data);
    } catch (err) {
      console.error('Failed to load stats:', err);
    } finally {
      setLoading(prev => ({ ...prev, stats: false }));
    }
  };

  const handleSuggestionAction = async (id, action, data = {}) => {
    try {
      let response;
      switch (action) {
        case 'accept':
          response = await suggestionsService.acceptSuggestion(id);
          break;
        case 'reject':
          response = await suggestionsService.rejectSuggestion(id, data.reason);
          break;
        case 'postpone':
          response = await suggestionsService.postponeSuggestion(id, data.postponeUntil);
          break;
        default:
          throw new Error('Invalid action');
      }
      
      // Atualizar lista de sugestões
      await loadSuggestions();
      await loadStats();
      
      return { success: true, data: response };
    } catch (err) {
      console.error('Failed to perform action:', err);
      return { success: false, error: err.message };
    }
  };

  const updateFilters = (newFilters) => {
    setFilters(prev => ({ ...prev, ...newFilters }));
  };

  const value = {
    suggestions,
    stats,
    loading,
    filters,
    loadSuggestions,
    loadStats,
    handleSuggestionAction,
    updateFilters,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};

export default AppContext;