<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="landing-header">
      <q-toolbar class="landing-toolbar">
        <q-btn
          flat
          dense
          round
          icon="menu"
          class="mobile-menu-btn q-mr-sm lt-md"
          @click="drawer = !drawer"
        />

        <q-toolbar-title class="landing-title">
          <div class="brand-container">
            <div class="brand-icon-wrapper">
              <q-icon name="school" size="36px" class="brand-icon q-mr-sm" />
              <div class="icon-pulse"></div>
            </div>
            <div class="brand-text">
              <span class="brand-name">ElijoHoy</span>
              <span class="brand-tagline">Tu futuro comienza aquí</span>
            </div>
          </div>
        </q-toolbar-title>

        <q-space />

        <!-- Navigation Links for Desktop -->
        <div class="nav-links gt-sm q-mr-lg">
          <q-btn
            flat
            no-caps
            label="Características"
            class="nav-link"
          />
          <q-btn
            flat
            no-caps
            label="Precios"
            class="nav-link"
          />
          <q-btn
            flat
            no-caps
            label="Contacto"
            class="nav-link"
          />
        </div>

        <!-- Auth Buttons -->
        <div class="auth-buttons gt-sm">
          <q-btn
            flat
            no-caps
            label="Iniciar Sesión"
            icon="login"
            to="/auth/login"
            class="login-btn q-mr-sm"
          />

          <q-btn
            unelevated
            no-caps
            label="Registrarse"
            icon="person_add"
            to="/auth/registro"
            class="register-btn"
          />
        </div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-if="$q.screen.lt.md"
      v-model="drawer"
      behavior="mobile"
      :breakpoint="1024"
      side="left"
      bordered
    >
      <q-list padding>
        <q-item
          clickable
          v-ripple
          to="/auth/login"
        >
          <q-item-section avatar>
            <q-icon name="login" color="primary" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Iniciar Sesión</q-item-label>
          </q-item-section>
        </q-item>

        <q-item
          clickable
          v-ripple
          to="/auth/registro"
        >
          <q-item-section avatar>
            <q-icon name="person_add" color="primary" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Registrarse</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue'

export default defineComponent({
  name: 'LandingLayout',
  setup() {
    const drawer = ref(false)

    return {
      drawer
    }
  }
})
</script>

<style scoped>
.landing-header {
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  color: #1e293b;
  border-bottom: 1px solid rgba(148, 163, 184, 0.2);
  position: sticky;
  top: 0;
  z-index: 1000;
  backdrop-filter: blur(10px) saturate(180%);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.landing-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent 0%, rgba(124, 58, 237, 0.03) 50%, transparent 100%);
  pointer-events: none;
}

.landing-toolbar {
  min-height: 64px;
  padding: 0 24px;
  position: relative;
  z-index: 1;
  margin: 0;
}

.mobile-menu-btn {
  background: rgba(124, 58, 237, 0.1);
  color: #7C3AED;
  border-radius: 12px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.mobile-menu-btn:hover {
  background: rgba(124, 58, 237, 0.2);
  transform: scale(1.05);
}

.landing-title {
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
  color: #7C3AED;
  filter: drop-shadow(0 2px 8px rgba(124, 58, 237, 0.3));
  z-index: 2;
  position: relative;
}

.icon-pulse {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 40px;
  height: 40px;
  background: radial-gradient(circle, rgba(124, 58, 237, 0.2) 0%, transparent 70%);
  border-radius: 50%;
  animation: pulse-landing 3s infinite;
}

@keyframes pulse-landing {
  0%, 100% { opacity: 0.3; transform: translate(-50%, -50%) scale(1); }
  50% { opacity: 0.6; transform: translate(-50%, -50%) scale(1.2); }
}

.brand-text {
  display: flex;
  flex-direction: column;
  margin-left: 12px;
}

.brand-name {
  font-size: 1.6rem;
  font-weight: 800;
  line-height: 1.2;
  background: linear-gradient(135deg, #7C3AED 0%, #3B82F6 50%, #06B6D4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.brand-tagline {
  font-size: 0.75rem;
  font-weight: 500;
  color: #64748b;
  margin-top: -2px;
  opacity: 0.8;
}

.nav-links {
  display: flex;
  gap: 8px;
}

.nav-link {
  color: #475569;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 8px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.nav-link::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(124, 58, 237, 0.1), transparent);
  transition: left 0.5s;
}

.nav-link:hover {
  color: #7C3AED;
  background: rgba(124, 58, 237, 0.05);
  transform: translateY(-1px);
}

.nav-link:hover::before {
  left: 100%;
}

.auth-buttons {
  display: flex;
  gap: 12px;
  align-items: center;
}

.login-btn {
  color: #7C3AED;
  font-weight: 600;
  padding: 10px 20px;
  border-radius: 12px;
  border: 2px solid transparent;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.login-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(124, 58, 237, 0.1), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.login-btn:hover {
  border-color: rgba(124, 58, 237, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(124, 58, 237, 0.15);
}

.login-btn:hover::before {
  opacity: 1;
}

.register-btn {
  background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%);
  color: white;
  font-weight: 600;
  padding: 10px 24px;
  border-radius: 12px;
  border: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.register-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.6s;
}

.register-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 35px rgba(124, 58, 237, 0.3);
}

.register-btn:hover::before {
  left: 100%;
}

/* Remove any unwanted spacing */
:deep(.q-page-container) {
  padding-top: 0 !important;
  margin-top: 0 !important;
}

:deep(.q-page) {
  padding-top: 0 !important;
  margin-top: 0 !important;
}

/* Mobile Responsiveness */
@media (max-width: 768px) {
  .landing-toolbar {
    padding: 0 16px;
    min-height: 60px;
  }
  
  .brand-name {
    font-size: 1.3rem;
  }
  
  .brand-tagline {
    font-size: 0.7rem;
  }
}
</style>