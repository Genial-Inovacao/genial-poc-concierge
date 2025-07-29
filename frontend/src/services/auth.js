import api from './api';

const authService = {
  async login(credentials) {
    const response = await api.post('/auth/login', credentials);
    const { access_token, refresh_token, token_type } = response.data;
    
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
    
    return response.data;
  },

  async register(userData) {
    // Adaptar os dados para o formato esperado pelo backend
    const registrationData = {
      username: userData.name, // backend espera username, não name
      email: userData.email,
      password: userData.password,
    };
    const response = await api.post('/auth/register', registrationData);
    return response.data;
  },

  async logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    // Opcionalmente, fazer chamada para invalidar token no backend
  },

  async getCurrentUser() {
    const response = await api.get('/users/me/profile');
    return response.data;
  },

  async refreshToken(refreshToken) {
    const response = await api.post('/auth/refresh', {
      refresh_token: refreshToken,
    });
    return response.data;
  },

  isAuthenticated() {
    return !!localStorage.getItem('access_token');
  },

  getToken() {
    return localStorage.getItem('access_token');
  },
};

export default authService;