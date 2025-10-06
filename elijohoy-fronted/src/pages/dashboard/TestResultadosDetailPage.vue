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
          <!-- Header -->
          <q-card class="q-mb-lg" flat bordered>
            <q-card-section class="text-center bg-primary text-white">
              <div class="text-h3 text-weight-bold q-mb-sm">
                {{ perfil.tipo.nombre }}
              </div>
              <div class="text-h5">
                {{ perfil.tipo.codigo }}
              </div>
              <div class="text-subtitle1 q-mt-md">
                {{ perfil.tipo.descripcion_corta }}
              </div>
            </q-card-section>
          </q-card>

          <!-- Puntuaciones -->
          <q-card class="q-mb-lg" flat bordered>
            <q-card-section>
              <div class="text-h6 text-weight-bold q-mb-md">Tus Dimensiones</div>

              <div class="q-gutter-md">
                <!-- IE -->
                <div>
                  <div class="row items-center q-mb-sm">
                    <div class="col-6 text-weight-bold">
                      {{ perfil.dimensiones.extraversion_introversion }}
                    </div>
                    <div class="col-6 text-right text-grey-7">
                      Puntuación: {{ perfil.puntuaciones.IE }}
                    </div>
                  </div>
                  <q-linear-progress
                    :value="(perfil.puntuaciones.IE - 8) / 30"
                    color="purple"
                    size="12px"
                  />
                </div>

                <!-- SN -->
                <div>
                  <div class="row items-center q-mb-sm">
                    <div class="col-6 text-weight-bold">
                      {{ perfil.dimensiones.intuicion_sensacion }}
                    </div>
                    <div class="col-6 text-right text-grey-7">
                      Puntuación: {{ perfil.puntuaciones.SN }}
                    </div>
                  </div>
                  <q-linear-progress
                    :value="(perfil.puntuaciones.SN - 4) / 40"
                    color="blue"
                    size="12px"
                  />
                </div>

                <!-- FT -->
                <div>
                  <div class="row items-center q-mb-sm">
                    <div class="col-6 text-weight-bold">
                      {{ perfil.dimensiones.pensamiento_sentimiento }}
                    </div>
                    <div class="col-6 text-right text-grey-7">
                      Puntuación: {{ perfil.puntuaciones.FT }}
                    </div>
                  </div>
                  <q-linear-progress
                    :value="(perfil.puntuaciones.FT - 8) / 30"
                    color="green"
                    size="12px"
                  />
                </div>

                <!-- JP -->
                <div>
                  <div class="row items-center q-mb-sm">
                    <div class="col-6 text-weight-bold">
                      {{ perfil.dimensiones.percepcion_juicio }}
                    </div>
                    <div class="col-6 text-right text-grey-7">
                      Puntuación: {{ perfil.puntuaciones.JP }}
                    </div>
                  </div>
                  <q-linear-progress
                    :value="(perfil.puntuaciones.JP - 10) / 30"
                    color="orange"
                    size="12px"
                  />
                </div>
              </div>
            </q-card-section>
          </q-card>

          <!-- Descripción -->
          <q-card class="q-mb-lg" flat bordered>
            <q-card-section>
              <div class="text-h6 text-weight-bold q-mb-md">Descripción</div>
              <p class="text-body1">{{ perfil.tipo.descripcion_completa }}</p>
            </q-card-section>
          </q-card>

          <!-- Fortalezas y Debilidades -->
          <div class="row q-col-gutter-md q-mb-lg">
            <div class="col-12 col-md-6">
              <q-card flat bordered>
                <q-card-section>
                  <div class="text-h6 text-weight-bold text-positive q-mb-md">
                    <q-icon name="star" /> Fortalezas
                  </div>
                  <p class="text-body1">{{ perfil.tipo.fortalezas }}</p>
                </q-card-section>
              </q-card>
            </div>
            <div class="col-12 col-md-6">
              <q-card flat bordered>
                <q-card-section>
                  <div class="text-h6 text-weight-bold text-warning q-mb-md">
                    <q-icon name="warning" /> Áreas de Mejora
                  </div>
                  <p class="text-body1">{{ perfil.tipo.debilidades }}</p>
                </q-card-section>
              </q-card>
            </div>
          </div>

          <!-- Carreras Sugeridas -->
          <q-card class="q-mb-lg" flat bordered>
            <q-card-section>
              <div class="text-h6 text-weight-bold q-mb-md">
                <q-icon name="work" /> Carreras Sugeridas
              </div>
              <p class="text-body1">{{ perfil.tipo.carreras_sugeridas }}</p>
            </q-card-section>
          </q-card>

          <!-- Famosos del mismo tipo -->
          <q-card class="q-mb-lg" flat bordered>
            <q-card-section>
              <div class="text-h6 text-weight-bold q-mb-md">
                <q-icon name="people" /> Personas Famosas con este Tipo
              </div>
              <p class="text-body1">{{ perfil.tipo.famosos_tipo }}</p>
            </q-card-section>
          </q-card>

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
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTestStore } from 'src/stores/test'
import { useQuasar } from 'quasar'

const route = useRoute()
const router = useRouter()
const testStore = useTestStore()
const $q = useQuasar()

const loading = ref(false)
const perfil = ref(null)

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
