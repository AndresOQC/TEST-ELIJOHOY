<template>
  <q-page class="q-pa-md">
    <div class="row q-mb-md">
      <div class="col">
        <div class="text-h4 text-weight-bold">Administrar Preguntas del Test</div>
        <div class="text-subtitle2 text-grey-7">
          Gestiona las 32 preguntas del test OEJTS
        </div>
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
              </div>
            </q-td>
          </template>
        </q-table>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import api from 'src/services/api'

const $q = useQuasar()

const loading = ref(false)
const preguntas = ref([])
const editando = ref(null)
const preguntaEdit = ref({})

const pagination = ref({
  rowsPerPage: 10
})

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
    const response = await api.get('/test/preguntas')

    if (response.data.success) {
      preguntas.value = response.data.preguntas
    }
  } catch {
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

    const response = await api.put(`/test/admin/preguntas/${preguntaEdit.value.id_pregunta}`, {
      texto_izquierda: preguntaEdit.value.texto_izquierda,
      texto_derecha: preguntaEdit.value.texto_derecha
    })

    if (response.data.success) {
      $q.notify({
        type: 'positive',
        message: 'Pregunta actualizada exitosamente'
      })

      // Actualizar en la lista
      const index = preguntas.value.findIndex(p => p.id_pregunta === preguntaEdit.value.id_pregunta)
      if (index !== -1) {
        preguntas.value[index] = { ...preguntaEdit.value }
      }

      cancelarEdicion()
    }
  } catch {
    $q.notify({
      type: 'negative',
      message: 'Error al actualizar pregunta'
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

onMounted(() => {
  cargarPreguntas()
})
</script>

<style scoped>
:deep(.q-table tbody td) {
  font-size: 0.9rem;
}

:deep(.q-table__card) {
  box-shadow: none;
}
</style>
