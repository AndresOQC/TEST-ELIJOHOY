import { api } from 'boot/axios';

const API_URL = 'http://185.111.156.248:5000/api'; // Asigna directamente la URL del backend

// Configure axios defaults
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