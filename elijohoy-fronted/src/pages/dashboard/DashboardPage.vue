<template>
  <q-page class="dashboard-page">
    <div class="dashboard-container">
      <!-- Welcome Section -->
      <q-card class="welcome-card" flat bordered>
        <q-card-section class="welcome-content">
          <div class="welcome-text">
            <div class="text-h4 text-weight-bold text-primary q-mb-sm">
              ¡Bienvenido de nuevo, {{ authStore.userName }}!
            </div>
            <div class="text-body1 text-grey-7">
              Estamos aquí para ayudarte a descubrir tu futuro académico y profesional.
            </div>
          </div>
          <div class="welcome-icon">
            <q-icon
              name="waving_hand"
              size="64px"
              color="warning"
            />
          </div>
        </q-card-section>
      </q-card>

      <!-- Profile & Actions Row -->
      <div class="cards-row">
        <!-- Profile Status -->
        <q-card class="profile-status-card" flat bordered>
          <q-card-section>
            <div class="card-header">
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
              <div class="chips-container">
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
        <q-card class="quick-actions-card" flat bordered>
          <q-card-section>
            <div class="card-header">
              <q-icon name="flash_on" size="32px" color="secondary" class="q-mr-sm" />
              <div class="text-h6 text-weight-bold">Acciones Rápidas</div>
            </div>

            <div class="actions-buttons">
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

      <!-- Statistics -->
      <q-card class="stats-card" flat bordered>
        <q-card-section>
          <div class="card-header">
            <q-icon name="analytics" size="32px" color="info" class="q-mr-sm" />
            <div class="text-h6 text-weight-bold">Tu Progreso</div>
          </div>

          <div class="stats-grid">
            <div class="stat-item">
              <div class="text-h3 text-weight-bold text-primary">0</div>
              <div class="text-body2 text-grey-7">Tests Completados</div>
            </div>

            <div class="stat-item">
              <div class="text-h3 text-weight-bold text-secondary">0</div>
              <div class="text-body2 text-grey-7">Carreras Exploradas</div>
            </div>

            <div class="stat-item">
              <div class="text-h3 text-weight-bold text-positive">{{ daysSinceRegistration }}</div>
              <div class="text-body2 text-grey-7">Días en ElijoHoy</div>
            </div>
          </div>
        </q-card-section>
      </q-card>

      <!-- Recent Activity -->
      <q-card class="activity-card" flat bordered>
        <q-card-section>
          <div class="card-header">
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
  min-height: 100vh;
  background: linear-gradient(135deg,
    rgba(99, 102, 241, 0.05) 0%,
    rgba(236, 72, 153, 0.05) 50%,
    rgba(245, 158, 11, 0.05) 100%);
  padding: 1.5rem;
  overflow-x: hidden;
}

.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Welcome Card */
.welcome-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
}

.welcome-text {
  flex: 1;
  min-width: 250px;
}

.welcome-icon {
  flex-shrink: 0;
}

/* Cards Row */
.cards-row {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.cards-row > .q-card {
  flex: 1 1 300px;
  min-width: 280px;
}

/* Card Header */
.card-header {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

/* Chips Container */
.chips-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

/* Actions Buttons */
.actions-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
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
  padding: clamp(0.875rem, 2.5vw, 1.25rem);
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.6) 0%,
    rgba(255, 255, 255, 0.3) 100%);
  backdrop-filter: blur(0.625rem);
  -webkit-backdrop-filter: blur(0.625rem);
  border-radius: clamp(0.75rem, 2vw, 1.25rem);
  transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow:
    0 0.25rem 1rem rgba(0, 0, 0, 0.1),
    inset 0 0.0625rem 0 rgba(255, 255, 255, 0.2);
}

.stat-item:hover {
  transform: translateY(-0.25rem) scale(1.02);
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

/* Responsive */
@media (max-width: 768px) {
  .dashboard-page {
    padding: 1rem;
  }

  .dashboard-container {
    gap: 1rem;
  }

  .cards-row {
    flex-direction: column;
    gap: 1rem;
  }

  .cards-row > .q-card {
    flex: 1 1 auto;
    min-width: 100%;
  }

  .welcome-card,
  .profile-status-card,
  .quick-actions-card,
  .stats-card,
  .activity-card {
    border-radius: 1.25rem;
  }

  .stat-item {
    padding: 1rem;
  }

  .text-h4 {
    font-size: 1.5rem;
  }

  .text-h6 {
    font-size: 1rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .dashboard-page {
    padding: 0.75rem;
  }

  .welcome-card,
  .profile-status-card,
  .quick-actions-card,
  .stats-card,
  .activity-card {
    border-radius: 1rem;
  }

  .text-h4 {
    font-size: 1.3rem;
  }

  .stat-item {
    padding: 0.875rem;
  }

  .text-h3 {
    font-size: 1.75rem;
  }

  .profile-info {
    padding: 0.875rem;
  }
}
</style>