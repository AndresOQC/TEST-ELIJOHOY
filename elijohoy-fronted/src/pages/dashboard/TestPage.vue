<template>
  <q-page class="test-page">
    <div class="container">
      <!-- Header con título y progreso general -->
      <div class="test-header">
        <h1 class="test-title">Test de Personalidad OEJTS</h1>
        <div class="progress-info">
          <div class="progress-text">
            Progreso: <strong>{{ paginaActual + 1 }}</strong> de <strong>{{ totalPaginas }}</strong> páginas
          </div>
          <div class="progress-dots">
            <div
              v-for="i in totalPaginas"
              :key="i"
              class="progress-dot"
              :class="{ active: i <= paginaActual + 1, completed: i < paginaActual + 1 }"
            ></div>
          </div>
        </div>
      </div>

      <!-- Contenedor de preguntas -->
      <div v-if="!loading && preguntasPagina.length > 0" class="questions-container">
        <div
          v-for="(pregunta, index) in preguntasPagina"
          :key="pregunta.id_pregunta"
          class="question-card"
        >
          <div class="question-number">Pregunta {{ (paginaActual * 3) + index + 1 }}</div>

          <div class="question-options">
            <div class="option-label left">{{ pregunta.texto_izquierda }}</div>

            <!-- Selector de bolitas -->
            <div class="bubbles-selector">
              <div
                v-for="valor in 5"
                :key="valor"
                class="bubble"
                :class="{ selected: getRespuesta(pregunta.id_pregunta) === valor }"
                :style="{
                  width: BUBBLE_SIZES[valor - 1] + 'px',
                  height: BUBBLE_SIZES[valor - 1] + 'px'
                }"
                @click="seleccionarRespuesta(pregunta.id_pregunta, valor)"
              >
                <div class="bubble-inner"></div>
              </div>
            </div>

            <div class="option-label right">{{ pregunta.texto_derecha }}</div>
          </div>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading-container">
        <q-spinner color="purple-7" size="60px" />
        <p>Cargando test...</p>
      </div>

      <!-- Botones de navegación -->
      <div class="navigation-buttons">
        <q-btn
          v-if="paginaActual > 0"
          unelevated
          color="grey-6"
          label="Anterior"
          icon="arrow_back"
          @click="paginaAnterior"
          class="nav-btn"
          no-caps
        />
        <div v-else></div>

        <q-btn
          v-if="paginaActual < totalPaginas - 1"
          unelevated
          color="purple-7"
          label="Siguiente"
          icon-right="arrow_forward"
          @click="paginaSiguiente"
          :disable="!paginaCompleta"
          class="nav-btn"
          no-caps
        />
        <q-btn
          v-else
          unelevated
          color="positive"
          label="Finalizar Test"
          icon-right="check_circle"
          @click="finalizar"
          :disable="!todasRespondidas"
          class="nav-btn finish-btn"
          no-caps
        />
      </div>

      <!-- Error Notification se maneja programáticamente -->
      <div v-if="error" class="error-notification">
        <q-banner class="text-white bg-red-8" rounded>
          <template v-slot:avatar>
            <q-icon name="error" />
          </template>
          {{ errorMessage }}
        </q-banner>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTestStore } from 'src/stores/test'
import { useAuthStore } from 'src/stores/auth'
import { useQuasar } from 'quasar'

const router = useRouter()
const testStore = useTestStore()
const authStore = useAuthStore()
const $q = useQuasar()

const loading = ref(false)
const preguntas = ref([])
const respuestas = ref({})
const paginaActual = ref(0)
const error = ref(false)
const errorMessage = ref('')

const PREGUNTAS_POR_PAGINA = 3
const BUBBLE_SIZES = [32, 40, 48, 56, 64] // Tamaños para las 5 bolitas

const totalPaginas = computed(() => Math.ceil(preguntas.value.length / PREGUNTAS_POR_PAGINA))

const preguntasPagina = computed(() => {
  const inicio = paginaActual.value * PREGUNTAS_POR_PAGINA
  const fin = inicio + PREGUNTAS_POR_PAGINA
  return preguntas.value.slice(inicio, fin)
})

const paginaCompleta = computed(() => {
  return preguntasPagina.value.every(p => respuestas.value[p.id_pregunta])
})

const todasRespondidas = computed(() => {
  return preguntas.value.every(p => respuestas.value[p.id_pregunta])
})

async function finalizarTestAutomaticamente() {
  console.log('Iniciando finalización automática del test...')

  // Verificar que todas las preguntas estén respondidas
  if (!todasRespondidas.value) {
    throw new Error('El test no está completo')
  }

  loading.value = true

  try {
    // Si está autenticado, verificar si necesita crear sesión y sincronizar
    if (authStore.isAuthenticated) {
      // Si no tiene sesión activa, crear una y sincronizar respuestas
      if (!testStore.getSesion) {
        console.log('Creando sesión y sincronizando respuestas...')

        // 1. Crear sesión de test
        const sesionResponse = await testStore.iniciarTest()
        if (!sesionResponse.success) {
          throw new Error('Error al crear sesión de test')
        }

        // 2. Sincronizar respuestas del localStorage a la BD
        const respuestasGuardadas = localStorage.getItem('testRespuestas')
        if (respuestasGuardadas) {
          const respuestasParseadas = JSON.parse(respuestasGuardadas)
          const sincronizacionResponse = await testStore.sincronizarRespuestas(respuestasParseadas)

          if (sincronizacionResponse.success) {
            console.log('Respuestas sincronizadas exitosamente')
            // Limpiar localStorage después de sincronizar
            localStorage.removeItem('testRespuestas')
          } else {
            throw new Error('Error al sincronizar respuestas')
          }
        }
      }

      // Finalizar test
      const response = await testStore.finalizarTest()

      if (response.success) {
        console.log('Test finalizado exitosamente')

        $q.notify({
          type: 'positive',
          message: '¡Test completado! Tus resultados han sido guardados.',
          icon: 'check_circle'
        })

        // Redirigir a resultados
        router.push({
          name: 'test-resultados',
          params: { id: testStore.getSesion.id_sesion }
        })
      } else {
        throw new Error(response.message || 'Error al finalizar el test')
      }
    } else {
      throw new Error('Usuario no autenticado')
    }
  } catch (error) {
    console.error('Error en finalización automática:', error)
    throw error
  } finally {
    loading.value = false
  }
}

function getRespuesta(idPregunta) {
  return respuestas.value[idPregunta] || null
}

function seleccionarRespuesta(idPregunta, valor) {
  respuestas.value[idPregunta] = valor
  // Guardar respuesta SOLO en localStorage (no en BD hasta que se registre/loguee)
  localStorage.setItem('testRespuestas', JSON.stringify(respuestas.value))
  console.log('Respuesta guardada en localStorage:', idPregunta, valor)
}

function paginaSiguiente() {
  if (paginaCompleta.value && paginaActual.value < totalPaginas.value - 1) {
    paginaActual.value++
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

function paginaAnterior() {
  if (paginaActual.value > 0) {
    paginaActual.value--
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

async function finalizar() {
  if (!todasRespondidas.value) {
    error.value = true
    errorMessage.value = 'Debes responder todas las preguntas antes de finalizar el test.'
    return
  }

  try {
    loading.value = true

    // Verificar si está autenticado
    if (!authStore.isAuthenticated) {
      loading.value = false

      // Mostrar diálogo obligando a iniciar sesión
      $q.dialog({
        title: 'Iniciar Sesión Requerido',
        message: 'Para guardar tus resultados y acceder a ellos en el futuro, debes iniciar sesión o crear una cuenta.',
        persistent: true,
        ok: {
          label: 'Iniciar Sesión',
          color: 'primary',
          noCaps: true
        },
        cancel: {
          label: 'Crear Cuenta',
          color: 'secondary',
          noCaps: true,
          flat: true
        }
      }).onOk(() => {
        // Marcar que viene desde el test para finalizar automáticamente después
        localStorage.setItem('pendingTestFinalization', 'true')
        router.push('/auth/login')
      }).onCancel(() => {
        // Marcar que viene desde el test para finalizar automáticamente después
        localStorage.setItem('pendingTestFinalization', 'true')
        router.push('/auth/registro')
      })
      return
    }

    // Si está autenticado, verificar si necesita crear sesión y sincronizar
    if (authStore.isAuthenticated) {
      // Si no tiene sesión activa, crear una y sincronizar respuestas
      if (!testStore.getSesion) {
        console.log('Creando sesión y sincronizando respuestas antes de finalizar...')

        try {
          // 1. Crear sesión de test
          const sesionResponse = await testStore.iniciarTest()
          if (!sesionResponse.success) {
            throw new Error('Error al crear sesión de test')
          }

          // 2. Sincronizar respuestas del localStorage a la BD
          const respuestasGuardadas = localStorage.getItem('testRespuestas')
          if (respuestasGuardadas) {
            const respuestasParseadas = JSON.parse(respuestasGuardadas)
            const sincronizacionResponse = await testStore.sincronizarRespuestas(respuestasParseadas)

            if (sincronizacionResponse.success) {
              console.log('Respuestas sincronizadas exitosamente')
              // Limpiar localStorage después de sincronizar
              localStorage.removeItem('testRespuestas')
            } else {
              throw new Error('Error al sincronizar respuestas')
            }
          }
        } catch (syncError) {
          console.error('Error en sincronización:', syncError)
          error.value = true
          errorMessage.value = 'Error al guardar el test. Intenta nuevamente.'
          return
        }
      }

      // Finalizar test normalmente
      const response = await testStore.finalizarTest()

      if (response.success) {
        $q.notify({
          type: 'positive',
          message: 'Test completado exitosamente'
        })

        // Redirigir a resultados
        router.push({
          name: 'test-resultados',
          params: { id: testStore.getSesion.id_sesion }
        })
      } else {
        throw new Error(response.message || 'Error al finalizar el test')
      }
    }
  } catch (error) {
    if (error.message === 'REQUIERE_AUTH') {
      // Ya se manejó arriba
      return
    }
    error.value = true
    errorMessage.value = error.message || 'Error al finalizar el test.'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  console.log('🚀 TestPage onMounted - Iniciando carga del test')

  // Asegurar que el authStore esté inicializado
  authStore.initializeAuth()

  console.log('🔐 Estado de autenticación:', authStore.isAuthenticated)
  console.log('👤 Usuario:', authStore.user)
  console.log('🔑 Token en sessionStorage:', sessionStorage.getItem('access_token') ? 'Presente' : 'Ausente')

  try {
    loading.value = true

    // Cargar preguntas
    console.log('📚 Cargando preguntas...')
    const respPreguntas = await testStore.cargarPreguntas();
    console.log('Respuesta del API preguntas:', respPreguntas);
    if (respPreguntas.success) {
      preguntas.value = respPreguntas.preguntas;
      console.log('Preguntas cargadas:', preguntas.value.length);
    }

    // Si el usuario está autenticado, verificar si ya tiene una sesión activa
    if (authStore.isAuthenticated && !testStore.getSesion) {
      console.log('✅ Usuario autenticado, verificando sesiones existentes...')
      try {
        const sesionesResponse = await testStore.cargarMisSesiones()
        console.log('Respuesta sesiones:', sesionesResponse)
        if (sesionesResponse.success && sesionesResponse.sesiones.length > 0) {
          // Buscar la sesión más reciente que no esté completada
          const sesionActiva = sesionesResponse.sesiones.find(s => !s.completado)
          if (sesionActiva) {
            console.log('Sesión activa encontrada:', sesionActiva)
            // Cargar respuestas de la sesión activa
            testStore.sesionActual = sesionActiva
            // Aquí podrías cargar las respuestas existentes de la BD si fuera necesario
          }
        }
      } catch (error) {
        console.log('No hay sesiones existentes o error al cargar:', error.message)
      }
    }

    // Cargar respuestas guardadas en localStorage si existen
    const respuestasGuardadas = localStorage.getItem('testRespuestas')
    if (respuestasGuardadas) {
      respuestas.value = JSON.parse(respuestasGuardadas)
      console.log('Respuestas restauradas de localStorage:', respuestas.value)
    }

    // Verificar si hay una finalización de test pendiente
    const pendingFinalization = localStorage.getItem('pendingTestFinalization')
    if (pendingFinalization === 'true' && authStore.isAuthenticated && respuestasGuardadas) {
      console.log('Finalización de test pendiente detectada, procediendo automáticamente...')

      // Limpiar el indicador
      localStorage.removeItem('pendingTestFinalization')

      // Proceder con la finalización automática
      try {
        // Simular click en finalizar para procesar automáticamente
        await finalizarTestAutomaticamente()
      } catch (error) {
        console.error('Error en finalización automática:', error)
        $q.notify({
          type: 'negative',
          message: 'Error al finalizar el test automáticamente',
          icon: 'error'
        })
      }
    }
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: error.message || 'Error al cargar el test'
    })
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.test-page {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  padding: 40px 20px;
}

.container {
  max-width: 900px;
  margin: 0 auto;
}

/* Header */
.test-header {
  background: white;
  border-radius: 20px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
}

.test-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: #5B21B6;
  margin: 0 0 20px 0;
  text-align: center;
}

.progress-info {
  text-align: center;
}

.progress-text {
  font-size: 1.2rem;
  color: #6B7280;
  margin-bottom: 15px;
}

.progress-text strong {
  color: #5B21B6;
  font-size: 1.4rem;
}

.progress-dots {
  display: flex;
  justify-content: center;
  gap: 8px;
  flex-wrap: wrap;
}

.progress-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #E5E7EB;
  transition: all 0.3s ease;
}

.progress-dot.active {
  background: #7C3AED;
  transform: scale(1.2);
}

.progress-dot.completed {
  background: #10B981;
}

/* Questions Container */
.questions-container {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.question-card {
  background: white;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.question-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
}

.question-number {
  font-size: 0.9rem;
  font-weight: 700;
  color: #7C3AED;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 20px;
}

.question-options {
  display: flex;
  align-items: center;
  gap: 20px;
}

.option-label {
  flex: 1;
  font-size: 1.1rem;
  font-weight: 600;
  color: #374151;
  line-height: 1.4;
}

.option-label.left {
  text-align: right;
}

.option-label.right {
  text-align: left;
}

/* Bubbles Selector */
.bubbles-selector {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  padding: 10px;
}

.bubble {
  border-radius: 50%;
  background: #E5E7EB;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.bubble:hover {
  background: #D1D5DB;
  transform: scale(1.1);
}

.bubble.selected {
  background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%);
  box-shadow: 0 4px 20px rgba(124, 58, 237, 0.4);
  transform: scale(1.15);
}

.bubble-inner {
  width: 70%;
  height: 70%;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
}

.bubble.selected .bubble-inner {
  background: rgba(255, 255, 255, 0.5);
}

/* Loading */
.loading-container {
  background: white;
  border-radius: 20px;
  padding: 60px;
  text-align: center;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
}

.loading-container p {
  margin-top: 20px;
  font-size: 1.2rem;
  color: #6B7280;
}

/* Navigation Buttons */
.navigation-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 40px;
  gap: 20px;
}

.nav-btn {
  font-size: 1.1rem;
  padding: 14px 32px;
  border-radius: 12px;
  font-weight: 600;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.nav-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.finish-btn {
  background: linear-gradient(135deg, #10B981 0%, #059669 100%);
}

/* Responsive */
@media (max-width: 768px) {
  .test-title {
    font-size: 1.8rem;
  }

  .question-options {
    flex-direction: column;
    gap: 15px;
  }

  .option-label.left,
  .option-label.right {
    text-align: center;
  }

  .bubbles-selector {
    gap: 10px;
  }

  .navigation-buttons {
    flex-direction: column;
  }

  .nav-btn {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .test-page {
    padding: 20px 10px;
  }

  .test-header,
  .question-card {
    padding: 20px;
  }

  .test-title {
    font-size: 1.5rem;
  }

  .option-label {
    font-size: 1rem;
  }

  .bubbles-selector {
    gap: 8px;
  }
}
</style>
