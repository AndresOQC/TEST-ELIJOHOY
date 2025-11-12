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
          <div class="brand-container" @click="$router.push('/')" style="cursor: pointer;">
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
            label="Inicio"
            class="nav-link"
            @click="scrollToSection('hero')"
          />
          <q-btn
            flat
            no-caps
            label="Características"
            class="nav-link"
            @click="scrollToSection('features')"
          />
          <q-btn
            flat
            no-caps
            label="Cómo Funciona"
            class="nav-link"
            @click="scrollToSection('how-it-works')"
          />
          <q-btn
            flat
            no-caps
            label="FAQ"
            class="nav-link"
            @click="scrollToSection('faq')"
          />
          <q-btn
            flat
            no-caps
            label="Contacto"
            class="nav-link"
            @click="scrollToSection('contact')"
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
        <!-- Navigation Links -->
        <q-item
          clickable
          v-ripple
          @click="scrollToSection('hero'); drawer = false"
        >
          <q-item-section avatar>
            <q-icon name="home" color="primary" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Inicio</q-item-label>
          </q-item-section>
        </q-item>

        <q-item
          clickable
          v-ripple
          @click="scrollToSection('features'); drawer = false"
        >
          <q-item-section avatar>
            <q-icon name="verified" color="primary" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Características</q-item-label>
          </q-item-section>
        </q-item>

        <q-item
          clickable
          v-ripple
          @click="scrollToSection('how-it-works'); drawer = false"
        >
          <q-item-section avatar>
            <q-icon name="timeline" color="primary" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Cómo Funciona</q-item-label>
          </q-item-section>
        </q-item>


        <q-item
          clickable
          v-ripple
          @click="scrollToSection('faq'); drawer = false"
        >
          <q-item-section avatar>
            <q-icon name="help" color="primary" />
          </q-item-section>
          <q-item-section>
            <q-item-label>FAQ</q-item-label>
          </q-item-section>
        </q-item>

        <q-item
          clickable
          v-ripple
          @click="scrollToSection('contact'); drawer = false"
        >
          <q-item-section avatar>
            <q-icon name="contact_mail" color="primary" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Contacto</q-item-label>
          </q-item-section>
        </q-item>

        <q-separator class="q-my-md" />

        <!-- Auth Links -->
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

        <!-- Quick Test Link -->
        <q-item
          clickable
          v-ripple
          to="/test"
        >
          <q-item-section avatar>
            <q-icon name="quiz" color="secondary" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Hacer Test</q-item-label>
            <q-item-label caption>Comienza tu evaluación</q-item-label>
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

    const scrollToSection = (sectionId) => {
      // Si estamos en la página de landing, hacer scroll
      if (window.location.pathname === '/' || window.location.pathname === '/#') {
        const element = document.getElementById(sectionId)
        if (element) {
          element.scrollIntoView({ behavior: 'smooth', block: 'start' })
        }
      } else {
        // Si no estamos en landing, ir a landing con el hash
        window.location.href = `/#${sectionId}`
      }
    }

    return {
      drawer,
      scrollToSection
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
  min-height: clamp(3rem, 6vh, 3.5rem);
  padding: 0 clamp(0.5rem, 1.5vw, 0.75rem);
  position: relative;
  z-index: 1;
  margin: 0;
}

.mobile-menu-btn {
  background: rgba(124, 58, 237, 0.1);
  color: #7C3AED;
  border-radius: clamp(0.625rem, 2vw, 0.75rem);
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
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  padding: clamp(0.25rem, 0.5vw, 0.35rem) clamp(0.4rem, 1vw, 0.5rem);
  border-radius: clamp(0.5rem, 1.5vw, 0.625rem);
  position: relative;
}

.brand-container:hover {
  background: rgba(124, 58, 237, 0.08);
  transform: translateY(-0.0625rem);
  box-shadow: 0 0.25rem 0.75rem rgba(124, 58, 237, 0.15);
}

.brand-icon-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.brand-icon {
  color: #7C3AED;
  filter: drop-shadow(0 0.125rem 0.5rem rgba(124, 58, 237, 0.3));
  z-index: 2;
  position: relative;
  font-size: clamp(1.25rem, 3vw, 1.75rem) !important;
}

.icon-pulse {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: clamp(2rem, 5vw, 2.5rem);
  height: clamp(2rem, 5vw, 2.5rem);
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
  margin-left: clamp(0.35rem, 1vw, 0.5rem);
}

.brand-name {
  font-size: clamp(1rem, 2.5vw, 1.35rem);
  font-weight: 800;
  line-height: 1.2;
  background: linear-gradient(135deg, #7C3AED 0%, #3B82F6 50%, #06B6D4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.1);
}

.brand-tagline {
  font-size: clamp(0.6rem, 1vw, 0.7rem);
  font-weight: 500;
  color: #64748b;
  margin-top: -0.125rem;
  opacity: 0.8;
}

.nav-links {
  display: flex;
  gap: clamp(0.25rem, 1vw, 0.5rem);
}

.nav-link {
  color: #475569;
  font-weight: 500;
  padding: clamp(0.3rem, 0.8vw, 0.4rem) clamp(0.5rem, 1.5vw, 0.75rem);
  border-radius: clamp(0.35rem, 1vw, 0.4rem);
  font-size: clamp(0.75rem, 1vw, 0.85rem);
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
  gap: clamp(0.35rem, 1vw, 0.5rem);
  align-items: center;
}

.login-btn {
  color: #7C3AED;
  font-weight: 600;
  padding: clamp(0.4rem, 1vw, 0.5rem) clamp(0.65rem, 2vw, 0.875rem);
  border-radius: clamp(0.5rem, 1.5vw, 0.625rem);
  font-size: clamp(0.75rem, 1vw, 0.85rem);
  border: 0.125rem solid transparent;
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
  transform: translateY(-0.125rem);
  box-shadow: 0 0.5rem 1.5625rem rgba(124, 58, 237, 0.15);
}

.login-btn:hover::before {
  opacity: 1;
}

.register-btn {
  background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%);
  color: white;
  font-weight: 600;
  padding: clamp(0.4rem, 1vw, 0.5rem) clamp(0.75rem, 2.5vw, 1rem);
  border-radius: clamp(0.5rem, 1.5vw, 0.625rem);
  font-size: clamp(0.75rem, 1vw, 0.85rem);
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
  transform: translateY(-0.125rem);
  box-shadow: 0 0.75rem 2.1875rem rgba(124, 58, 237, 0.3);
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

/* Mobile Responsiveness con unidades fluidas */
@media (max-width: 48rem) {
  .landing-toolbar {
    padding: 0 clamp(0.4rem, 1.5vw, 0.6rem);
  }
  
  .brand-tagline {
    display: none;
  }
}
</style>