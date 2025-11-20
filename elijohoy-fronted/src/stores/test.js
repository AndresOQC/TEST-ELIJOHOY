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
        authStore.initializeAuth();

        console.log('🔍 Iniciando test...');
        console.log('  - Autenticado:', authStore.isAuthenticated);
        console.log('  - Sesión anterior:', this.sesionActual?.id_sesion);

        // Verificar si hay respuestas guardadas en localStorage
        const respuestasGuardadas = localStorage.getItem('testRespuestas');
        const respuestasPreviasCount = respuestasGuardadas ? Object.keys(JSON.parse(respuestasGuardadas)).length : 0;

        if (authStore.isAuthenticated) {
          // ==================== CASO: Usuario autenticado ====================
          console.log('🔐 Usuario autenticado, creando sesión en BD...');

          // Preparar datos para la solicitud
          const requestData = {};
          
          // Si hay sesión local anterior, intentar reutilizarla
          const sesionLocal = localStorage.getItem('testSesionLocal');
          if (sesionLocal) {
            const sesionLocalParsed = JSON.parse(sesionLocal);
            if (sesionLocalParsed.id_sesion && !sesionLocalParsed.id_sesion.startsWith('local-')) {
              // Es una sesión con ID numérico, puede reutilizarse
              requestData.id_sesion_anterior = sesionLocalParsed.id_sesion;
              console.log('📝 Sesión anterior encontrada:', sesionLocalParsed.id_sesion);
            }
          }

          // Limpiar sesión anterior del estado local
          this.sesionActual = null;
          this.progreso = 0;
          this.resultados = null;

          // Crear nueva sesión en BD (o reutilizar la anterior)
          const response = await testService.iniciarTest(requestData);
          console.log('✅ Respuesta al iniciar test (autenticado):', response);

          if (response.success) {
            this.sesionActual = response.sesion;
            // Inicializar respuestas vacías para nueva sesión autenticada
            this.respuestas = {};
            this.progreso = 0;
            this.tiempoInicio = Date.now();
            
            // Si hay respuestas guardadas anteriormente (del test anónimo),
            // se sincronizarán en finalizarTestAutomaticamente()
            if (respuestasPreviasCount > 0) {
              console.log(`📝 Se encontraron ${respuestasPreviasCount} respuestas previas de sesión anónima`);
            }
            
            return response;
          } else {
            throw new Error(response.message || 'Error al crear sesión de test');
          }
        } else {
          // ==================== CASO: Usuario no autenticado ====================
          console.log('👤 Usuario no autenticado, usando sesión local...');

          // Si hay respuestas previas guardadas, reutilizar sesión anterior
          const sesionLocal = localStorage.getItem('testSesionLocal');
          
          if (respuestasPreviasCount > 0 && sesionLocal) {
            // Reutilizar sesión anterior
            console.log('♻️ Reutilizando sesión local anterior');
            this.sesionActual = JSON.parse(sesionLocal);
            this.respuestas = JSON.parse(respuestasGuardadas);
            this.progreso = respuestasPreviasCount;
          } else {
            // Crear nueva sesión local
            console.log('✨ Creando nueva sesión local');
            this.limpiarTest();
            
            this.sesionActual = {
              id_sesion: 'local-' + Date.now(),
              estado: 'iniciado',
              fecha_inicio: new Date().toISOString()
            };
            this.respuestas = {};
            this.progreso = 0;
            
            localStorage.setItem('testSesionLocal', JSON.stringify(this.sesionActual));
            localStorage.setItem('testRespuestas', JSON.stringify(this.respuestas));
          }

          this.resultados = null;
          this.tiempoInicio = Date.now();

          console.log('✅ Sesión local inicializada:', this.sesionActual.id_sesion);
          return { 
            success: true, 
            sesion: this.sesionActual 
          };
        }
      } catch (error) {
        console.error('❌ Error al iniciar test:', error);
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
          // Si no autenticado, guardar respuestas en localStorage
          localStorage.setItem('testRespuestas', JSON.stringify(this.respuestas));
          // También guardar sesión local para recuperación
          localStorage.setItem('testSesionLocal', JSON.stringify(this.sesionActual));
        }

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
     * Restaurar sesión desde localStorage (para usuarios no autenticados)
     */
    restaurarSesion() {
      try {
        // Intentar restaurar sesión local (usuarios no autenticados)
        const sesionLocalGuardada = localStorage.getItem('testSesionLocal');
        if (sesionLocalGuardada) {
          this.sesionActual = JSON.parse(sesionLocalGuardada);
          console.log('Sesión local restaurada desde localStorage:', this.sesionActual);
          return true;
        }
        
        // Si no hay sesión local guardada
        console.log('No hay sesión local guardada en localStorage');
        return false;
      } catch (error) {
        console.error('Error al restaurar la sesión desde localStorage:', error);
        return false;
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

        // Guardar ID de sesión antes de limpiar
        const idSesion = this.sesionActual.id_sesion;

        const response = await testService.finalizarTest(idSesion);
        console.log('Respuesta del backend:', response);

        if (response.success) {
          this.resultados = response.resultados;
          // Guardar resultados antes de limpiar
          const resultsToKeep = this.resultados;
          // Limpiar estado después de finalizar exitosamente
          this.limpiarTest();
          // Restaurar resultados para que se puedan mostrar
          this.resultados = resultsToKeep;
          // Agregar el ID de sesión a la respuesta para que TestPage pueda navegar
          response.id_sesion = idSesion;
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
