import { boot } from 'quasar/wrappers'
import axios from 'axios'

// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)

const api = axios.create({ 
  baseURL: process.env.VUE_APP_API_URL || 'http://localhost:5000/api',
  timeout: 10000,
  withCredentials: false, // Explicit setting for CORS
  headers: {
    'Content-Type': 'application/json',
  }
})

// Add request interceptor to attach Authorization header
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

export default boot(({ app }) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api

  app.config.globalProperties.$axios = axios
  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file

  app.config.globalProperties.$api = api
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API
})

// Add response interceptor to handle errors and token refresh
api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;

    if (error.response?.status === 401) {
      console.error('🚫 Error 401 - Token inválido o expirado:', error.config.url);
      console.error('Detalles del error:', error.response?.data);
    }

    // Only handle 401 errors from API endpoints (not login)
    if (error.response?.status !== 401) {
      return Promise.reject(error);
    }

    // Don't intercept login requests - let them fail naturally
    if (originalRequest.url?.includes('/auth/login') || originalRequest.url?.includes('/auth/register')) {
      return Promise.reject(error);
    }

    // Avoid infinite retry loops
    if (originalRequest._retry) {
      console.error('🔄 Max retries reached, clearing session');
      sessionStorage.clear();
      window.location.hash = '#/auth/login';
      return Promise.reject(error);
    }

    originalRequest._retry = true;

    // Get refresh token
    const refreshToken = sessionStorage.getItem('refresh_token');
    if (!refreshToken) {
      console.error('🔄 No refresh token available');
      sessionStorage.clear();
      window.location.hash = '#/auth/login';
      return Promise.reject(error);
    }

    // Prevent multiple simultaneous refresh attempts
    if (window._refreshingToken) {
      console.log('🔄 Waiting for ongoing token refresh...');
      return new Promise((resolve, reject) => {
        const checkInterval = setInterval(() => {
          if (!window._refreshingToken) {
            clearInterval(checkInterval);
            const newToken = sessionStorage.getItem('access_token');
            if (newToken) {
              originalRequest.headers.Authorization = `Bearer ${newToken}`;
              resolve(api(originalRequest));
            } else {
              reject(error);
            }
          }
        }, 100);
      });
    }

    window._refreshingToken = true;
    console.log('🔄 Attempting token refresh...');

    try {
      // Create a new axios instance for refresh to avoid interceptor loops
      const refreshApi = axios.create({
        baseURL: process.env.VUE_APP_API_URL || 'http://localhost:5000/api',
        timeout: 10000
      });

      const response = await refreshApi.post('/auth/refresh', {}, {
        headers: {
          'Authorization': `Bearer ${refreshToken}`,
          'Content-Type': 'application/json'
        }
      });

      const access_token = response.data.data?.access_token || response.data.access_token;

      if (access_token) {
        console.log('✅ Token refreshed successfully');
        sessionStorage.setItem('access_token', access_token);
        if (response.data.data?.user) {
          sessionStorage.setItem('user', JSON.stringify(response.data.data.user));
        }

        // Update the original request with new token
        originalRequest.headers.Authorization = `Bearer ${access_token}`;

        window._refreshingToken = false;
        return api(originalRequest);
      } else {
        throw new Error('No access token returned from refresh');
      }
    } catch (refreshError) {
      console.error('❌ Token refresh failed:', refreshError);
      sessionStorage.clear();
      window.location.hash = '#/auth/login';
      window._refreshingToken = false;
      return Promise.reject(refreshError);
    }
  }
);

export { api }