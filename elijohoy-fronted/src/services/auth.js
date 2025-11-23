import { api } from './api'

export class AuthService {
  /**
   * Register new user
   */
  static async register(userData) {
    try {
      const response = await api.post('/auth/register', {
        email: userData.email,
        password: userData.password,
        confirm_password: userData.confirm_password,
        nombre: userData.nombre,
        apellidos: userData.apellidos,
        edad: userData.edad,
        genero: userData.genero,
        ciudad: userData.ciudad,
        pais: userData.pais,
        institucion_educativa: userData.institucion_educativa,
        grado: userData.grado,
        seccion: userData.seccion,
        turno: userData.turno
      })
      
      if (response.data.success) {
        const { user, access_token, refresh_token } = response.data.data
        
        // Store tokens and user data in sessionStorage
        sessionStorage.setItem('access_token', access_token)
        sessionStorage.setItem('refresh_token', refresh_token)
        sessionStorage.setItem('user', JSON.stringify(user))
        
        return {
          success: true,
          user,
          requiresProfileCompletion: response.data.data.requires_profile_completion
        }
      }
      
      return { success: false, message: response.data.message }
    } catch (error) {
      console.error('Register error:', error)
      return {
        success: false,
        message: error.response?.data?.message || 'Error en el registro'
      }
    }
  }

  /**
   * Login user
   */
  static async login(credentials) {
    try {
      const response = await api.post('/auth/login', {
        email: credentials.email,
        password: credentials.password
      })
      
      if (response.data.success) {
        const { user, access_token, refresh_token } = response.data.data
        
        // Store tokens and user data in sessionStorage
        sessionStorage.setItem('access_token', access_token)
        sessionStorage.setItem('refresh_token', refresh_token)
        sessionStorage.setItem('user', JSON.stringify(user))
        
        return {
          success: true,
          user,
          requiresProfileCompletion: response.data.data.requires_profile_completion
        }
      }
      
      return { success: false, message: response.data.message }
    } catch (error) {
      console.error('Login error:', error)
      return {
        success: false,
        message: error.response?.data?.message || 'Error en el login'
      }
    }
  }

  /**
   * Update user profile
   */
  static async updateProfile(profileData) {
    try {
      const response = await api.put('/auth/update-profile', profileData)

      if (response.data.success) {
        const { user } = response.data.data

        // Update stored user data in sessionStorage
        sessionStorage.setItem('user', JSON.stringify(user))

        return { success: true, user }
      }

      return { success: false, message: response.data.message }
    } catch (error) {
      console.error('Profile update error:', error)
      return {
        success: false,
        message: error.response?.data?.message || 'Error actualizando perfil'
      }
    }
  }

  /**
   * Refresh user data
   */
  static async refreshUser() {
    try {
      const response = await api.get('/auth/me')

      if (response.data.success) {
        const { user } = response.data.data

        // Update stored user data in sessionStorage
        sessionStorage.setItem('user', JSON.stringify(user))

        return { success: true, user }
      }

      return { success: false, message: response.data.message }
    } catch (error) {
      console.error('Refresh user error:', error)
      return {
        success: false,
        message: error.response?.data?.message || 'Error obteniendo datos del usuario'
      }
    }
  }

  /**
   * Get current user info
   */
  static async getCurrentUser() {
    try {
      const response = await api.get('/auth/me')

      if (response.data.success) {
        const { user } = response.data.data

        // Update stored user data in sessionStorage
        sessionStorage.setItem('user', JSON.stringify(user))

        return { success: true, user }
      }

      return { success: false, message: response.data.message }
    } catch (error) {
      console.error('Get current user error:', error)
      return {
        success: false,
        message: error.response?.data?.message || 'Error obteniendo datos del usuario'
      }
    }
  }

  /**
   * Logout user
   */
  static async logout() {
    try {
      const response = await api.post('/auth/logout')
      
      if (!response.data.success) {
        console.warn('Logout server warning:', response.data.message)
      }
      
      return { success: true, message: 'Logout exitoso' }
    } catch (error) {
      console.error('Logout error:', error.response?.data?.message || error.message)
      
      // Even if logout fails on server, clear local session
      // but return the error so caller knows
      return {
        success: false,
        message: error.response?.data?.message || 'Error en logout'
      }
    } finally {
      // Always remove tokens and user data from sessionStorage
      // This ensures user is logged out locally even if server logout fails
      sessionStorage.removeItem('access_token')
      sessionStorage.removeItem('refresh_token')
      sessionStorage.removeItem('user')
    }
  }

  /**
   * Send password reset email
   */
  static async sendPasswordReset(email) {
    try {
      const response = await api.post('/auth/recover-password', { email })
      
      return {
        success: response.data.success,
        message: response.data.message
      }
    } catch (error) {
      console.error('Password reset error:', error)
      return {
        success: false,
        message: error.response?.data?.message || 'Error enviando email de recuperación'
      }
    }
  }

  /**
   * Reset password with token
   */
  static async resetPassword(token, newPassword) {
    try {
      const response = await api.post('/auth/reset-password', {
        token,
        new_password: newPassword
      })
      
      return {
        success: response.data.success,
        message: response.data.message
      }
    } catch (error) {
      console.error('Reset password error:', error)
      return {
        success: false,
        message: error.response?.data?.message || 'Error restableciendo contraseña'
      }
    }
  }

  /**
   * Check if user is authenticated
   */
  static isAuthenticated() {
    const token = sessionStorage.getItem('access_token')
    const user = sessionStorage.getItem('user')
    return !!(token && user)
  }

  /**
   * Get stored user data
   */
  static getStoredUser() {
    const userData = sessionStorage.getItem('user')
    return userData ? JSON.parse(userData) : null
  }

  /**
   * Get access token
   */
  static getAccessToken() {
    return sessionStorage.getItem('access_token')
  }

  /**
   * Get refresh token
   */
  static getRefreshToken() {
    return sessionStorage.getItem('refresh_token')
  }
}

// Export as default
export default AuthService