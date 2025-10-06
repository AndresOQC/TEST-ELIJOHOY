import api from './api'

/**
 * Servicio para gestionar el test de personalidad OEJTS
 */
const testService = {
  /**
   * Obtener todas las preguntas del test
   */
  async obtenerPreguntas() {
    try {
      const response = await api.get('/test/preguntas')
      return response.data
    } catch (error) {
      throw error.response?.data || error
    }
  },

  /**
   * Iniciar una nueva sesión de test
   */
  async iniciarTest() {
    try {
      // Esperar un poco para asegurar que el token esté disponible
      await new Promise(resolve => setTimeout(resolve, 100))
      
      const token = sessionStorage.getItem('access_token')
      console.log('🔍 Iniciando test - Token en sessionStorage:', !!token)
      console.log('🔍 Token completo:', token ? token.substring(0, 50) + '...' : 'null')
      
      if (!token) {
        throw new Error('No hay token de autenticación disponible')
      }
      
      // Hacer la petición manualmente con el token para asegurar que se envía
      const response = await api.post('/test/iniciar', {}, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })
      console.log('🔍 Respuesta del servidor:', response.data)
      return response.data
    } catch (error) {
      console.error('❌ Error en iniciarTest:', error)
      throw error.response?.data || error
    }
  },

  /**
   * Guardar una respuesta individual
   * @param {Object} respuesta - { id_sesion, id_pregunta, valor_respuesta, tiempo_respuesta }
   */
  async guardarRespuesta(respuesta) {
    try {
      console.log('🔍 Guardando respuesta - Token en sessionStorage:', !!sessionStorage.getItem('access_token'))
      
      const response = await api.post('/test/responder', respuesta)
      return response.data
    } catch (error) {
      console.error('❌ Error en guardarRespuesta:', error)
      throw error.response?.data || error
    }
  },

  /**
   * Finalizar test y calcular resultados
   * @param {number} idSesion
   */
  async finalizarTest(idSesion) {
    try {
      const response = await api.post(`/test/finalizar/${idSesion}`)
      return response.data
    } catch (error) {
      throw error.response?.data || error
    }
  },

  /**
   * Obtener sesiones del usuario actual
   */
  async obtenerMisSesiones() {
    try {
      const response = await api.get('/test/mis-sesiones')
      return response.data
    } catch (error) {
      console.error('❌ Error en obtenerMisSesiones:', error)
      throw error.response?.data || error
    }
  },

  /**
   * Asociar una sesión anónima al usuario tras registro
   * @param {number} idSesion
   */
  async asociarSesion(idSesion) {
    try {
      // Obtener el token JWT del almacenamiento (sessionStorage o localStorage)
      const accessToken = sessionStorage.getItem('access_token') || localStorage.getItem('access_token')
      const headers = {
        'Content-Type': 'application/json'
      }
      if (accessToken) {
        headers['Authorization'] = `Bearer ${accessToken}`
      }
      const response = await api.post(
        '/test/asociar-sesion',
        { id_sesion: idSesion },
        { headers }
      )
      return response.data
    } catch (error) {
      throw error.response?.data || error
    }
  },

  /**
   * Buscar sesión por id
   * @param {number} idSesion
   */
  async buscarSesionPorId(idSesion) {
    try {
      const response = await api.post('/test/buscar-sesion', {
        id_sesion: idSesion
      })
      return response.data
    } catch (error) {
      throw error.response?.data || error
    }
  },

  /**
   * Obtener todos los tipos de personalidad
   */
  async obtenerTipos() {
    try {
      const response = await api.get('/test/tipos')
      return response.data
    } catch (error) {
      throw error.response?.data || error
    }
  },

  /**
   * Obtener información de un tipo específico
   * @param {string} codigo - Código del tipo (ej: 'INTJ')
   */
  async obtenerTipoPorCodigo(codigo) {
    try {
      const response = await api.get(`/test/tipos/${codigo}`)
      return response.data
    } catch (error) {
      throw error.response?.data || error
    }
  },

  /**
   * Obtener estadísticas del sistema (solo admin)
   */
  async obtenerEstadisticas() {
    try {
      const response = await api.get('/test/estadisticas')
      return response.data
    } catch (error) {
      throw error.response?.data || error
    }
  },
}

export default testService
