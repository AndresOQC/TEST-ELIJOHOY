<template>
  <q-page class="test-page">
    <div class="container">
      <!-- Header con título y progreso general -->
      <div class="test-header">
        <h1 class="test-title">Test de Personalidad</h1>
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
const BUBBLE_SIZES = [64, 48, 32, 48, 64] // Tamaños mejorados: grandes, medianas, pequeña, medianas, grandes

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
  background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
  min-height: 100vh;
  padding: 8px;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0.1px;
}

/* Header */
.test-header {
  text-align: center;
  margin-bottom: 8px;
}

.test-title {
  font-size: 2.5rem;
  font-weight: 800;
  background: linear-gradient(135deg,
    #6366F1 0%,
    #EC4899 50%,
    #F59E0B 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 2px;
  letter-spacing: -0.02em;
}

.progress-info {
  margin-top: 2px;
}

.progress-text {
  font-size: 1.1rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 16px;
}

.progress-text strong {
  background: linear-gradient(135deg, #6366F1, #EC4899);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 1.2rem;
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
  background: rgba(156, 163, 175, 0.3);
  transition: all 0.3s ease;
}

.progress-dot.active {
  background: linear-gradient(135deg, #6366F1, #EC4899);
  transform: scale(1.2);
}

.progress-dot.completed {
  background: linear-gradient(135deg, #10B981, #059669);
}

/* Questions Container */
.questions-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.question-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 24px;
  padding: 8px;
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
  position: relative;
  overflow: hidden;
}

.question-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg,
    rgba(99, 102, 241, 0.02) 0%,
    rgba(236, 72, 153, 0.02) 50%,
    rgba(245, 158, 11, 0.02) 100%);
  opacity: 0;
  transition: opacity 0.4s ease;
}

.question-card:hover {
  transform: translateY(-4px);
  box-shadow:
    0 20px 60px rgba(0, 0, 0, 0.15),
    0 0 0 1px rgba(99, 102, 241, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.question-card:hover::before {
  opacity: 1;
}

.question-number {
  font-size: 0.95rem;
  font-weight: 700;
  background: linear-gradient(135deg, #6366F1, #EC4899);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 12px;
  text-align: center;
}

.question-options {
  display: flex;
  align-items: center;
  gap: 32px;
}

.option-label {
  flex: 1;
  font-size: 1.2rem;
  font-weight: 600;
  color: #1F2937;
  line-height: 1.5;
  padding: 16px;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
}

.option-label.left {
  text-align: right;
  background: linear-gradient(135deg,
    rgba(99, 102, 241, 0.1) 0%,
    rgba(99, 102, 241, 0.05) 100%);
}

.option-label.right {
  text-align: left;
  background: linear-gradient(135deg,
    rgba(245, 158, 11, 0.1) 0%,
    rgba(245, 158, 11, 0.05) 100%);
}

/* Bubbles Selector */
.bubbles-selector {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  padding: 16px;
  position: relative;
  margin: 16px 0;
}

.bubble {
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.8) 0%, rgba(255, 255, 255, 0.6) 100%);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  box-shadow:
    0 4px 16px rgba(0, 0, 0, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.6);
  border: 2px solid rgba(255, 255, 255, 0.4);
  overflow: hidden;
}

.bubble::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 50%;
  background: linear-gradient(135deg,
    rgba(156, 163, 175, 0.1) 0%,
    rgba(209, 213, 219, 0.1) 100%);
  opacity: 0;
  transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
  z-index: -1;
}

.bubble:hover {
  transform: scale(1.08);
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.12),
    0 0 0 1px rgba(99, 102, 241, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.7);
  border-color: rgba(99, 102, 241, 0.3);
}

.bubble:hover::before {
  opacity: 0.6;
  background: linear-gradient(135deg,
    rgba(59, 130, 246, 0.15) 0%,
    rgba(99, 102, 241, 0.15) 100%);
}

.bubble.selected {
  background: linear-gradient(135deg,
    rgba(59, 130, 246, 0.95) 0%,
    rgba(99, 102, 241, 0.95) 100%);
  box-shadow:
    0 8px 32px rgba(59, 130, 246, 0.4),
    0 0 0 3px rgba(255, 255, 255, 0.6),
    inset 0 1px 0 rgba(255, 255, 255, 0.4);
  border-color: rgba(255, 255, 255, 0.6);
  transform: scale(1.12);
  animation: bubble-selected-glow 2s ease-in-out infinite;
}

.bubble.selected::before {
  opacity: 1;
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.3) 0%,
    rgba(255, 255, 255, 0.1) 100%);
  animation: bubble-selected-rotate 3s linear infinite;
}

@keyframes bubble-selected-glow {
  0%, 100% {
    box-shadow:
      0 8px 32px rgba(59, 130, 246, 0.4),
      0 0 0 3px rgba(255, 255, 255, 0.6),
      inset 0 1px 0 rgba(255, 255, 255, 0.4);
  }
  50% {
    box-shadow:
      0 12px 40px rgba(59, 130, 246, 0.6),
      0 0 0 4px rgba(255, 255, 255, 0.8),
      inset 0 1px 0 rgba(255, 255, 255, 0.5);
  }
}

@keyframes bubble-selected-rotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.bubble-inner {
  border-radius: 50%;
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.4) 0%,
    rgba(255, 255, 255, 0.2) 100%);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
  box-shadow:
    inset 0 2px 4px rgba(0, 0, 0, 0.1),
    0 2px 8px rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.bubble.selected .bubble-inner {
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.7) 0%,
    rgba(255, 255, 255, 0.4) 100%);
  transform: scale(0.9);
  box-shadow:
    inset 0 4px 8px rgba(0, 0, 0, 0.15),
    0 4px 16px rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
}

/* Loading */
.loading-container {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 24px;
  padding: 60px;
  text-align: center;
  box-shadow:
    0 20px 60px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.loading-container p {
  margin-top: 24px;
  font-size: 1.2rem;
  font-weight: 600;
  color: #4B5563;
  background: linear-gradient(135deg, #6366F1, #EC4899);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Navigation Buttons */
.navigation-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 40px;
  gap: 24px;
}

.nav-btn {
  font-size: 1.1rem;
  padding: 16px 36px;
  border-radius: 16px;
  font-weight: 600;
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  position: relative;
  overflow: hidden;
}

.nav-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg,
    transparent,
    rgba(255, 255, 255, 0.2),
    transparent);
  transition: left 0.6s ease;
}

.nav-btn:hover:not(:disabled) {
  transform: translateY(-4px);
  box-shadow:
    0 20px 60px rgba(0, 0, 0, 0.15),
    0 0 0 1px rgba(99, 102, 241, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.nav-btn:hover:not(:disabled)::before {
  left: 100%;
}

.nav-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.finish-btn {
  background: linear-gradient(135deg,
    rgba(16, 185, 129, 0.9) 0%,
    rgba(5, 150, 105, 0.9) 100%);
  color: white;
}

.finish-btn:hover:not(:disabled) {
  background: linear-gradient(135deg,
    rgba(16, 185, 129, 1) 0%,
    rgba(5, 150, 105, 1) 100%);
  box-shadow:
    0 20px 60px rgba(16, 185, 129, 0.3),
    0 0 0 1px rgba(16, 185, 129, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

/* Responsive */
@media (max-width: 768px) {
  .test-page {
    padding: 10px;
  }

  .test-header {
    margin-bottom: 12px;
  }

  .test-title {
    font-size: 2rem;
  }

  .question-card {
    padding: 10px;
  }

  .question-options {
    flex-direction: column;
    gap: 24px;
  }

  .option-label.left,
  .option-label.right {
    text-align: center;
    padding: 12px;
    font-size: 1.1rem;
  }

  .bubbles-selector {
    gap: 16px;
    padding: 12px;
    margin: 12px 0;
  }

  .bubble {
    width: 70px;
    height: 70px;
  }

  .navigation-buttons {
    flex-direction: column;
    gap: 16px;
  }

  .nav-btn {
    width: 100%;
    padding: 14px 24px;
  }
}

@media (max-width: 480px) {
  .test-page {
    padding: 12px;
  }

  .test-header {
    margin-bottom: 10px;
  }

  .test-title {
    font-size: 2rem;
  }

  .question-card {
    padding: 12px;
  }

  .question-number {
    font-size: 0.85rem;
    margin-bottom: 12px;
  }

  .option-label {
    font-size: 1rem;
    padding: 5px;
  }

  .bubbles-selector {
    gap: 12px;
    padding: 10px;
    margin: 10px 0;
  }

  .bubble {
    width: 60px;
    height: 60px;
  }

  .nav-btn {
    font-size: 1rem;
    padding: 12px 20px;
  }
}
</style>
