import { api } from 'boot/axios';

// Prefer environment value, fall back to relative '/api' so requests are proxied correctly by nginx
const API_URL = process.env.VUE_APP_API_URL || '/api';

// Configure axios defaults sss
api.defaults.baseURL = API_URL;
api.defaults.headers.common['Content-Type'] = 'application/json';
api.defaults.headers.common['Accept'] = 'application/json';

// Add request interceptor to include Authorization header
api.interceptors.request.use(config => {
  const token = sessionStorage.getItem('access_token');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
    console.log('🔑 Token enviado en request:', config.url, token.substring(0, 20) + '...');
  } else {
    console.warn('⚠️ No hay token para request:', config.url);
  }
  return config;
});

export { api };
export default api;