<template>
  <q-page class="q-pa-md">
    <div class="row justify-center">
      <div class="col-12 col-md-10 col-lg-8">
        <!-- Loading -->
        <div v-if="loading" class="text-center q-py-xl">
          <q-spinner color="primary" size="50px" />
          <p class="text-body1 text-grey-7 q-mt-md">Cargando resultados...</p>
        </div>

        <!-- Resultados -->
        <div v-else-if="perfil">
          <!-- Header con Avatar, Nombre, Dimensiones y Descripción -->
          <q-card class="q-mb-lg" flat bordered>
            <q-card-section class="bg-primary text-white">
              <div class="main-header-content">
                <!-- Columna Izquierda: Avatar -->
                <div class="avatar-column">
                  <div class="avatar-container">
                    <img 
                      :src="avatarUrl" 
                      :alt="perfil.tipo.nombre"
                      class="avatar-image"
                      @error="onImageError"
                    />
                  </div>
                  
                  <div class="title-info">
                    <div class="text-h3 text-weight-bold">
                      {{ perfil.tipo.nombre }}
                    </div>
                    <div class="text-h5 q-mt-xs">
                      {{ perfil.tipo.codigo }}
                    </div>
                    <div class="text-subtitle1 q-mt-sm description-short">
                      {{ perfil.tipo.descripcion_corta }}
                    </div>
                  </div>
                </div>

                <!-- Columna Derecha: Dimensiones y Descripción -->
                <div class="info-column">
                  <!-- Dimensiones -->
                  <div class="dimensions-wrapper">
                    <div class="text-h6 text-weight-bold q-mb-md">Tus Dimensiones</div>

                    <div class="q-gutter-sm">
                      <!-- IE -->
                      <div>
                        <div class="row items-center q-mb-xs no-wrap">
                          <div class="col text-weight-medium dimension-label">
                            {{ perfil.dimensiones.extraversion_introversion }}
                          </div>
                          <div class="dimension-score">
                            Puntuación: {{ perfil.puntuaciones.IE }}
                          </div>
                        </div>
                        <q-linear-progress
                          :value="(perfil.puntuaciones.IE - 8) / 30"
                          color="purple-4"
                          size="10px"
                          class="rounded-progress"
                        />
                      </div>

                      <!-- SN -->
                      <div>
                        <div class="row items-center q-mb-xs no-wrap">
                          <div class="col text-weight-medium dimension-label">
                            {{ perfil.dimensiones.intuicion_sensacion }}
                          </div>
                          <div class="dimension-score">
                            Puntuación: {{ perfil.puntuaciones.SN }}
                          </div>
                        </div>
                        <q-linear-progress
                          :value="(perfil.puntuaciones.SN - 4) / 40"
                          color="blue-4"
                          size="10px"
                          class="rounded-progress"
                        />
                      </div>

                      <!-- FT -->
                      <div>
                        <div class="row items-center q-mb-xs no-wrap">
                          <div class="col text-weight-medium dimension-label">
                            {{ perfil.dimensiones.pensamiento_sentimiento }}
                          </div>
                          <div class="dimension-score">
                            Puntuación: {{ perfil.puntuaciones.FT }}
                          </div>
                        </div>
                        <q-linear-progress
                          :value="(perfil.puntuaciones.FT - 8) / 30"
                          color="green-4"
                          size="10px"
                          class="rounded-progress"
                        />
                      </div>

                      <!-- JP -->
                      <div>
                        <div class="row items-center q-mb-xs no-wrap">
                          <div class="col text-weight-medium dimension-label">
                            {{ perfil.dimensiones.percepcion_juicio }}
                          </div>
                          <div class="dimension-score">
                            Puntuación: {{ perfil.puntuaciones.JP }}
                          </div>
                        </div>
                        <q-linear-progress
                          :value="(perfil.puntuaciones.JP - 10) / 30"
                          color="orange-4"
                          size="10px"
                          class="rounded-progress"
                        />
                      </div>
                    </div>
                  </div>

                  <!-- Descripción corta -->
                  <div class="description-wrapper q-mt-md">
                    <div class="text-h6 text-weight-bold q-mb-sm">Descripción</div>
                    <p class="text-body2 description-text">
                      {{ perfil.tipo.descripcion_completa }}
                    </p>
                  </div>
                </div>
              </div>
            </q-card-section>
          </q-card>

          <!-- Botón Descripción Completa -->
          <div class="text-center q-mb-lg">
            <q-btn
              label="Ver Descripción Completa"
              icon="article"
              color="primary"
              size="md"
              unelevated
              @click="mostrarDescripcionCompleta = true"
            />
          </div>

          <!-- Dialog Descripción Completa -->
          <q-dialog v-model="mostrarDescripcionCompleta">
            <q-card style="min-width: 350px; max-width: 700px;">
              <q-card-section class="bg-primary text-white">
                <div class="text-h5 text-weight-bold">
                  {{ perfil.tipo.nombre }} - {{ perfil.tipo.codigo }}
                </div>
              </q-card-section>

              <q-card-section class="q-pt-md" style="max-height: 60vh; overflow-y: auto;">

                <div class="text-h6 text-weight-bold q-mt-md q-mb-sm text-positive">
                  <q-icon name="star" /> Fortalezas
                </div>
                <p class="text-body1">{{ perfil.tipo.fortalezas }}</p>

                <div class="text-h6 text-weight-bold q-mt-md q-mb-sm text-warning">
                  <q-icon name="warning" /> Áreas de Mejora
                </div>
                <p class="text-body1">{{ perfil.tipo.debilidades }}</p>

                <div class="text-h6 text-weight-bold q-mt-md q-mb-sm">
                  <q-icon name="work" /> Carreras Sugeridas
                </div>
                <p class="text-body1">{{ perfil.tipo.carreras_sugeridas }}</p>

                <div class="text-h6 text-weight-bold q-mt-md q-mb-sm">
                  <q-icon name="people" /> Personas Famosas
                </div>
                <p class="text-body1">{{ perfil.tipo.famosos_tipo }}</p>
              </q-card-section>

              <q-card-actions align="right">
                <q-btn flat label="Cerrar" color="primary" v-close-popup />
              </q-card-actions>
            </q-card>
          </q-dialog>

          <!-- Estadística -->
          <q-card flat bordered>
            <q-card-section class="bg-grey-2">
              <div class="text-center">
                <div class="text-subtitle1 text-grey-7">Porcentaje de la población</div>
                <div class="text-h4 text-weight-bold text-primary">
                  {{ perfil.tipo.porcentaje_poblacion }}%
                </div>
              </div>
            </q-card-section>
          </q-card>

          <!-- Acciones -->
          <div class="q-mt-lg text-center">
            <q-btn
              label="Hacer Test Nuevamente"
              color="primary"
              @click="reiniciarTest"
              class="q-mr-sm"
            />
            <q-btn
              label="Ver Mis Tests"
              color="secondary"
              @click="$router.push('/dashboard/test-resultados')"
              outline
            />
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTestStore } from 'src/stores/test'
import { useQuasar } from 'quasar'

const route = useRoute()
const router = useRouter()
const testStore = useTestStore()
const $q = useQuasar()

const loading = ref(false)
const perfil = ref(null)
const mostrarDescripcionCompleta = ref(false)

// Mapeo de códigos MBTI a nombres de archivo de avatar
// Los archivos tienen formato: "CODIGO NombreSimple_GX.png"
const avatarMapping = {
  'INTJ': { nombre: 'Arquitecto', grupo: 'G1' },
  'INTP': { nombre: 'Lógico', grupo: 'G1' },
  'ENTJ': { nombre: 'Comandante', grupo: 'G1' },
  'ENTP': { nombre: 'Debatiente', grupo: 'G1' },
  'INFJ': { nombre: 'Defensor', grupo: 'G2' },
  'INFP': { nombre: 'Mediador', grupo: 'G2' },
  'ENFJ': { nombre: 'Protagonista', grupo: 'G2' },
  'ENFP': { nombre: 'Activista', grupo: 'G2' },
  'ISTJ': { nombre: 'Logístico', grupo: 'G3' },
  'ISFJ': { nombre: 'Defensor', grupo: 'G3' },
  'ESTJ': { nombre: 'Ejecutivo', grupo: 'G3' },
  'ESFJ': { nombre: 'Cónsul', grupo: 'G3' },
  'ISTP': { nombre: 'Virtuoso', grupo: 'G4' },
  'ISFP': { nombre: 'Aventurero', grupo: 'G4' },
  'ESTP': { nombre: 'Emprendedor', grupo: 'G4' },
  'ESFP': { nombre: 'Animador', grupo: 'G4' }
}

// Computed para obtener la URL del avatar
const avatarUrl = computed(() => {
  if (!perfil.value) return ''
  
  const codigo = perfil.value.tipo.codigo
  const avatarInfo = avatarMapping[codigo]
  
  if (!avatarInfo) {
    console.warn(`No se encontró mapeo de avatar para el código: ${codigo}`)
    return ''
  }
  
  // Construir el nombre del archivo según el formato real: "CODIGO Nombre_GX.png"
  const nombreArchivo = `${codigo} ${avatarInfo.nombre}_${avatarInfo.grupo}.png`
  
  // Usar ruta relativa desde la carpeta public
  return `/AVATAR/${nombreArchivo}`
})

const onImageError = (event) => {
  console.error('Error cargando avatar:', avatarUrl.value)
  // Imagen por defecto si no se encuentra el avatar
  event.target.style.display = 'none'
}

onMounted(async () => {
  await cargarResultados()
})

async function cargarResultados() {
  try {
    loading.value = true
    const idSesion = route.params.id

    const response = await testStore.obtenerResultados(idSesion)
    if (response.success) {
      perfil.value = response.perfil
    }
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: error.message || 'Error al cargar resultados'
    })
  } finally {
    loading.value = false
  }
}

async function reiniciarTest() {
  try {
    await testStore.reiniciarTest()
    router.push('/dashboard/test')
  } catch {
    $q.notify({
      type: 'negative',
      message: 'Error al iniciar test'
    })
  }
}
</script>

<style scoped>
.q-page {
  min-height: calc(100vh - 64px);
  height: 100%;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* Asegurar que el padding no cause overflow */
.row {
  margin: 0;
  width: 100%;
}

/* Layout principal del header - Optimizado para ocupar todo el espacio */
.main-header-content {
  display: flex;
  gap: 20px;
  align-items: stretch;
  min-height: 400px;
}

/* Columna del Avatar (izquierda) - Más ancha */
.avatar-column {
  flex: 0 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 12px;
  min-width: 300px;
}

.avatar-container {
  background-color: rgba(255, 255, 255, 0.15);
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  position: relative;
}

/* Avatar MÁS GRANDE con animaciones */
.avatar-image {
  width: 280px;
  height: 280px;
  object-fit: contain;
  display: block;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  animation: float 3s ease-in-out infinite;
}

/* Animación de flotación */
@keyframes float {
  0%, 100% {
    transform: translateY(0px) scale(1);
  }
  50% {
    transform: translateY(-10px) scale(1.02);
  }
}

/* Hover con zoom y rotación */
.avatar-image:hover {
  transform: scale(1.15) rotate(5deg);
  animation-play-state: paused;
}

/* Animación de entrada */
.avatar-image {
  animation: float 3s ease-in-out infinite, fadeInZoom 0.8s ease-out;
}

@keyframes fadeInZoom {
  0% {
    opacity: 0;
    transform: scale(0.5);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

.title-info {
  width: 100%;
}

.description-short {
  opacity: 0.95;
  line-height: 1.3;
  font-size: 0.95rem;
}

/* Columna de Información (derecha) - Ocupa TODO el espacio */
.info-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-width: 0;
}

.dimensions-wrapper {
  flex: 0 0 auto;
}

.dimension-label {
  font-size: 0.95rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.dimension-score {
  flex-shrink: 0;
  font-size: 0.9rem;
  opacity: 0.9;
  white-space: nowrap;
  margin-left: 12px;
}

/* Descripción ocupa TODO el espacio restante */
.description-wrapper {
  flex: 1 1 auto;
  background-color: rgba(255, 255, 255, 0.12);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  min-height: 0;
  box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.1);
}

.description-wrapper .text-h6 {
  margin-bottom: 12px;
  flex-shrink: 0;
}

.description-text {
  line-height: 1.5;
  margin: 0;
  opacity: 0.95;
  overflow-y: auto;
  flex: 1;
}

.rounded-progress {
  border-radius: 5px;
  overflow: hidden;
}

/* Reducir padding del card */
:deep(.q-card-section) {
  padding: 20px !important;
}

/* Responsive: Tablet */
@media (max-width: 1024px) {
  .main-header-content {
    flex-direction: column;
    align-items: stretch;
    min-height: auto;
  }
  
  .avatar-column {
    width: 100%;
    min-width: auto;
  }
  
  .info-column {
    width: 100%;
  }
  
  .avatar-image {
    width: 240px;
    height: 240px;
  }
}

/* Responsive: Mobile */
@media (max-width: 768px) {
  .q-page {
    padding: 12px !important;
  }
  
  .main-header-content {
    gap: 16px;
  }
  
  .avatar-column {
    gap: 10px;
  }
  
  .avatar-container {
    padding: 16px;
  }
  
  .avatar-image {
    width: 200px;
    height: 200px;
  }
  
  .text-h3 {
    font-size: 1.6rem;
  }
  
  .text-h5 {
    font-size: 1.1rem;
  }
  
  .text-h6 {
    font-size: 0.95rem;
  }
  
  .dimension-label {
    font-size: 0.88rem;
  }
  
  .dimension-score {
    font-size: 0.82rem;
  }
  
  .description-wrapper {
    padding: 12px;
  }
  
  :deep(.q-card-section) {
    padding: 16px !important;
  }
}

/* Responsive: Small Mobile */
@media (max-width: 480px) {
  .q-page {
    padding: 10px !important;
  }
  
  .main-header-content {
    gap: 12px;
  }
  
  .avatar-column {
    min-width: auto;
  }
  
  .avatar-container {
    padding: 12px;
  }
  
  .avatar-image {
    width: 160px;
    height: 160px;
  }
  
  .text-h3 {
    font-size: 1.4rem;
  }
  
  .text-h5 {
    font-size: 1rem;
  }
  
  .text-h6 {
    font-size: 0.9rem;
  }
  
  .text-subtitle1 {
    font-size: 0.82rem;
  }
  
  .dimension-label {
    font-size: 0.85rem;
  }
  
  .dimension-score {
    font-size: 0.78rem;
    margin-left: 8px;
  }
  
  .description-wrapper {
    padding: 10px;
  }
  
  .description-text {
    font-size: 0.88rem;
  }
  
  :deep(.q-card-section) {
    padding: 12px !important;
  }
}

/* Low Height Screens */
@media (max-height: 700px) {
  .avatar-image {
    width: 180px;
    height: 180px;
  }
  
  .main-header-content {
    min-height: 300px;
  }
}

/* Animaciones adicionales para elementos */
.dimensions-wrapper > div {
  animation: slideInRight 0.6s ease-out backwards;
}

.dimensions-wrapper > div:nth-child(2) {
  animation-delay: 0.1s;
}

.dimensions-wrapper > div:nth-child(3) {
  animation-delay: 0.2s;
}

.dimensions-wrapper > div:nth-child(4) {
  animation-delay: 0.3s;
}

.dimensions-wrapper > div:nth-child(5) {
  animation-delay: 0.4s;
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.description-wrapper {
  animation: fadeIn 0.8s ease-out 0.5s backwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>

