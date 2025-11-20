import { api } from './api'

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
   * @param {Object} data - Datos opcionales como id_sesion_anterior
   */
  async iniciarTest(data = {}) {
    try {
      // Simplemente hacer la petición - el interceptor de axios agregará el token automáticamente
      const response = await api.post('/test/iniciar', data)
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

  /**
   * Obtener resultados detallados de una sesión específica
   * @param {number} idSesion
   */
  async obtenerResultados(idSesion) {
    try {
      const response = await api.get(`/test/resultados/${idSesion}`)
      return response.data
    } catch (error) {
      console.error('❌ Error en obtenerResultados:', error)
      throw error.response?.data || error
    }
  },

  // ========== FUNCIONES DE ADMINISTRACIÓN DE PREGUNTAS ==========

  /**
   * Obtener todas las preguntas (solo administradores)
   */
  async obtenerTodasPreguntas() {
    try {
      const response = await api.get('/test/admin/preguntas')
      return response.data
    } catch (error) {
      throw error.response?.data || error
    }
  },

  /**
   * Crear una nueva pregunta (solo administradores)
   * @param {Object} preguntaData
   */
  async crearPregunta(preguntaData) {
    try {
      const response = await api.post('/test/admin/preguntas', preguntaData)
      return response.data
    } catch (error) {
      throw error.response?.data || error
    }
  },

  /**
   * Actualizar una pregunta existente (solo administradores)
   * @param {number} idPregunta
   * @param {Object} preguntaData
   */
  async actualizarPregunta(idPregunta, preguntaData) {
    try {
      const response = await api.put(`/test/admin/preguntas/${idPregunta}`, preguntaData)
      return response.data
    } catch (error) {
      throw error.response?.data || error
    }
  },

  /**
   * Eliminar (desactivar) una pregunta (solo administradores)
   * @param {number} idPregunta
   */
  async eliminarPregunta(idPregunta) {
    try {
      const response = await api.delete(`/test/admin/preguntas/${idPregunta}`)
      return response.data
    } catch (error) {
      throw error.response?.data || error
    }
  },
}

export default testService
