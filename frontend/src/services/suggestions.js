import api from './api';

const suggestionsService = {
  async getSuggestions(params = {}) {
    const response = await api.get('/suggestions', { params });
    return response.data;
  },

  async getSuggestionById(id) {
    const response = await api.get(`/suggestions/${id}`);
    return response.data;
  },

  async acceptSuggestion(id) {
    const response = await api.post(`/suggestions/${id}/interact`, {
      action: 'accept'
    });
    return response.data;
  },

  async rejectSuggestion(id, reason = '') {
    const response = await api.post(`/suggestions/${id}/interact`, {
      action: 'reject',
      feedback: reason
    });
    return response.data;
  },

  async postponeSuggestion(id, snoozeHours = 24) {
    const response = await api.post(`/suggestions/${id}/interact`, {
      action: 'snooze',
      snooze_hours: snoozeHours
    });
    return response.data;
  },

  async executeSuggestion(id) {
    const response = await api.post(`/suggestions/${id}/interact`, {
      action: 'execute'
    });
    return response.data;
  },

  async getSuggestionStats() {
    const response = await api.get('/suggestions/stats');
    return response.data;
  },
};

export default suggestionsService;