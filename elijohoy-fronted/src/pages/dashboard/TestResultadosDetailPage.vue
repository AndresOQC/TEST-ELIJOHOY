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
          <!-- Container para las descargas -->
          <div ref="resultadosRef" class="resultados-container">
          <!-- Header con Avatar, Nombre, Dimensiones y Descripción -->
          <q-card class="q-mb-lg result-card-fullheight" flat bordered>
            <q-card-section class="bg-primary text-white">
              <div class="main-header-content">
                <!-- Avatar Grande -->
                <div class="avatar-section">
                  <img 
                    :src="avatarUrl" 
                    :alt="perfil.tipo.nombre"
                    class="avatar-image"
                    @error="onImageError"
                  />
                </div>

                <!-- Información completa abajo -->
                <div class="info-column">
                  <!-- Título sobre las métricas -->
                  <div class="title-header">
                    <div class="text-h3 text-weight-bold">
                      {{ perfil.tipo.nombre }}
                    </div>
                    <div class="text-h5 q-mt-xs">
                      {{ perfil.tipo.codigo }}
                    </div>
                  </div>
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

          <!-- Acciones de Descarga y Compartir -->
          <q-card flat bordered class="q-mt-lg">
            <q-card-section>
              <div class="text-h6 text-weight-bold q-mb-md">Compartir mis Resultados</div>
              
              <!-- Botones de Descarga -->
              <div class="q-mb-lg">
                <div class="text-subtitle2 text-weight-bold q-mb-sm text-grey-8">Descargar</div>
                <div class="row q-gutter-sm">
                  <q-btn
                    color="negative"
                    label="Descargar PDF"
                    icon="picture_as_pdf"
                    unelevated
                    @click="descargarPDF"
                    :loading="descargando.pdf"
                  />
                  <q-btn
                    color="info"
                    label="Descargar Imagen"
                    icon="image"
                    unelevated
                    @click="descargarImagen"
                    :loading="descargando.imagen"
                  />
                  <q-btn
                    color="primary"
                    label="Copiar Resultado"
                    icon="content_copy"
                    unelevated
                    @click="copiarAlPortapapeles"
                  />
                </div>
              </div>

              <!-- Botones de Redes Sociales -->
              <div class="q-mb-lg">
                <div class="text-subtitle2 text-weight-bold q-mb-sm text-grey-8">Compartir en Redes Sociales</div>
                <div class="row q-gutter-sm wrap">
                  <q-btn
                    color="green"
                    icon="wechat"
                    round
                    @click="compartirWhatsApp"
                    size="lg"
                  >
                    <q-tooltip>WhatsApp</q-tooltip>
                  </q-btn>
                  <q-btn
                    color="info"
                    icon="photo_camera"
                    round
                    @click="compartirInstagram"
                    size="lg"
                  >
                    <q-tooltip>Instagram</q-tooltip>
                  </q-btn>
                  <q-btn
                    color="facebook"
                    icon="facebook"
                    round
                    @click="compartirFacebook"
                    size="lg"
                  >
                    <q-tooltip>Facebook</q-tooltip>
                  </q-btn>
                  <q-btn
                    color="blue-10"
                    icon="mail"
                    round
                    @click="compartirMessenger"
                    size="lg"
                  >
                    <q-tooltip>Messenger</q-tooltip>
                  </q-btn>
                  <q-btn
                    color="blue"
                    icon="tag"
                    round
                    @click="compartirTwitter"
                    size="lg"
                  >
                    <q-tooltip>X (Twitter)</q-tooltip>
                  </q-btn>
                  <q-btn
                    color="linkedin"
                    icon="business"
                    round
                    @click="compartirLinkedIn"
                    size="lg"
                  >
                    <q-tooltip>LinkedIn</q-tooltip>
                  </q-btn>
                  <q-btn
                    color="purple"
                    icon="email"
                    round
                    @click="compartirEmail"
                    size="lg"
                  >
                    <q-tooltip>Correo</q-tooltip>
                  </q-btn>
                </div>
              </div>

              <!-- Botones de Acciones -->
              <div>
                <div class="text-subtitle2 text-weight-bold q-mb-sm text-grey-8">Acciones</div>
                <div class="row q-gutter-sm">
                  <q-btn
                    label="Hacer Test Nuevamente"
                    color="primary"
                    @click="reiniciarTest"
                    unelevated
                  />
                  <q-btn
                    label="Ver Mis Tests"
                    color="secondary"
                    @click="$router.push('/dashboard/test-resultados')"
                    outline
                  />
                </div>
              </div>
            </q-card-section>
          </q-card>
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
import shareService from 'src/services/share'

const route = useRoute()
const router = useRouter()
const testStore = useTestStore()
const $q = useQuasar()

const loading = ref(false)
const perfil = ref(null)
const mostrarDescripcionCompleta = ref(false)
const descargando = ref({
  pdf: false,
  imagen: false
})
const resultadosRef = ref(null)

// Mapeo de códigos MBTI a nombres de archivo de avatar
// Los archivos tienen formato: "CODIGO NombreSimple_GX.png"
const avatarMapping = {
  'INTJ': { nombre: 'Arquitecto', grupo: 'G1' },
  'INTP': { nombre: 'Lógico', grupo: 'G1' },
  'ENTJ': { nombre: 'Lógico', grupo: 'G1' },
  'ENTP': { nombre: 'Comandante', grupo: 'G1' },
  'INFJ': { nombre: 'Defensor', grupo: 'G2' },
  'INFP': { nombre: 'Mediador', grupo: 'G2' },
  'ENFJ': { nombre: 'Protaiganta', grupo: 'G2' },
  'ENFP': { nombre: 'Activista', grupo: 'G2' },
  'ISTJ': { nombre: 'Logístico', grupo: 'G3' },
  'ISFJ': { nombre: 'Protector', grupo: 'G3' },
  'ESTJ': { nombre: 'Executive', grupo: 'G3' },
  'ESFJ': { nombre: 'Cónsul', grupo: 'G3' },
  'ISTP': { nombre: 'Virtueso', grupo: 'G4' },
  'ISFP': { nombre: 'Adventurer', grupo: 'G4' },
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

// ==================== Funciones de Descarga y Compartir ====================

async function descargarPDF() {
  if (!perfil.value) return

  descargando.value.pdf = true
  try {
    const resultado = await shareService.descargarPDF(perfil.value, avatarUrl.value)
    
    if (resultado.success) {
      $q.notify({
        type: 'positive',
        message: 'PDF descargado exitosamente',
        icon: 'check_circle'
      })
    } else {
      throw new Error(resultado.message)
    }
  } catch (error) {
    console.error('Error descargando PDF:', error)
    $q.notify({
      type: 'negative',
      message: 'Error al descargar PDF',
      icon: 'error'
    })
  } finally {
    descargando.value.pdf = false
  }
}

async function descargarImagen() {
  if (!perfil.value) return

  descargando.value.imagen = true
  try {
    const resultado = await shareService.descargarImagen(perfil.value, avatarUrl.value)
    
    if (resultado.success) {
      $q.notify({
        type: 'positive',
        message: 'Imagen descargada exitosamente',
        icon: 'check_circle'
      })
    } else {
      throw new Error(resultado.message)
    }
  } catch (error) {
    console.error('Error descargando imagen:', error)
    $q.notify({
      type: 'negative',
      message: 'Error al descargar imagen',
      icon: 'error'
    })
  } finally {
    descargando.value.imagen = false
  }
}

async function copiarAlPortapapeles() {
  if (!perfil.value) return

  try {
    const resultado = await shareService.copiarAlPortapapeles(perfil.value)
    
    if (resultado.success) {
      $q.notify({
        type: 'positive',
        message: resultado.message,
        icon: 'check_circle'
      })
    } else {
      throw new Error(resultado.message)
    }
  } catch (error) {
    console.error('Error copiando al portapapeles:', error)
    $q.notify({
      type: 'negative',
      message: 'Error al copiar al portapapeles',
      icon: 'error'
    })
  }
}

async function compartirWhatsApp() {
  if (!perfil.value) return
  try {
    await shareService.compartirWhatsApp(perfil.value)
  } catch (error) {
    console.error('Error compartiendo en WhatsApp:', error)
  }
}

async function compartirInstagram() {
  if (!perfil.value) return
  try {
    await shareService.compartirInstagram(perfil.value)
  } catch (error) {
    console.error('Error compartiendo en Instagram:', error)
  }
}

async function compartirFacebook() {
  if (!perfil.value) return
  try {
    await shareService.compartirFacebook(perfil.value)
  } catch (error) {
    console.error('Error compartiendo en Facebook:', error)
  }
}

async function compartirMessenger() {
  if (!perfil.value) return
  try {
    await shareService.compartirMessenger(perfil.value)
  } catch (error) {
    console.error('Error compartiendo en Messenger:', error)
  }
}

async function compartirTwitter() {
  if (!perfil.value) return
  try {
    await shareService.compartirTwitter(perfil.value)
  } catch (error) {
    console.error('Error compartiendo en Twitter:', error)
  }
}

async function compartirLinkedIn() {
  if (!perfil.value) return
  try {
    await shareService.compartirLinkedIn(perfil.value)
  } catch (error) {
    console.error('Error compartiendo en LinkedIn:', error)
  }
}

async function compartirEmail() {
  if (!perfil.value) return
  try {
    await shareService.compartirEmail(perfil.value)
  } catch (error) {
    console.error('Error compartiendo por email:', error)
  }
}
</script>

<style scoped>
.q-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  overflow-y: auto;
  padding: 1rem;
}

/* Asegurar que el padding no cause overflow */
.row {
  margin: 0;
  width: 100%;
}

/* Card principal - altura automática */
.result-card-fullheight {
  min-height: auto;
  display: flex;
  flex-direction: column;
}

.result-card-fullheight .q-card__section {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* Layout principal del header - Flexbox responsivo */
.main-header-content {
  display: flex;
  gap: 1.5rem;
  align-items: flex-start;
  flex-wrap: wrap;
}

/* Sección del Avatar (izquierda) */
.avatar-section {
  flex: 1 1 300px;
  min-width: 250px;
  max-width: 500px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

/* Avatar responsivo */
.avatar-image {
  width: 100%;
  max-width: 400px;
  height: auto;
  object-fit: contain;
  display: block;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  animation: float 3s ease-in-out infinite;
  filter: drop-shadow(0 10px 30px rgba(0, 0, 0, 0.3));
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

.title-info .text-h3 {
  font-size: 2.5rem;
}

.title-info .text-h5 {
  font-size: 1.5rem;
}

.description-short {
  opacity: 0.95;
  line-height: 1.4;
  font-size: 1.05rem;
}

/* Columna de Información (derecha) - Ancho flexible */
.info-column {
  flex: 1 1 350px;
  min-width: 280px;
  max-width: 450px;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

/* Título del perfil */
.title-header {
  text-align: center;
  padding-bottom: 16px;
  border-bottom: 2px solid rgba(255, 255, 255, 0.3);
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

/* Responsive: Tablet y menor */
@media (max-width: 1024px) {
  .main-header-content {
    flex-direction: column;
    align-items: center;
  }

  .avatar-section {
    max-width: 100%;
    width: 100%;
  }

  .avatar-image {
    max-width: 350px;
  }

  .info-column {
    max-width: 100%;
    width: 100%;
  }
}

/* Responsive: Mobile */
@media (max-width: 768px) {
  .q-page {
    padding: 0.75rem;
  }

  .main-header-content {
    gap: 1rem;
  }

  .avatar-image {
    max-width: 300px;
  }

  .info-column {
    gap: 1rem;
    min-width: 100%;
  }

  .text-h3 {
    font-size: 1.5rem;
  }

  .text-h5 {
    font-size: 1rem;
  }

  .text-h6 {
    font-size: 0.9rem;
  }

  .dimension-label {
    font-size: 0.85rem;
  }

  .dimension-score {
    font-size: 0.8rem;
  }

  .description-wrapper {
    padding: 0.75rem;
  }

  :deep(.q-card-section) {
    padding: 1rem !important;
  }
}

/* Responsive: Small Mobile */
@media (max-width: 480px) {
  .q-page {
    padding: 0.5rem;
  }

  .main-header-content {
    gap: 0.75rem;
  }

  .avatar-section {
    padding: 0.5rem;
  }

  .avatar-image {
    max-width: 250px;
  }

  .text-h3 {
    font-size: 1.3rem;
  }

  .text-h5 {
    font-size: 0.95rem;
  }

  .text-h6 {
    font-size: 0.85rem;
  }

  .dimension-label {
    font-size: 0.8rem;
  }

  .dimension-score {
    font-size: 0.75rem;
    margin-left: 0.5rem;
  }

  .description-wrapper {
    padding: 0.6rem;
  }

  .description-text {
    font-size: 0.85rem;
  }

  :deep(.q-card-section) {
    padding: 0.75rem !important;
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

/* Estilos para botones de compartir y descargar */
.resultados-container {
  animation: fadeInDown 0.5s ease-out;
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Estilos para los botones de redes sociales */
:deep(.q-btn--round) {
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

:deep(.q-btn--round:hover) {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

/* Color para Facebook */
:deep(.q-btn.bg-facebook) {
  background-color: #1877F2 !important;
}

/* Color para LinkedIn */
:deep(.q-btn.bg-linkedin) {
  background-color: #0A66C2 !important;
}

/* Mejorar aspecto de los botones de descarga y redes sociales */
:deep(.q-btn) {
  font-weight: 600;
  transition: all 0.3s ease;
}

:deep(.q-btn:not(.q-btn--round)) {
  border-radius: 8px;
  padding: 12px 24px;
}

:deep(.q-btn--outline) {
  border-width: 2px;
}

/* Card de acciones con mejor presentación */
:deep(.q-card) {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-radius: 12px;
}

/* Tooltip estilo */
:deep(.q-tooltip) {
  background-color: rgba(0, 0, 0, 0.9);
  border-radius: 6px;
  font-weight: 500;
}

/* Responsive para botones de redes */
@media (max-width: 768px) {
  :deep(.q-btn--round) {
    size: md;
  }
}

@media (max-width: 480px) {
  :deep(.q-btn:not(.q-btn--round)) {
    padding: 10px 16px;
    font-size: 0.9rem;
  }
  
  :deep(.q-btn--round) {
    size: sm;
  }
}
</style>

