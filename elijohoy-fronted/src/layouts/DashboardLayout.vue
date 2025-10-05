<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="dashboard-header">
      <q-toolbar class="dashboard-toolbar">
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
          class="menu-btn q-mr-sm"
          color="white"
        >
          <q-tooltip class="bg-white text-primary">Menú de navegación</q-tooltip>
        </q-btn>

        <q-toolbar-title class="dashboard-title">
          <div class="brand-container">
            <div class="brand-icon-wrapper">
              <q-icon name="school" size="36px" class="brand-icon q-mr-sm" />
              <div class="icon-glow"></div>
            </div>
            <div class="brand-text">
              <div class="brand-name">ElijoHoy</div>
              <div class="brand-subtitle">Dashboard Estudiantil</div>
            </div>
          </div>
        </q-toolbar-title>

        <q-space />


        <!-- User Profile Menu -->
        <q-btn-dropdown
          flat
          no-caps
          class="user-dropdown"
          dropdown-icon="expand_more"
        >
          <template v-slot:label>
            <div class="user-profile-label">
              <q-avatar size="38px" class="user-avatar-icon">
                <q-icon name="home" size="20px" color="white" />
              </q-avatar>
              <div class="user-info gt-xs">
                <div class="user-status">En línea</div>
              </div>
              <q-icon name="expand_more" size="18px" class="dropdown-arrow" />
            </div>
          </template>

          <q-list>
            <q-item-label header class="text-purple-10 text-weight-bold">
              {{ authStore.userName }}
            </q-item-label>

            <q-separator />

            <q-item clickable v-close-popup @click="goToSettings">
              <q-item-section avatar>
                <q-icon name="settings" color="purple-7" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Configuraciones</q-item-label>
              </q-item-section>
            </q-item>

            <q-separator />

            <q-item clickable v-close-popup @click="showLogoutDialog = true">
              <q-item-section avatar>
                <q-icon name="logout" color="negative" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Cerrar Sesión</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-btn-dropdown>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      :width="260"
      :breakpoint="1024"
      bordered
      class="dashboard-drawer"
    >
      <q-scroll-area class="fit">
        <div class="q-pa-md">
          <div class="drawer-header q-mb-md">
            <div class="text-h6 text-weight-bold text-purple-10">Menú Principal</div>
            <div class="text-caption text-grey-7">Panel de Control</div>
          </div>

          <q-list class="menu-list">
            <q-item
              clickable
              :active="$route.path === '/dashboard'"
              @click="$router.push('/dashboard')"
              active-class="active-menu-item"
              class="menu-item"
            >
              <q-item-section avatar>
                <q-icon name="dashboard" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Dashboard</q-item-label>
                <q-item-label caption>Vista general</q-item-label>
              </q-item-section>
            </q-item>

            <q-item
              clickable
              :active="$route.path === '/dashboard/test-resultados'"
              @click="$router.push('/dashboard/test-resultados')"
              active-class="active-menu-item"
              class="menu-item"
            >
              <q-item-section avatar>
                <q-icon name="quiz" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Test Resultados</q-item-label>
                <q-item-label caption>Tus resultados</q-item-label>
              </q-item-section>
            </q-item>

            <q-item
              clickable
              :active="$route.path === '/dashboard/configuraciones'"
              @click="$router.push('/dashboard/configuraciones')"
              active-class="active-menu-item"
              class="menu-item"
            >
              <q-item-section avatar>
                <q-icon name="settings" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Configuraciones</q-item-label>
                <q-item-label caption>Ajustes</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </div>

        <q-separator class="q-my-md" />

        <div class="q-pa-md">
          <q-btn
            unelevated
            color="purple-7"
            icon="arrow_back"
            label="Volver al Inicio"
            @click="$router.push('/')"
            class="full-width"
            no-caps
          />
        </div>
      </q-scroll-area>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

    <ConfirmDialog
      v-model="showLogoutDialog"
      title="Cerrar Sesión"
      message="¿Estás seguro que deseas cerrar sesión?"
      icon="logout"
      @ok="confirmLogout"
    />
  </q-layout>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import ConfirmDialog from 'src/components/common/ConfirmDialog.vue'
import { Notify } from 'quasar'
import { useAuthStore } from 'src/stores/auth'

export default defineComponent({
  name: 'DashboardLayout',
  components: {
    ConfirmDialog
  },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const leftDrawerOpen = ref(false)
    const showLogoutDialog = ref(false)

    const toggleLeftDrawer = () => {
      leftDrawerOpen.value = !leftDrawerOpen.value
    }

    const goToSettings = () => {
      router.push('/dashboard/configuraciones')
    }

    const confirmLogout = () => {
      authStore.logout()
      Notify.create({
        message: 'Sesión cerrada exitosamente',
        color: 'positive',
        icon: 'check_circle',
        position: 'top'
      })
      router.push('/auth/login')
    }

    // Check authentication on mount
    onMounted(() => {
      if (!authStore.isAuthenticated) {
        router.push('/auth/login')
      }
    })

    return {
      leftDrawerOpen,
      authStore,
      toggleLeftDrawer,
      goToSettings,
      showLogoutDialog,
      confirmLogout
    }
  }
})
</script>

<style scoped>
.dashboard-header {
  background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 50%, #3B82F6 100%);
  color: white;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
}

.dashboard-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, rgba(255, 255, 255, 0.1) 0%, transparent 50%, rgba(255, 255, 255, 0.05) 100%);
  pointer-events: none;
}

.dashboard-toolbar {
  min-height: 70px;
  padding: 0 24px;
  position: relative;
  z-index: 1;
}

.menu-btn {
  background: rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.menu-btn:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: scale(1.05);
}

.dashboard-title {
  flex: 1;
}

.brand-container {
  display: flex;
  align-items: center;
}

.brand-icon-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.brand-icon {
  filter: drop-shadow(0 2px 8px rgba(0, 0, 0, 0.3));
  z-index: 2;
  position: relative;
}

.icon-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 40px;
  height: 40px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.3) 0%, transparent 70%);
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 0.5; transform: translate(-50%, -50%) scale(1); }
  50% { opacity: 0.8; transform: translate(-50%, -50%) scale(1.1); }
}

.brand-text {
  display: flex;
  flex-direction: column;
  margin-left: 12px;
}

.brand-name {
  font-size: 1.4rem;
  font-weight: 700;
  line-height: 1.2;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  background: linear-gradient(45deg, #ffffff, #e0e7ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.brand-subtitle {
  font-size: 0.75rem;
  font-weight: 400;
  opacity: 0.85;
  margin-top: -2px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.notification-btn {
  background: rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.notification-btn:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: scale(1.05);
}

.user-dropdown {
  background: rgba(255, 255, 255, 0.15);
  border-radius: 25px;
  padding: 4px 16px 4px 4px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.user-dropdown:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-1px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.user-profile-label {
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-avatar-icon {
  position: relative;
  background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%);
  border: 2px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
}

.user-avatar-icon:hover {
  border-color: rgba(255, 255, 255, 0.6);
  background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
  transform: scale(1.05);
}

.avatar-border {
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  border-radius: 50%;
  background: linear-gradient(45deg, rgba(255, 255, 255, 0.6), transparent, rgba(255, 255, 255, 0.3));
  z-index: -1;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.user-name {
  font-weight: 600;
  font-size: 0.9rem;
  line-height: 1.2;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.user-status {
  font-size: 0.7rem;
  opacity: 0.8;
  font-weight: 400;
}

.dropdown-arrow {
  transition: transform 0.3s ease;
  opacity: 0.8;
}

.user-dropdown[aria-expanded="true"] .dropdown-arrow {
  transform: rotate(180deg);
}

.dashboard-drawer {
  background: #FAFAFA;
}

.drawer-header {
  border-bottom: 2px solid #7C3AED;
  padding-bottom: 12px;
}

.menu-list {
  background: transparent;
}

.menu-item {
  border-radius: 12px;
  margin-bottom: 8px;
  transition: all 0.3s ease;
}

.menu-item:hover {
  background: rgba(124, 58, 237, 0.1);
}

.active-menu-item {
  background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%) !important;
  color: white !important;
}

.active-menu-item :deep(.q-item__section),
.active-menu-item :deep(.q-item__label) {
  color: white !important;
}

/* Mobile Responsiveness */
@media (max-width: 1023px) {
  .dashboard-drawer {
    width: 280px !important;
  }
}

@media (max-width: 768px) {
  .dashboard-toolbar {
    padding: 0 16px;
    min-height: 64px;
  }
  
  .brand-name {
    font-size: 1.2rem;
  }
  
  .brand-subtitle {
    font-size: 0.7rem;
  }
  
  .user-info {
    display: none;
  }
  
  .notification-btn {
    display: none;
  }
}

@media (max-width: 480px) {
  .brand-text {
    margin-left: 8px;
  }
  
  .brand-name {
    font-size: 1.1rem;
  }
  
  .brand-subtitle {
    display: none;
  }
  
  .user-dropdown {
    padding: 4px 8px 4px 4px;
  }
}
</style>
