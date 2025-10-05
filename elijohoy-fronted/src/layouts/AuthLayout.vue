<template>
  <q-layout view="lHh Lpr lFf" class="auth-layout">
    <q-header class="auth-header">
      <q-toolbar class="auth-toolbar">
        <q-btn
          flat
          round
          icon="arrow_back"
          @click="$router.push('/')"
          class="back-btn"
          size="md"
        >
          <q-tooltip class="bg-purple-9 text-white">Volver al inicio</q-tooltip>
        </q-btn>
        
        <q-toolbar-title class="auth-title">
          <div class="brand-container">
            <div class="brand-logo">
              <q-icon name="psychology" size="28px" class="brand-icon" />
            </div>
            <div class="brand-text">
              <div class="brand-name">ElijoHoy</div>
              <div class="brand-subtitle">Descubre tu vocación</div>
            </div>
          </div>
        </q-toolbar-title>

        <q-space />

        <!-- Security indicator -->
        <div class="security-badge">
          <q-icon name="security" size="18px" class="security-icon" />
          <span class="security-text">Seguro</span>
        </div>
      </q-toolbar>
    </q-header>

    <q-page-container class="auth-page-container">
      <div class="auth-background">
        <!-- Formas decorativas del layout -->
        <div class="layout-shape layout-shape-1"></div>
        <div class="layout-shape layout-shape-2"></div>
        <div class="layout-shape layout-shape-3"></div>
        <div class="layout-shape layout-shape-4"></div>
        
        <!-- Contenido principal -->
        <div class="auth-content-wrapper">
          <router-view />
        </div>
      </div>
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'AuthLayout'
})
</script>

<style scoped>
.auth-layout {
  min-height: 100vh;
  background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 50%, #4C1D95 100%);
  position: relative;
  overflow: hidden;
}

.auth-header {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.12);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.auth-toolbar {
  min-height: 64px;
  padding: 0 24px;
  color: white;
}

.back-btn {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  border-radius: 12px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.brand-container {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-logo {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, rgba(253, 184, 19, 0.2), rgba(251, 146, 60, 0.2));
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid rgba(253, 184, 19, 0.3);
  box-shadow: 0 4px 16px rgba(253, 184, 19, 0.2);
}

.brand-icon {
  color: #FDB813;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

.brand-text {
  display: flex;
  flex-direction: column;
  line-height: 1.1;
}

.brand-name {
  font-size: 1.4rem;
  font-weight: 800;
  color: white;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  letter-spacing: -0.5px;
}

.brand-subtitle {
  font-size: 0.7rem;
  font-weight: 500;
  color: rgba(253, 184, 19, 0.9);
  margin-top: 1px;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.security-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  background: rgba(16, 185, 129, 0.15);
  color: #10B981;
  padding: 6px 12px;
  border-radius: 20px;
  border: 1px solid rgba(16, 185, 129, 0.3);
  backdrop-filter: blur(10px);
  font-size: 0.75rem;
  font-weight: 600;
}

.security-icon {
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

.security-text {
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

/* Contenedor principal mejorado */
.auth-page-container {
  position: relative;
  min-height: calc(100vh - 64px);
}

.auth-background {
  position: relative;
  min-height: 100%;
  overflow: hidden;
}

/* Formas decorativas del layout */
.layout-shape {
  position: absolute;
  border-radius: 50%;
  opacity: 0.06;
  pointer-events: none;
}

.layout-shape-1 {
  width: 400px;
  height: 400px;
  background: #FDB813;
  top: -100px;
  right: -100px;
  animation: float 6s ease-in-out infinite;
}

.layout-shape-2 {
  width: 300px;
  height: 300px;
  background: #EC4899;
  bottom: -80px;
  left: -80px;
  animation: float 8s ease-in-out infinite reverse;
}

.layout-shape-3 {
  width: 200px;
  height: 200px;
  background: #10B981;
  top: 60%;
  right: -50px;
  animation: float 7s ease-in-out infinite;
}

.layout-shape-4 {
  width: 150px;
  height: 150px;
  background: #8B5CF6;
  top: 20%;
  left: -40px;
  animation: float 9s ease-in-out infinite reverse;
}

.auth-content-wrapper {
  position: relative;
  z-index: 2;
  min-height: calc(100vh - 64px);
  padding: 0;
}

/* Animaciones */
@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(5deg);
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .auth-toolbar {
    padding: 0 16px;
    min-height: 60px;
  }
  
  .brand-container {
    gap: 8px;
  }
  
  .brand-logo {
    width: 40px;
    height: 40px;
  }
  
  .brand-icon {
    font-size: 22px !important;
  }
  
  .brand-name {
    font-size: 1.2rem;
  }
  
  .brand-subtitle {
    font-size: 0.65rem;
  }
  
  .security-badge {
    padding: 4px 8px;
    font-size: 0.7rem;
  }
  
  .security-text {
    display: none;
  }
  
  .layout-shape-1,
  .layout-shape-2,
  .layout-shape-3,
  .layout-shape-4 {
    width: 200px;
    height: 200px;
  }
  
  .auth-content-wrapper {
    min-height: calc(100vh - 60px);
  }
  
  .auth-page-container {
    min-height: calc(100vh - 60px);
  }
}

@media (max-width: 480px) {
  .auth-toolbar {
    padding: 0 12px;
  }
  
  .brand-container {
    gap: 6px;
  }
  
  .brand-logo {
    width: 36px;
    height: 36px;
  }
  
  .brand-icon {
    font-size: 20px !important;
  }
  
  .brand-name {
    font-size: 1.1rem;
  }
  
  .brand-subtitle {
    font-size: 0.6rem;
  }
  
  .back-btn {
    padding: 6px;
  }
  
  .layout-shape-1,
  .layout-shape-2,
  .layout-shape-3,
  .layout-shape-4 {
    width: 150px;
    height: 150px;
  }
}

@media (max-width: 360px) {
  .brand-subtitle {
    display: none;
  }
  
  .security-badge {
    padding: 4px 6px;
  }
}
</style>