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
      try {
        user.value = JSON.parse(userData)
        isAuthenticated.value = true
      } catch (e) {
        console.error('Error al parsear userData:', e)
        sessionStorage.removeItem('user')
        sessionStorage.removeItem('access_token')
        user.value = null
        isAuthenticated.value = false
      }
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

  const logout = async () => {
    try {
      const result = await AuthService.logout()
      
      if (!result.success) {
        console.warn('Logout server failed, but clearing local session:', result.message)
      }
    } catch (error) {
      console.error('Logout error:', error)
      // Continue with local logout even if there's an error
    } finally {
      // Ensure we always clear local session state
      sessionStorage.clear()
      user.value = null
      isAuthenticated.value = false
    }
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