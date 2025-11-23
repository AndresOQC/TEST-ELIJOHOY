<template>
  <q-page class="q-pa-md">
    <div class="row q-mb-md">
      <div class="col">
        <div class="text-h4 text-weight-bold">Administrar Preguntas del Test</div>
        <div class="text-subtitle2 text-grey-7">
          Gestiona las 32 preguntas del test OEJTS
        </div>
      </div>
      <div class="col-auto">
        <q-btn
          color="primary"
          icon="add"
          label="Nueva Pregunta"
          @click="mostrarDialogCrear = true"
          unelevated
          no-caps
        />
      </div>
    </div>

    <!-- Tabla de preguntas -->
    <q-card>
      <q-card-section>
        <q-table
          :rows="preguntas"
          :columns="columns"
          row-key="id_pregunta"
          :loading="loading"
          :pagination="pagination"
          binary-state-sort
          flat
          bordered
        >
          <!-- Slot para editar texto izquierda -->
          <template v-slot:body-cell-texto_izquierda="props">
            <q-td :props="props">
              <div v-if="editando !== props.row.id_pregunta" class="text-left">
                {{ props.row.texto_izquierda }}
              </div>
              <q-input
                v-else
                v-model="preguntaEdit.texto_izquierda"
                dense
                outlined
                autofocus
                type="textarea"
                rows="2"
              />
            </q-td>
          </template>

          <!-- Slot para editar texto derecha -->
          <template v-slot:body-cell-texto_derecha="props">
            <q-td :props="props">
              <div v-if="editando !== props.row.id_pregunta" class="text-left">
                {{ props.row.texto_derecha }}
              </div>
              <q-input
                v-else
                v-model="preguntaEdit.texto_derecha"
                dense
                outlined
                type="textarea"
                rows="2"
              />
            </q-td>
          </template>

          <!-- Slot para dimensión -->
          <template v-slot:body-cell-dimension="props">
            <q-td :props="props">
              <q-badge
                :color="getDimensionColor(props.row.dimension)"
                :label="props.row.dimension"
              />
            </q-td>
          </template>

          <!-- Slot para peso -->
          <template v-slot:body-cell-peso="props">
            <q-td :props="props">
              <q-chip
                :color="props.row.peso > 0 ? 'positive' : 'negative'"
                text-color="white"
                dense
              >
                {{ props.row.peso > 0 ? '+' : '' }}{{ props.row.peso }}
              </q-chip>
            </q-td>
          </template>

          <!-- Slot para activa -->
          <template v-slot:body-cell-activa="props">
            <q-td :props="props">
              <q-toggle
                :model-value="props.row.activa"
                @update:model-value="toggleActiva(props.row)"
                color="positive"
                :disable="loading"
              />
            </q-td>
          </template>

          <!-- Slot para acciones -->
          <template v-slot:body-cell-acciones="props">
            <q-td :props="props">
              <div class="q-gutter-sm">
                <q-btn
                  v-if="editando !== props.row.id_pregunta"
                  icon="edit"
                  color="primary"
                  flat
                  dense
                  round
                  @click="iniciarEdicion(props.row)"
                >
                  <q-tooltip>Editar</q-tooltip>
                </q-btn>
                <template v-else>
                  <q-btn
                    icon="check"
                    color="positive"
                    flat
                    dense
                    round
                    @click="guardarEdicion()"
                  >
                    <q-tooltip>Guardar</q-tooltip>
                  </q-btn>
                  <q-btn
                    icon="close"
                    color="negative"
                    flat
                    dense
                    round
                    @click="cancelarEdicion()"
                  >
                    <q-tooltip>Cancelar</q-tooltip>
                  </q-btn>
                </template>
                <q-btn
                  icon="delete"
                  color="negative"
                  flat
                  dense
                  round
                  @click="confirmarEliminar(props.row)"
                >
                  <q-tooltip>Eliminar</q-tooltip>
                </q-btn>
              </div>
            </q-td>
          </template>
        </q-table>
      </q-card-section>
    </q-card>

    <!-- Diálogo para crear nueva pregunta -->
    <q-dialog v-model="mostrarDialogCrear" persistent>
      <q-card style="min-width: 600px">
        <q-card-section class="row items-center">
          <div class="text-h6">Crear Nueva Pregunta</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-card-section>
          <q-form @submit="crearPregunta" class="q-gutter-md">
            <q-input
              v-model="nuevaPregunta.texto_izquierda"
              label="Texto Izquierda *"
              type="textarea"
              rows="3"
              outlined
              required
            />

            <q-input
              v-model="nuevaPregunta.texto_derecha"
              label="Texto Derecha *"
              type="textarea"
              rows="3"
              outlined
              required
            />

            <div class="row q-gutter-sm">
              <div class="col-4">
                <q-select
                  v-model="nuevaPregunta.dimension"
                  :options="dimensiones"
                  label="Dimensión *"
                  outlined
                  required
                />
              </div>
              <div class="col-4">
                <q-select
                  v-model="nuevaPregunta.peso"
                  :options="pesos"
                  label="Peso *"
                  outlined
                  required
                />
              </div>
              <div class="col-4">
                <q-input
                  v-model.number="nuevaPregunta.orden"
                  label="Orden *"
                  type="number"
                  outlined
                  required
                />
              </div>
            </div>

            <q-toggle
              v-model="nuevaPregunta.activa"
              label="Activa"
              color="positive"
            />
          </q-form>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancelar" v-close-popup />
          <q-btn
            color="primary"
            label="Crear Pregunta"
            @click="crearPregunta"
            :loading="loading"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { api } from 'src/services/api'
import testService from 'src/services/test'

const $q = useQuasar()

const loading = ref(false)
const preguntas = ref([])
const editando = ref(null)
const preguntaEdit = ref({})
const mostrarDialogCrear = ref(false)
const nuevaPregunta = ref({
  texto_izquierda: '',
  texto_derecha: '',
  dimension: null,
  peso: null,
  orden: null,
  activa: true
})

const pagination = ref({
  rowsPerPage: 10
})

const dimensiones = ['IE', 'SN', 'FT', 'JP']
const pesos = [-1, 1]

const columns = [
  {
    name: 'orden',
    label: '#',
    field: 'orden',
    align: 'center',
    sortable: true,
    style: 'width: 60px'
  },
  {
    name: 'texto_izquierda',
    label: 'Texto Izquierda',
    field: 'texto_izquierda',
    align: 'left',
    sortable: false,
    style: 'min-width: 250px'
  },
  {
    name: 'texto_derecha',
    label: 'Texto Derecha',
    field: 'texto_derecha',
    align: 'left',
    sortable: false,
    style: 'min-width: 250px'
  },
  {
    name: 'dimension',
    label: 'Dimensión',
    field: 'dimension',
    align: 'center',
    sortable: true,
    style: 'width: 100px'
  },
  {
    name: 'peso',
    label: 'Peso',
    field: 'peso',
    align: 'center',
    sortable: true,
    style: 'width: 80px'
  },
  {
    name: 'activa',
    label: 'Activa',
    field: 'activa',
    align: 'center',
    sortable: true,
    style: 'width: 100px'
  },
  {
    name: 'acciones',
    label: 'Acciones',
    field: 'acciones',
    align: 'center',
    style: 'width: 120px'
  }
]

function getDimensionColor(dimension) {
  const colors = {
    'IE': 'purple',
    'SN': 'blue',
    'FT': 'orange',
    'JP': 'pink'
  }
  return colors[dimension] || 'grey'
}

async function cargarPreguntas() {
  try {
    loading.value = true
    const response = await testService.obtenerTodasPreguntas()
    preguntas.value = response.preguntas
  } catch (error) {
    console.error('Error cargando preguntas:', error)
    $q.notify({
      type: 'negative',
      message: 'Error al cargar preguntas'
    })
  } finally {
    loading.value = false
  }
}

function iniciarEdicion(pregunta) {
  editando.value = pregunta.id_pregunta
  preguntaEdit.value = { ...pregunta }
}

function cancelarEdicion() {
  editando.value = null
  preguntaEdit.value = {}
}

async function guardarEdicion() {
  try {
    loading.value = true

    await testService.actualizarPregunta(preguntaEdit.value.id_pregunta, {
      texto_izquierda: preguntaEdit.value.texto_izquierda,
      texto_derecha: preguntaEdit.value.texto_derecha
    })

    // Actualizar en la lista
    const index = preguntas.value.findIndex(p => p.id_pregunta === preguntaEdit.value.id_pregunta)
    if (index !== -1) {
      preguntas.value[index] = { ...preguntaEdit.value }
    }

    cancelarEdicion()
    $q.notify({
      type: 'positive',
      message: 'Pregunta actualizada exitosamente'
    })
  } catch (error) {
    console.error('Error actualizando pregunta:', error)
    $q.notify({
      type: 'negative',
      message: error.message || 'Error al actualizar pregunta'
    })
  } finally {
    loading.value = false
  }
}

async function toggleActiva(pregunta) {
  try {
    const nuevaActiva = !pregunta.activa

    const response = await api.patch(`/test/admin/preguntas/${pregunta.id_pregunta}/toggle`, {
      activa: nuevaActiva
    })

    if (response.data.success) {
      pregunta.activa = nuevaActiva
      $q.notify({
        type: 'positive',
        message: `Pregunta ${nuevaActiva ? 'activada' : 'desactivada'} exitosamente`
      })
    }
  } catch {
    $q.notify({
      type: 'negative',
      message: 'Error al actualizar estado de pregunta'
    })
  }
}

async function crearPregunta() {
  try {
    loading.value = true

    const response = await testService.crearPregunta(nuevaPregunta.value)

    // Agregar a la lista
    preguntas.value.push(response.pregunta)

    // Resetear formulario y cerrar diálogo
    nuevaPregunta.value = {
      texto_izquierda: '',
      texto_derecha: '',
      dimension: null,
      peso: null,
      orden: null,
      activa: true
    }
    mostrarDialogCrear.value = false

    // Recargar preguntas para asegurar orden correcto
    await cargarPreguntas()

    $q.notify({
      type: 'positive',
      message: 'Pregunta creada exitosamente'
    })
  } catch (error) {
    console.error('Error creando pregunta:', error)
    $q.notify({
      type: 'negative',
      message: error.message || 'Error al crear pregunta'
    })
  } finally {
    loading.value = false
  }
}

async function confirmarEliminar(pregunta) {
  $q.dialog({
    title: 'Confirmar eliminación',
    message: `¿Estás seguro de que deseas eliminar la pregunta "${pregunta.texto_izquierda.substring(0, 50)}..."?`,
    cancel: true,
    persistent: true
  }).onOk(async () => {
    try {
      loading.value = true

      await testService.eliminarPregunta(pregunta.id_pregunta)

      // Remover de la lista
      const index = preguntas.value.findIndex(p => p.id_pregunta === pregunta.id_pregunta)
      if (index !== -1) {
        preguntas.value.splice(index, 1)
      }

      $q.notify({
        type: 'positive',
        message: 'Pregunta eliminada exitosamente'
      })
    } catch (error) {
      console.error('Error eliminando pregunta:', error)
      $q.notify({
        type: 'negative',
        message: error.message || 'Error al eliminar pregunta'
      })
    } finally {
      loading.value = false
    }
  })
}

onMounted(() => {
  cargarPreguntas()
})
</script>

<style scoped>
.q-page {
  min-height: calc(100vh - 64px);
  height: 100%;
  padding: 24px !important;
}

:deep(.q-table tbody td) {
  font-size: 0.9rem;
}

:deep(.q-table__card) {
  box-shadow: none;
}

@media (max-width: 768px) {
  .q-page {
    min-height: calc(100vh - 60px);
    padding: 16px !important;
  }
  
  .text-h4 {
    font-size: 1.8rem;
  }
  
  :deep(.q-table) {
    font-size: 0.85rem;
  }
}

@media (max-width: 480px) {
  .q-page {
    padding: 12px !important;
  }
  
  .text-h4 {
    font-size: 1.5rem;
  }
  
  :deep(.q-table tbody td) {
    font-size: 0.8rem;
  }
}

@media (max-height: 700px) {
  .q-page {
    padding: 16px !important;
  }
  
  .text-h4 {
    font-size: 1.4rem;
    margin-bottom: 4px !important;
  }
  
  .text-subtitle2 {
    font-size: 0.875rem;
  }
}
</style>
