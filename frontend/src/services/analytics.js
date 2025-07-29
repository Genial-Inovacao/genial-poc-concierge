import api from './api';

const analyticsService = {
  async getDashboardStats() {
    const response = await api.get('/suggestions/stats');
    return response.data;
  },

  async getBehaviorPatterns() {
    const response = await api.get('/analytics/behavior-patterns');
    return response.data;
  },

  async getEngagementMetrics() {
    const response = await api.get('/analytics/engagement');
    return response.data;
  },

  async getActivityHistory(params = {}) {
    const response = await api.get('/interactions', { params });
    return response.data;
  },

  async getTransactions(params = {}) {
    const response = await api.get('/transactions', { params });
    return response.data;
  },

  async getTransactionById(id) {
    const response = await api.get(`/transactions/${id}`);
    return response.data;
  },
};

export default analyticsService;