import { api } from 'boot/axios';

const API_URL = 'http://185.111.156.248:5000/api'; // Asigna directamente la URL del backend

// Configure axios defaults
api.defaults.baseURL = API_URL;
api.defaults.headers.common['Content-Type'] = 'application/json';
api.defaults.headers.common['Accept'] = 'application/json';

// Interceptors are now configured in boot/axios.js

export { api };
export default api;