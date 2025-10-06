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
  background: linear-gradient(135deg,
    rgba(99, 102, 241, 0.05) 0%,
    rgba(236, 72, 153, 0.05) 50%,
    rgba(245, 158, 11, 0.05) 100%);
  min-height: calc(100vh - 64px);
  padding: 24px;
}

.welcome-card {
  border-radius: 24px;
  background: linear-gradient(135deg,
    rgba(99, 102, 241, 0.9) 0%,
    rgba(236, 72, 153, 0.9) 50%,
    rgba(245, 158, 11, 0.9) 100%);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  color: white;
  box-shadow:
    0 20px 60px rgba(99, 102, 241, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
  position: relative;
  overflow: hidden;
}

.welcome-card::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(45deg,
    transparent 30%,
    rgba(255, 255, 255, 0.1) 50%,
    transparent 70%);
  transform: rotate(45deg) translate(-100%, -100%);
  transition: all 0.6s ease;
  opacity: 0;
}

.welcome-card:hover {
  transform: translateY(-8px);
  box-shadow:
    0 30px 80px rgba(99, 102, 241, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.welcome-card:hover::before {
  opacity: 1;
  transform: rotate(45deg) translate(100%, 100%);
}

.welcome-card :deep(.text-primary) {
  color: #FDB813 !important;
}

.welcome-card :deep(.text-grey-7) {
  color: rgba(255, 255, 255, 0.95) !important;
}

.profile-status-card,
.quick-actions-card,
.stats-card,
.activity-card {
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  position: relative;
  overflow: hidden;
}

.profile-status-card::before,
.quick-actions-card::before,
.stats-card::before,
.activity-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg,
    rgba(99, 102, 241, 0.05) 0%,
    rgba(236, 72, 153, 0.05) 50%,
    rgba(245, 158, 11, 0.05) 100%);
  opacity: 0;
  transition: opacity 0.4s ease;
}

.profile-status-card:hover,
.quick-actions-card:hover,
.stats-card:hover,
.activity-card:hover {
  transform: translateY(-8px);
  box-shadow:
    0 20px 60px rgba(0, 0, 0, 0.15),
    0 0 0 1px rgba(99, 102, 241, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.profile-status-card:hover::before,
.quick-actions-card:hover::before,
.stats-card:hover::before,
.activity-card:hover::before {
  opacity: 1;
}

.profile-status-card :deep(.text-primary),
.stats-card :deep(.text-primary),
.activity-card :deep(.text-primary) {
  color: #6366F1 !important;
}

.quick-actions-card :deep(.text-secondary) {
  color: #EC4899 !important;
}

.stats-card :deep(.text-secondary) {
  color: #F59E0B !important;
}

.stat-item {
  padding: 24px;
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.6) 0%,
    rgba(255, 255, 255, 0.3) 100%);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 20px;
  transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow:
    0 4px 16px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.stat-item:hover {
  transform: translateY(-4px) scale(1.02);
  background: linear-gradient(135deg,
    rgba(99, 102, 241, 0.1) 0%,
    rgba(236, 72, 153, 0.1) 100%);
  box-shadow:
    0 8px 32px rgba(99, 102, 241, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.profile-info {
  margin-top: 20px;
  padding: 20px;
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.6) 0%,
    rgba(255, 255, 255, 0.3) 100%);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow:
    inset 0 2px 4px rgba(0, 0, 0, 0.1),
    0 2px 8px rgba(255, 255, 255, 0.1);
}

.quick-actions-card :deep(.q-btn) {
  border-radius: 16px;
  font-weight: 600;
  padding: 14px 28px;
  transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  position: relative;
  overflow: hidden;
}

.quick-actions-card :deep(.q-btn::before) {
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

.quick-actions-card :deep(.q-btn:hover) {
  transform: translateY(-2px);
}

.quick-actions-card :deep(.q-btn:hover::before) {
  left: 100%;
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
    padding: 16px;
  }

  .welcome-card,
  .profile-status-card,
  .quick-actions-card,
  .stats-card,
  .activity-card {
    border-radius: 20px;
  }

  .stat-item {
    padding: 20px;
    margin-bottom: 16px;
  }

  /* Forzar columnas en móvil */
  .cards-horizontal-container {
    flex-direction: column;
    gap: 20px;
  }

  .card-half {
    flex: none;
  }
}
</style>