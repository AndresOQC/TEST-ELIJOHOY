<template>
  <div class="error-page">
    <!-- Formas decorativas -->
    <div class="shape-decoration shape-1"></div>
    <div class="shape-decoration shape-2"></div>
    <div class="shape-decoration shape-3"></div>

    <div class="error-content">
      <div class="error-icon-wrapper q-mb-lg">
        <q-icon name="search_off" size="120px" color="white" />
      </div>

      <div class="error-number">404</div>

      <div class="text-h3 text-weight-bold text-white q-mb-md">
        ¡Página No Encontrada!
      </div>

      <div class="text-h6 text-white-7 q-mb-xl" style="max-width: 500px; margin: 0 auto;">
        Lo sentimos, la página que estás buscando no existe o ha sido movida.
      </div>

      <div class="row q-gutter-md justify-center">
        <q-btn
          unelevated
          size="lg"
          color="yellow-9"
          text-color="purple-10"
          label="Ir al Inicio"
          icon="home"
          to="/"
          class="btn-gradient"
          no-caps
        />

        <q-btn
          outline
          size="lg"
          color="white"
          label="Volver Atrás"
          icon="arrow_back"
          @click="$router.back()"
          class="btn-outline"
          no-caps
        />
      </div>
    </div>
  </div>
</template>

<script setup>
//
</script>

<style scoped>
.error-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 50%, #4C1D95 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  position: relative;
  overflow: hidden;
  text-align: center;
}

.error-content {
  position: relative;
  z-index: 2;
  max-width: 700px;
}

/* Formas decorativas */
.shape-decoration {
  position: fixed;
  border-radius: 50%;
  opacity: 0.12;
  z-index: 1;
}

.shape-1 {
  width: 400px;
  height: 400px;
  background: #FDB813;
  top: -100px;
  right: -100px;
}

.shape-2 {
  width: 300px;
  height: 300px;
  background: #EC4899;
  bottom: -80px;
  left: -80px;
}

.shape-3 {
  width: 250px;
  height: 250px;
  background: #10B981;
  top: 50%;
  right: -60px;
}

.error-icon-wrapper {
  width: 180px;
  height: 180px;
  margin: 0 auto;
  background: rgba(253, 184, 19, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 4px solid rgba(253, 184, 19, 0.4);
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

.error-number {
  font-size: 120px;
  font-weight: 900;
  color: white;
  line-height: 1;
  margin-bottom: 20px;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  letter-spacing: -5px;
}

.text-white-7 {
  color: rgba(255, 255, 255, 0.85);
}

.btn-gradient {
  background: linear-gradient(135deg, #FDB813 0%, #F59E0B 100%);
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  padding: 14px 32px;
  box-shadow: 0 4px 20px rgba(253, 184, 19, 0.4);
  transition: all 0.3s ease;
}

.btn-gradient:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 28px rgba(253, 184, 19, 0.6);
}

.btn-outline {
  border: 2px solid white;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  padding: 12px 32px;
  transition: all 0.3s ease;
}

.btn-outline:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

@media (max-width: 600px) {
  .error-number {
    font-size: 80px;
  }

  .error-icon-wrapper {
    width: 140px;
    height: 140px;
  }

  .error-icon-wrapper .q-icon {
    font-size: 80px !important;
  }

  .text-h3 {
    font-size: 1.75rem;
  }

  .text-h6 {
    font-size: 1rem;
  }

  .shape-1,
  .shape-2,
  .shape-3 {
    width: 200px;
    height: 200px;
  }
}
</style>
