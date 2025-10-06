import { api } from 'boot/axios'

const API_BASE_URL = process.env.VUE_APP_API_URL || 'http://localhost:5000/api'

// Configure axios defaults
api.defaults.baseURL = API_BASE_URL
api.defaults.headers.common['Content-Type'] = 'application/json'
api.defaults.headers.common['Accept'] = 'application/json'

// Interceptors are now configured in boot/axios.js

export { api }
export default api