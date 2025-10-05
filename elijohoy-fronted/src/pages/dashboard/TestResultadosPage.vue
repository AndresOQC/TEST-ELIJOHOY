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
                Test Vocacional
              </h1>
              <p class="text-body1 text-grey-7">
                Descubre tu vocación profesional
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Coming Soon Card -->
      <div class="col-12">
        <q-card class="coming-soon-card" flat>
          <q-card-section class="text-center q-pa-xl">
            <div class="coming-soon-icon-wrapper q-mb-lg">
              <q-icon name="construction" size="80px" color="white" />
            </div>

            <div class="text-h3 text-weight-bold text-white q-mb-md">
              ¡Próximamente!
            </div>

            <div class="text-h6 text-white-7 q-mb-xl" style="max-width: 600px; margin: 0 auto;">
              Estamos trabajando en traerte la mejor experiencia de test vocacional.
              Pronto podrás descubrir tu futuro profesional aquí.
            </div>

            <div class="features-grid q-mb-xl">
              <div class="feature-item">
                <q-icon name="psychology" size="48px" color="yellow-9" class="q-mb-sm" />
                <div class="text-subtitle1 text-white text-weight-bold">Test Personalizado</div>
                <div class="text-body2 text-white-7">Análisis detallado de tus intereses</div>
              </div>

              <div class="feature-item">
                <q-icon name="school" size="48px" color="yellow-9" class="q-mb-sm" />
                <div class="text-subtitle1 text-white text-weight-bold">Carreras Sugeridas</div>
                <div class="text-body2 text-white-7">Recomendaciones personalizadas</div>
              </div>

              <div class="feature-item">
                <q-icon name="insights" size="48px" color="yellow-9" class="q-mb-sm" />
                <div class="text-subtitle1 text-white text-weight-bold">Resultados Detallados</div>
                <div class="text-body2 text-white-7">Informes completos de tu perfil</div>
              </div>
            </div>

            <q-btn
              unelevated
              size="lg"
              color="yellow-9"
              text-color="purple-10"
              label="Volver al Dashboard"
              icon="dashboard"
              @click="$router.push('/dashboard')"
              class="btn-gradient"
              no-caps
            />
          </q-card-section>
        </q-card>
      </div>

      <!-- Info Cards -->
      <div class="col-12 col-md-4">
        <q-card class="info-card" flat bordered>
          <q-card-section class="text-center">
            <q-icon name="timer" size="48px" color="purple-7" class="q-mb-md" />
            <div class="text-h6 text-weight-bold text-purple-10 q-mb-sm">
              15-20 minutos
            </div>
            <div class="text-body2 text-grey-7">
              Tiempo estimado del test
            </div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-md-4">
        <q-card class="info-card" flat bordered>
          <q-card-section class="text-center">
            <q-icon name="checklist" size="48px" color="purple-7" class="q-mb-md" />
            <div class="text-h6 text-weight-bold text-purple-10 q-mb-sm">
              50+ preguntas
            </div>
            <div class="text-body2 text-grey-7">
              Test completo y detallado
            </div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-12 col-md-4">
        <q-card class="info-card" flat bordered>
          <q-card-section class="text-center">
            <q-icon name="trending_up" size="48px" color="purple-7" class="q-mb-md" />
            <div class="text-h6 text-weight-bold text-purple-10 q-mb-sm">
              Resultados inmediatos
            </div>
            <div class="text-body2 text-grey-7">
              Obtén tu perfil vocacional al instante
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'TestResultadosPage'
})
</script>

<style scoped>
.test-resultados-page {
  max-width: 1200px;
  margin: 0 auto;
  background: linear-gradient(to bottom, #F3F4F6, #FFFFFF);
  min-height: calc(100vh - 64px);
}

.page-header {
  padding: 20px 0;
}

.coming-soon-card {
  border-radius: 24px;
  background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%);
  box-shadow: 0 12px 40px rgba(124, 58, 237, 0.3);
}

.coming-soon-icon-wrapper {
  width: 160px;
  height: 160px;
  margin: 0 auto;
  background: rgba(253, 184, 19, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 4px solid rgba(253, 184, 19, 0.4);
  animation: rotate 4s linear infinite;
}

@keyframes rotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.text-white-7 {
  color: rgba(255, 255, 255, 0.85);
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 32px;
  padding: 0 32px;
}

.feature-item {
  padding: 24px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.feature-item:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-4px);
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

.info-card {
  border-radius: 20px;
  border: 2px solid #E5E7EB;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  background: white;
}

.info-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 32px rgba(124, 58, 237, 0.15);
  border-color: #7C3AED;
}

@media (max-width: 768px) {
  .test-resultados-page {
    padding: 12px;
  }

  .coming-soon-card {
    border-radius: 16px;
  }

  .coming-soon-icon-wrapper {
    width: 120px;
    height: 120px;
  }

  .coming-soon-icon-wrapper .q-icon {
    font-size: 60px !important;
  }

  .features-grid {
    grid-template-columns: 1fr;
    gap: 16px;
    padding: 0;
  }

  .text-h3 {
    font-size: 1.75rem;
  }
}
</style>