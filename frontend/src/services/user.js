import api from './api';

const userService = {
  async getProfile() {
    const response = await api.get('/users/me/profile');
    return response.data;
  },

  async updateProfile(profileData) {
    const response = await api.put('/users/me/profile', profileData);
    return response.data;
  },

  async getPreferences() {
    const response = await api.get('/users/me/preferences');
    return response.data;
  },

  async updatePreferences(preferences) {
    const response = await api.put('/users/me/preferences', preferences);
    return response.data;
  },

  // TODO: Implementar endpoint de avatar no backend
  // async uploadAvatar(file) {
  //   const formData = new FormData();
  //   formData.append('avatar', file);
  //   
  //   const response = await api.post('/users/avatar', formData, {
  //     headers: {
  //       'Content-Type': 'multipart/form-data',
  //     },
  //   });
  //   
  //   return response.data;
  // },
};

export default userService;