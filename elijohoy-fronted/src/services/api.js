import { api } from 'boot/axios'
import axios from 'axios'

const API_BASE_URL = process.env.VUE_APP_API_URL || 'http://localhost:5000/api'

// Configure axios defaults
api.defaults.baseURL = API_BASE_URL

// ...existing code...

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // Only handle 401 errors from API endpoints (not login)
    if (error.response?.status !== 401) {
      return Promise.reject(error);
    }

    // Don't intercept login requests - let them fail naturally
    if (originalRequest.url?.includes('/auth/login')) {
      return Promise.reject(error);
    }

    // Avoid infinite retry loops
    if (originalRequest._retry) {
      sessionStorage.clear();
      window.location.hash = '#/auth/login';
      return Promise.reject(error);
    }
    
    originalRequest._retry = true;

    // Get refresh token
    const refreshToken = sessionStorage.getItem('refresh_token');
    if (!refreshToken) {
      sessionStorage.clear();
      window.location.hash = '#/auth/login';
      return Promise.reject(error);
    }

    // Prevent multiple simultaneous refresh attempts
    if (window._refreshingToken) {
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
    
    try {
      // Create a new axios instance for refresh to avoid interceptor loops
      const refreshApi = axios.create({ 
        baseURL: API_BASE_URL,
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
      sessionStorage.clear();
      window.location.hash = '#/auth/login';
      window._refreshingToken = false;
      return Promise.reject(refreshError);
    }
  }
)

export { api }
export default api