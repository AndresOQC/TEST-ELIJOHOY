import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import AuthService from 'src/services/auth'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const isAuthenticated = ref(false)
  const loading = ref(false)

  // Getters
  const userName = computed(() => {
    return user.value?.nombre_completo || ''
  })

  const userRoles = computed(() => {
    return user.value?.roles || []
  })

  // Actions
  const initializeAuth = () => {
    const token = sessionStorage.getItem('access_token')
    const userData = sessionStorage.getItem('user')

    if (token && userData) {
      user.value = JSON.parse(userData)
      isAuthenticated.value = true
    } else {
      user.value = null
      isAuthenticated.value = false
    }
  }

  const login = async (credentials) => {
    loading.value = true
    try {
      const result = await AuthService.login(credentials)

      if (result.success) {
        user.value = result.user
        isAuthenticated.value = true
        return { success: true }
      }

      return { success: false, message: result.message }
    } catch (error) {
      console.error('Store login error:', error)
      return { success: false, message: 'Error de conexión' }
    } finally {
      loading.value = false
    }
  }

  const register = async (userData) => {
    loading.value = true
    try {
      const result = await AuthService.register(userData)

      if (result.success) {
        user.value = result.user
        isAuthenticated.value = true
        return { success: true }
      }

      return { success: false, message: result.message }
    } catch (error) {
      console.error('Store register error:', error)
      return { success: false, message: 'Error de conexión' }
    } finally {
      loading.value = false
    }
  }

  const updateProfile = async (profileData) => {
    loading.value = true
    try {
      const result = await AuthService.updateProfile(profileData)

      if (result.success) {
        user.value = result.user
        return { success: true }
      }

      return { success: false, message: result.message }
    } catch (error) {
      console.error('Store update profile error:', error)
      return { success: false, message: 'Error de conexión' }
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    // Limpiar sessionStorage
    sessionStorage.clear()
    // Limpiar localStorage de datos de autenticación
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    localStorage.removeItem('user_data')
    localStorage.removeItem('user_token')
    localStorage.removeItem('idUsuario')
    // Limpiar estado
    user.value = null
    isAuthenticated.value = false
  }

  const refreshUser = async () => {
    if (!isAuthenticated.value) return
    
    // Check if we have a token before making the request
    const token = sessionStorage.getItem('access_token')
    if (!token) {
      return
    }

    try {
      const result = await AuthService.getCurrentUser()
      if (result.success) {
        user.value = result.user
      }
    } catch (error) {
      console.error('Refresh user error:', error)
      // If refresh fails due to auth issues, clear auth state
      if (error.response?.status === 401) {
        logout()
      }
    }
  }

  // Initialize auth state on store creation
  initializeAuth()

  return {
    // State
    user,
    isAuthenticated,
    loading,

    // Getters
    userName,
    userRoles,

    // Actions
    initializeAuth,
    login,
    register,
    updateProfile,
    logout,
    refreshUser
  }
})

export default useAuthStore