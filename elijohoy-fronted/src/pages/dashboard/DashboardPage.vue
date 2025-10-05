<template>
  <q-page class="dashboard-page q-pa-lg">
    <div class="row q-gutter-lg">
      <!-- Welcome Section -->
      <div class="col-12">
        <q-card class="welcome-card" flat bordered>
          <q-card-section class="row items-center">
            <div class="col">
              <div class="text-h4 text-weight-bold text-primary q-mb-sm">
                ¡Bienvenido de nuevo, {{ authStore.userName }}!
              </div>
              <div class="text-body1 text-grey-7">
                Estamos aquí para ayudarte a descubrir tu futuro académico y profesional.
              </div>
            </div>
            <div class="col-auto">
              <q-icon 
                name="waving_hand" 
                size="64px" 
                color="warning"
                class="q-ml-md"
              />
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Profile & Actions Row -->
      <div class="col-12">
        <div class="cards-horizontal-container">
          <!-- Profile Status -->
          <q-card class="profile-status-card card-half" flat bordered>
            <q-card-section>
              <div class="row items-center q-mb-md">
                <q-icon name="person" size="32px" color="primary" class="q-mr-sm" />
                <div class="text-h6 text-weight-bold">Estado del Perfil</div>
              </div>
              
              <div class="q-mb-md">
                <div class="text-body2 text-grey-7 q-mb-xs">Completitud del perfil</div>
                <q-linear-progress 
                  :value="profileCompletion" 
                  size="12px" 
                  color="positive"
                  class="q-mb-xs"
                />
                <div class="text-caption text-right">{{ Math.round(profileCompletion * 100) }}%</div>
              </div>
              
              <div class="profile-info">
                <div class="row q-gutter-sm q-mb-sm">
                  <q-chip 
                    :color="user.email_verificado ? 'positive' : 'negative'"
                    :icon="user.email_verificado ? 'verified' : 'error'"
                    text-color="white"
                    size="sm"
                  >
                    Email {{ user.email_verificado ? 'Verificado' : 'No Verificado' }}
                  </q-chip>
                  
                  <q-chip 
                    :color="user.perfil_completo ? 'positive' : 'warning'"
                    :icon="user.perfil_completo ? 'check_circle' : 'pending'"
                    text-color="white"
                    size="sm"
                  >
                    Perfil {{ user.perfil_completo ? 'Completo' : 'Incompleto' }}
                  </q-chip>
                </div>
                
                <div class="text-body2">
                  <div><strong>Institución:</strong> {{ user.institucion_educativa || 'No especificada' }}</div>
                  <div><strong>Grado:</strong> {{ user.grado || 'No especificado' }}</div>
                </div>
              </div>
            </q-card-section>
          </q-card>

          <!-- Quick Actions -->
          <q-card class="quick-actions-card card-half" flat bordered>
            <q-card-section>
              <div class="row items-center q-mb-md">
                <q-icon name="flash_on" size="32px" color="secondary" class="q-mr-sm" />
                <div class="text-h6 text-weight-bold">Acciones Rápidas</div>
              </div>
              
              <div class="q-gutter-sm">
                <q-btn
                  unelevated
                  color="primary"
                  icon="quiz"
                  label="Ver Test Resultados"
                  @click="$router.push('/dashboard/test-resultados')"
                  class="full-width"
                  no-caps
                />
                
                <q-btn
                  outline
                  color="secondary"
                  icon="settings"
                  label="Configuraciones"
                  @click="$router.push('/dashboard/configuraciones')"
                  class="full-width"
                  no-caps
                />
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>

      <!-- Statistics -->
      <div class="col-12">
        <q-card class="stats-card" flat bordered>
          <q-card-section>
            <div class="row items-center q-mb-md">
              <q-icon name="analytics" size="32px" color="info" class="q-mr-sm" />
              <div class="text-h6 text-weight-bold">Tu Progreso</div>
            </div>
            
            <div class="row q-gutter-lg">
              <div class="col-12 col-sm-4 text-center">
                <div class="stat-item">
                  <div class="text-h3 text-weight-bold text-primary">0</div>
                  <div class="text-body2 text-grey-7">Tests Completados</div>
                </div>
              </div>
              
              <div class="col-12 col-sm-4 text-center">
                <div class="stat-item">
                  <div class="text-h3 text-weight-bold text-secondary">0</div>
                  <div class="text-body2 text-grey-7">Carreras Exploradas</div>
                </div>
              </div>
              
              <div class="col-12 col-sm-4 text-center">
                <div class="stat-item">
                  <div class="text-h3 text-weight-bold text-positive">{{ daysSinceRegistration }}</div>
                  <div class="text-body2 text-grey-7">Días en ElijoHoy</div>
                </div>
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Recent Activity -->
      <div class="col-12">
        <q-card class="activity-card" flat bordered>
          <q-card-section>
            <div class="row items-center q-mb-md">
              <q-icon name="history" size="32px" color="primary" class="q-mr-sm" />
              <div class="text-h6 text-weight-bold">Actividad Reciente</div>
            </div>
            
            <div class="text-center q-pa-lg">
              <q-icon name="inbox" size="64px" color="grey-5" class="q-mb-md" />
              <div class="text-h6 text-grey-6">No hay actividad reciente</div>
              <div class="text-body2 text-grey-5">
                Completa tu primer test vocacional para comenzar a ver tu actividad aquí
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, computed, onMounted } from 'vue'
import { useAuthStore } from 'src/stores/auth'

export default defineComponent({
  name: 'DashboardPage',

  setup() {
    const authStore = useAuthStore()

    const user = computed(() => authStore.user || {})

    const profileCompletion = computed(() => {
      const user = authStore.user
      if (!user) return 0

      let completed = 0
      const total = 6

      if (user.nombre_completo) completed++
      if (user.email_verificado) completed++
      if (user.institucion_educativa) completed++
      if (user.grado) completed++
      if (user.fecha_nacimiento) completed++
      if (user.perfil_completo) completed++

      return completed / total
    })

    const daysSinceRegistration = computed(() => {
      const user = authStore.user
      if (!user || !user.creado_en) return 0

      const createdDate = new Date(user.creado_en)
      const today = new Date()
      const diffTime = Math.abs(today - createdDate)
      return Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    })

    onMounted(async () => {
      // Solo refrescar datos del usuario si no los tenemos
      if (authStore.isAuthenticated && !authStore.user && sessionStorage.getItem('access_token')) {
        await authStore.refreshUser()
      }
    })

    return {
      authStore,
      user,
      profileCompletion,
      daysSinceRegistration
    }
  }
})
</script>

<style scoped>
.dashboard-page {
  max-width: 1200px;
  margin: 0 auto;
  background: linear-gradient(to bottom, #F3F4F6, #FFFFFF);
  min-height: calc(100vh - 64px);
}

.welcome-card {
  border-radius: 20px;
  background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%);
  color: white;
  box-shadow: 0 8px 32px rgba(124, 58, 237, 0.3);
  border: none !important;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.welcome-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(124, 58, 237, 0.4);
}

.welcome-card :deep(.text-primary) {
  color: #FDB813 !important;
}

.welcome-card :deep(.text-grey-7) {
  color: rgba(255, 255, 255, 0.9) !important;
}

.profile-status-card,
.quick-actions-card,
.stats-card,
.activity-card {
  border-radius: 20px;
  border: 2px solid #E5E7EB !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  background: white;
}

.profile-status-card:hover,
.quick-actions-card:hover,
.stats-card:hover,
.activity-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 32px rgba(124, 58, 237, 0.15);
  border-color: #7C3AED !important;
}

.profile-status-card :deep(.text-primary),
.stats-card :deep(.text-primary),
.activity-card :deep(.text-primary) {
  color: #7C3AED !important;
}

.quick-actions-card :deep(.text-secondary) {
  color: #5B21B6 !important;
}

.stats-card :deep(.text-secondary) {
  color: #EC4899 !important;
}

.stat-item {
  padding: 20px;
  background: linear-gradient(135deg, #F9FAFB 0%, #F3F4F6 100%);
  border-radius: 16px;
  transition: all 0.3s ease;
}

.stat-item:hover {
  transform: scale(1.05);
  background: linear-gradient(135deg, #EDE9FE 0%, #DDD6FE 100%);
}

.profile-info {
  margin-top: 16px;
  padding: 16px;
  background: linear-gradient(135deg, #F9FAFB 0%, #F3F4F6 100%);
  border-radius: 12px;
}

.quick-actions-card :deep(.q-btn) {
  border-radius: 12px;
  font-weight: 600;
  padding: 12px 24px;
  transition: all 0.3s ease;
}

.quick-actions-card :deep(.q-btn:hover) {
  transform: translateX(4px);
}

/* Contenedor horizontal para las tarjetas */
.cards-horizontal-container {
  display: flex;
  gap: 24px;
  width: 100%;
}

.card-half {
  flex: 1;
  min-width: 0;
}

@media (max-width: 768px) {
  .dashboard-page {
    padding: 12px;
  }

  .welcome-card,
  .profile-status-card,
  .quick-actions-card,
  .stats-card,
  .activity-card {
    border-radius: 16px;
  }

  .stat-item {
    padding: 16px;
    margin-bottom: 12px;
  }

  /* Forzar columnas en móvil */
  .cards-horizontal-container {
    flex-direction: column;
    gap: 16px;
  }
  
  .card-half {
    flex: none;
  }
}
</style>