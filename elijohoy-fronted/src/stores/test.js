import { defineStore } from 'pinia'
import testService from 'src/services/test'
import { useAuthStore } from 'src/stores/auth'

export const useTestStore = defineStore('test', {
  state: () => ({
    sesionActual: null,
    preguntas: [],
    respuestas: {},
    progreso: 0,
    resultados: null,
    misSesiones: [],
    tiempoInicio: null
  }),

  getters: {
    /**
     * Obtener la sesión actual
     */
    getSesion: (state) => state.sesionActual,

    /**
     * Verificar si hay una sesión activa
     */
    tieneSessionActiva: (state) => !!state.sesionActual,

    /**
     * Obtener progreso del test
     */
    getProgreso: (state) => state.progreso,

    /**
     * Verificar si el test está completo
     */
    estaCompleto: (state) => state.progreso === 32,

    /**
     * Obtener respuesta para una pregunta específica
     */
    getRespuesta: (state) => (idPregunta) => state.respuestas[idPregunta],

    /**
     * Obtener resultados actuales
     */
    getResultados: (state) => state.resultados
  },

  actions: {
    /**
     * Cargar preguntas del test
     */
    async cargarPreguntas() {
      try {
        const response = await testService.obtenerPreguntas()
        if (response.success) {
          this.preguntas = response.preguntas
        }
        return response
      } catch (error) {
        console.error('Error al cargar preguntas:', error)
        throw error
      }
    },

    /**
     * Iniciar nuevo test
     */
    async iniciarTest() {
      try {
        const authStore = useAuthStore();

        if (authStore.isAuthenticated) {
          // Si autenticado, crear sesión en BD
          const response = await testService.iniciarTest();
          console.log('Respuesta al iniciar test:', response);

          if (response.success) {
            this.sesionActual = response.sesion;
            this.respuestas = {};
            this.progreso = 0;
            this.resultados = null;
            this.tiempoInicio = Date.now();
            return response;
          }
        } else {
          // Si no autenticado, inicializar localmente
          this.sesionActual = {
            id_sesion: 'local-' + Date.now(),
            estado: 'iniciado',
            fecha_inicio: new Date().toISOString()
          };
          this.respuestas = {};
          this.progreso = 0;
          this.resultados = null;
          this.tiempoInicio = Date.now();
          console.log('Test iniciado localmente (no autenticado)');
          return { success: true, sesion: this.sesionActual };
        }

        return { success: false, message: 'Error al iniciar test' };
      } catch (error) {
        console.error('Error al iniciar test:', error);
        throw error;
      }
    },

    /**
     * Guardar respuesta
     */
    async guardarRespuesta(idPregunta, valorRespuesta) {
      try {
        if (!this.sesionActual) {
          throw new Error('No hay sesión activa');
        }

        // Calcular tiempo de respuesta
        const tiempoRespuesta = this.tiempoInicio
          ? Math.floor((Date.now() - this.tiempoInicio) / 1000)
          : null;

        // Guardar en estado local
        this.respuestas[idPregunta] = {
          valor: valorRespuesta,
          tiempo: tiempoRespuesta
        };
        this.progreso = Object.keys(this.respuestas).length;

        // Si está autenticado, enviar a BD
        const authStore = useAuthStore();
        if (authStore.isAuthenticated) {
          const response = await testService.guardarRespuesta({
            id_sesion: this.sesionActual.id_sesion,
            id_pregunta: idPregunta,
            valor_respuesta: valorRespuesta,
            tiempo_respuesta: tiempoRespuesta
          });

          if (!response.success) {
            console.error('Error guardando respuesta en BD:', response.message);
          }
        } else {
          // Si no autenticado, guardar en localStorage
          localStorage.setItem('testRespuestas', JSON.stringify(this.respuestas));
        }

        console.log(`Progreso actualizado: ${this.progreso}/32 preguntas respondidas.`);

        // Reiniciar tiempo para siguiente pregunta
        this.tiempoInicio = Date.now();

        return { success: true };
      } catch (error) {
        console.error('Error al guardar respuesta:', error);
        throw error;
      }
    },

    /**
     * Sincronizar respuestas del localStorage a la BD
     */
    async sincronizarRespuestas(respuestasLocales = null) {
      try {
        const authStore = useAuthStore();

        if (!authStore.isAuthenticated) {
          console.log('Usuario no autenticado, no se puede sincronizar');
          return { success: false, message: 'Usuario no autenticado' };
        }

        if (!this.sesionActual) {
          console.log('No hay sesión activa, no se puede sincronizar');
          return { success: false, message: 'No hay sesión activa' };
        }

        // Usar respuestasLocales si se pasan, sino usar this.respuestas
        const respuestasASincronizar = respuestasLocales || this.respuestas;

        if (!respuestasASincronizar || Object.keys(respuestasASincronizar).length === 0) {
          console.log('No hay respuestas para sincronizar');
          return { success: true, message: 'No hay respuestas para sincronizar' };
        }

        console.log('Sincronizando respuestas:', respuestasASincronizar);

        // Enviar todas las respuestas a la BD
        const promesas = Object.entries(respuestasASincronizar).map(async ([idPregunta, respuesta]) => {
          const tiempoRespuesta = respuesta.tiempo || Math.floor((Date.now() - this.tiempoInicio) / 1000);

          return testService.guardarRespuesta({
            id_sesion: this.sesionActual.id_sesion,
            id_pregunta: parseInt(idPregunta),
            valor_respuesta: respuesta.valor || respuesta,
            tiempo_respuesta: tiempoRespuesta
          });
        });

        const resultados = await Promise.all(promesas);

        // Verificar si todas las respuestas se guardaron correctamente
        const errores = resultados.filter(r => !r.success);
        if (errores.length > 0) {
          console.error('Errores al sincronizar respuestas:', errores);
          return { success: false, message: 'Error al sincronizar algunas respuestas' };
        }

        // Actualizar estado local
        this.respuestas = { ...respuestasASincronizar };
        this.progreso = Object.keys(this.respuestas).length;

        console.log('Respuestas sincronizadas exitosamente');
        return { success: true, message: 'Respuestas sincronizadas exitosamente' };

      } catch (error) {
        console.error('Error al sincronizar respuestas:', error);
        return { success: false, message: error.message || 'Error al sincronizar respuestas' };
      }
    },

    /**
     * Restaurar sesión desde localStorage
     */
    restaurarSesion() {
      try {
        const sesionGuardada = JSON.parse(localStorage.getItem('testSesion'));
        if (sesionGuardada) {
          this.sesionActual = sesionGuardada;
          console.log('Sesión restaurada desde localStorage:', this.sesionActual);
        }
      } catch (error) {
        console.error('Error al restaurar la sesión desde localStorage:', error);
      }
    },

    /**
     * Finalizar test y obtener resultados
     */
    async finalizarTest() {
      try {
        const authStore = useAuthStore();

        if (!authStore.isAuthenticated) {
          // Si no autenticado, no permitir finalizar, devolver error para mostrar diálogo
          throw new Error('REQUIERE_AUTH');
        }

        console.log('Sesión actual:', this.sesionActual);

        if (!this.sesionActual) {
          throw new Error('No hay sesión activa')
        }

        if (this.progreso < 32) {
          throw new Error('Test incompleto')
        }

        const response = await testService.finalizarTest(this.sesionActual.id_sesion);
        console.log('Respuesta del backend:', response);

        if (response.success) {
          this.resultados = response.resultados;
        }

        return response;
      } catch (error) {
        console.error('Error al finalizar test:', error)
        throw error
      }
    },

    /**
     * Obtener resultados de una sesión específica
     */
    async obtenerResultados(idSesion) {
      try {
        const response = await testService.obtenerResultados(idSesion)
        if (response.success) {
          this.resultados = response.perfil
        }
        return response
      } catch (error) {
        console.error('Error al obtener resultados:', error)
        throw error
      }
    },

    /**
     * Cargar mis sesiones
     */
    async cargarMisSesiones() {
      try {
        const response = await testService.obtenerMisSesiones()
        if (response.success) {
          this.misSesiones = response.sesiones
        }
        return response
      } catch (error) {
        console.error('Error al cargar sesiones:', error)
        throw error
      }
    },

    /**
     * Asociar sesión anónima tras registro
     */
    async asociarSesionAnonima() {
      try {
        const tokenAnonimo = localStorage.getItem('tokenAnonimo');
        console.log('Token anónimo para asociar:', tokenAnonimo);

        if (!tokenAnonimo) {
          console.warn('No hay token anónimo para asociar sesión.');
          return;
        }

        const response = await testService.asociarSesion(tokenAnonimo);
        console.log('Respuesta al asociar sesión:', response);

        if (response.success) {
          localStorage.removeItem('tokenAnonimo');
          this.tokenAnonimo = null;
          console.log('Token anónimo eliminado después de asociar sesión.');
        }

        return response;
      } catch (error) {
        console.error('Error al asociar sesión:', error);
        // No lanzar error, es opcional
      }
    },

    /**
     * Verificar si el usuario debe iniciar sesión o registrarse después de completar el test
     */
    async verificarSesionPostTest() {
      try {
        if (!this.tokenAnonimo) {
          console.warn('No hay token anónimo almacenado.');
          return;
        }

        const response = await testService.verificarSesion(this.tokenAnonimo);
        console.log('Respuesta al verificar sesión post-test:', response);

        if (response.success && response.requiereLogin) {
          // Redirigir al usuario a la página de inicio de sesión o registro
          console.log('Redirigiendo al usuario a iniciar sesión o registrarse.');
          // Aquí puedes agregar la lógica para redirigir al usuario, por ejemplo:
          // this.router.push('/login');
        }

        return response;
      } catch (error) {
        console.error('Error al verificar sesión post-test:', error);
        throw error;
      }
    },

    /**
     * Redirigir al usuario a iniciar sesión o registrarse
     */
    redirigirALoginORegistro() {
      console.warn('Redirigiendo al usuario a iniciar sesión o registrarse.');
      this.router.push('/auth/login'); // Cambiar a '/auth/registro' si es necesario
    },

    /**
     * Limpiar estado del test
     */
    limpiarTest() {
      this.sesionActual = null
      this.respuestas = {}
      this.progreso = 0
      this.resultados = null
      this.tiempoInicio = null
    },

    /**
     * Reiniciar test
     */
    async reiniciarTest() {
      this.limpiarTest()
      return await this.iniciarTest()
    }
  }
})
