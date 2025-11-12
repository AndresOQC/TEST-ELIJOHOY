<template>
  <q-page class="test-resultados-page q-pa-lg">
    <div class="row q-col-gutter-lg">
      <!-- Page Header -->
      <div class="col-12">
        <div class="page-header">
          <div class="row items-center">
            <q-icon name="quiz" size="48px" color="purple-7" class="q-mr-md" />
            <div>
              <h1 class="text-h4 text-weight-bold" style="color: #7C3AED;">
                Resultados de Tests
              </h1>
              <p class="text-body1 text-grey-7">
                {{ isAdmin ? 'Administra todos los tests realizados' : 'Tus tests vocacionales completados' }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Filtros y Estadísticas -->
      <div class="col-12" v-if="isAdmin">
        <q-card flat bordered class="q-mb-lg">
          <q-card-section>
            <div class="row q-gutter-md items-center">
              <div class="col-auto">
                <div class="text-h6 text-weight-bold">Estadísticas</div>
              </div>
              <div class="col-auto">
                <q-chip color="primary" text-color="white">
                  Total: {{ sesiones.length }}
                </q-chip>
              </div>
              <div class="col-auto">
                <q-chip color="positive" text-color="white">
                  Completados: {{ sesionesCompletadas.length }}
                </q-chip>
              </div>
              <div class="col-auto">
                <q-chip color="warning" text-color="white">
                  Pendientes: {{ sesionesPendientes.length }}
                </q-chip>
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Lista de Sesiones -->
      <div class="col-12">
        <q-card flat bordered>
          <q-card-section>
            <div v-if="loading" class="text-center q-py-xl">
              <q-spinner color="primary" size="50px" />
              <p class="text-body1 text-grey-7 q-mt-md">Cargando resultados...</p>
            </div>

            <div v-else-if="sesiones.length === 0" class="text-center q-py-xl">
              <q-icon name="quiz" size="80px" color="grey-5" class="q-mb-lg" />
              <div class="text-h6 text-grey-7 q-mb-md">
                {{ isAdmin ? 'No hay tests realizados aún' : 'No has completado ningún test aún' }}
              </div>
              <q-btn
                unelevated
                color="primary"
                icon="quiz"
                label="Realizar Test"
                @click="$router.push('/dashboard/test')"
                no-caps
              />
            </div>

            <div v-else class="sesiones-list">
              <q-list separator>
                <q-item
                  v-for="sesion in sesiones"
                  :key="sesion.id_sesion"
                  clickable
                  @click="verResultados(sesion)"
                  class="sesion-item"
                >
                  <q-item-section avatar>
                    <q-avatar size="48px">
                      <img :src="getAvatarUrl(sesion.tipo_personalidad)" alt="avatar" v-if="sesion.tipo_personalidad" />
                      <q-icon
                        v-else
                        :name="sesion.completado ? 'check_circle' : 'pending'"
                        :color="sesion.completado ? 'positive' : 'warning'"
                        size="32px"
                      />
                    </q-avatar>
                  </q-item-section>

                  <q-item-section>
                    <q-item-label class="text-weight-bold">
                      Test #{{ sesion.id_sesion }}
                      <q-badge
                        v-if="sesion.tipo_personalidad"
                        :color="getTipoColor(sesion.tipo_personalidad)"
                        class="q-ml-sm"
                      >
                        {{ sesion.tipo_personalidad }}
                      </q-badge>
                    </q-item-label>

                    <q-item-label caption>
                      <div class="row q-gutter-sm">
                        <span>📅 {{ formatDate(sesion.fecha_inicio) }}</span>
                        <span v-if="sesion.fecha_fin">⏱️ {{ formatDate(sesion.fecha_fin) }}</span>
                        <span v-if="isAdmin && sesion.usuario">
                          👤 {{ sesion.usuario.nombre }} {{ sesion.usuario.apellidos }}
                        </span>
                      </div>
                    </q-item-label>

                    <q-item-label caption v-if="sesion.completado && sesion.tipo">
                      {{ sesion.tipo.nombre }} - {{ sesion.tipo.descripcion_corta }}
                    </q-item-label>
                  </q-item-section>

                  <q-item-section side>
                    <div class="text-right">
                      <div class="text-caption text-grey-7">
                        {{ sesion.completado ? 'Completado' : 'Pendiente' }}
                      </div>
                      <q-btn
                        flat
                        dense
                        round
                        icon="arrow_forward"
                        color="primary"
                        @click.stop="verResultados(sesion)"
                      />
                    </div>
                  </q-item-section>
                </q-item>
              </q-list>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useAuthStore } from 'src/stores/auth'
import api from 'src/services/api'

const router = useRouter()
const $q = useQuasar()
const authStore = useAuthStore()

const loading = ref(false)
const sesiones = ref([])

const isAdmin = computed(() => {
  return authStore.user?.roles?.some(role => role.nombre === 'administrador') || false
})

const sesionesCompletadas = computed(() => {
  return sesiones.value.filter(s => s.completado)
})

const sesionesPendientes = computed(() => {
  return sesiones.value.filter(s => !s.completado)
})

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getAvatarUrl = (tipo) => {
  if (!tipo) return ''
  const encoded = encodeURIComponent(tipo)
  return `http://localhost:5001/avatars/${encoded}`
}

const getTipoColor = (tipo) => {
  const colors = {
    'INTJ': 'purple',
    'INTP': 'blue',
    'ENTJ': 'red',
    'ENTP': 'orange',
    'INFJ': 'pink',
    'INFP': 'green',
    'ENFJ': 'yellow',
    'ENFP': 'cyan',
    'ISTJ': 'brown',
    'ISFJ': 'teal',
    'ESTJ': 'deep-orange',
    'ESFJ': 'lime',
    'ISTP': 'indigo',
    'ISFP': 'light-green',
    'ESTP': 'amber',
    'ESFP': 'light-blue'
  }
  return colors[tipo] || 'grey'
}

const cargarSesiones = async () => {
  loading.value = true
  try {
    const response = await api.get('/test/mis-sesiones')
    if (response.data.success) {
      sesiones.value = response.data.sesiones
      console.log('Sesiones cargadas:', sesiones.value)
    } else {
      $q.notify({
        type: 'negative',
        message: 'Error al cargar sesiones',
        icon: 'error'
      })
    }
  } catch (error) {
    console.error('Error cargando sesiones:', error)
    $q.notify({
      type: 'negative',
      message: 'Error de conexión al cargar sesiones',
      icon: 'error'
    })
  } finally {
    loading.value = false
  }
}

const verResultados = (sesion) => {
  if (sesion.completado) {
    router.push(`/dashboard/test-resultados/${sesion.id_sesion}`)
  } else {
    $q.notify({
      type: 'warning',
      message: 'Este test aún no está completado',
      icon: 'warning'
    })
  }
}

onMounted(() => {
  cargarSesiones()
})
</script>

<style scoped>
.test-resultados-page {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: calc(100vh - 64px);
  height: 100%;
  padding: 24px;
}

.page-header {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  padding: 24px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.sesion-item {
  border-radius: 8px;
  margin-bottom: 8px;
  transition: all 0.2s ease;
}

.sesion-item:hover {
  background: rgba(255, 255, 255, 0.05);
}

.sesiones-list {
  max-height: 70vh;
  overflow-y: auto;
}

@media (max-width: 768px) {
  .test-resultados-page {
    min-height: calc(100vh - 60px);
    padding: 16px;
  }
  
  .page-header {
    padding: 16px;
  }
  
  .page-header h1 {
    font-size: 1.8rem;
  }
  
  .page-header .q-icon {
    font-size: 36px !important;
  }
  
  .sesiones-list {
    max-height: 65vh;
  }
}

@media (max-width: 480px) {
  .test-resultados-page {
    padding: 12px;
  }
  
  .page-header {
    padding: 12px;
  }
  
  .page-header h1 {
    font-size: 1.5rem;
  }
  
  .page-header .q-icon {
    font-size: 32px !important;
    margin-right: 8px !important;
  }
}

@media (max-height: 700px) {
  .test-resultados-page {
    padding: 16px;
  }
  
  .page-header {
    padding: 16px;
  }
  
  .page-header h1 {
    font-size: 1.4rem;
    margin-bottom: 4px !important;
  }
  
  .page-header p {
    font-size: 0.875rem;
  }
  
  .sesiones-list {
    max-height: 60vh;
  }
}
</style>