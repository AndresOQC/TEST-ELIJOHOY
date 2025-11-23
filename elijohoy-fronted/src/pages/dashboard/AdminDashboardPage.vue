<template>
  <q-page class="admin-dashboard-page">
    <div class="admin-container">
      <!-- Header -->
      <div class="page-header">
        <div class="header-content">
          <h1 class="text-h4 text-weight-bold text-primary">
            <q-icon name="admin_panel_settings" class="q-mr-sm" />
            Panel de Administración
          </h1>
          <p class="text-body1 text-grey-7">
            Resumen de estadísticas y datos de tests vocacionales
          </p>
        </div>
        <div class="header-actions">
          <q-btn
            outline
            color="primary"
            icon="refresh"
            label="Actualizar"
            @click="cargarDatos"
            :loading="loading"
            no-caps
          />
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="stats-grid" v-if="!loading">
        <q-card class="stat-card stat-primary" flat>
          <q-card-section>
            <div class="stat-icon">
              <q-icon name="assignment_turned_in" size="40px" />
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.total_tests }}</div>
              <div class="stat-label">Tests Completados</div>
            </div>
          </q-card-section>
        </q-card>

        <q-card class="stat-card stat-secondary" flat>
          <q-card-section>
            <div class="stat-icon">
              <q-icon name="people" size="40px" />
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.total_usuarios }}</div>
              <div class="stat-label">Usuarios Registrados</div>
            </div>
          </q-card-section>
        </q-card>

        <q-card class="stat-card stat-accent" flat>
          <q-card-section>
            <div class="stat-icon">
              <q-icon name="trending_up" size="40px" />
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.tests_ultimo_mes }}</div>
              <div class="stat-label">Tests (Último Mes)</div>
            </div>
          </q-card-section>
        </q-card>

        <q-card class="stat-card stat-info" flat>
          <q-card-section>
            <div class="stat-icon">
              <q-icon name="psychology" size="40px" />
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.distribucion_tipos?.length || 0 }}</div>
              <div class="stat-label">Tipos Detectados</div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading-container">
        <q-spinner color="primary" size="60px" />
        <p class="text-grey-7 q-mt-md">Cargando estadísticas...</p>
      </div>

      <!-- Content Grid -->
      <div class="content-grid" v-if="!loading">
        <!-- Distribution by Personality Type -->
        <q-card class="distribution-card" flat bordered>
          <q-card-section>
            <div class="card-header">
              <q-icon name="pie_chart" size="28px" color="primary" class="q-mr-sm" />
              <span class="text-h6 text-weight-bold">Distribución por Tipo de Personalidad</span>
            </div>
          </q-card-section>
          <q-card-section class="q-pt-none">
            <q-table
              :rows="stats.distribucion_tipos || []"
              :columns="columnsDistribucion"
              row-key="tipo"
              flat
              bordered
              dense
              :pagination="{ rowsPerPage: 16 }"
              class="distribution-table"
            >
              <template v-slot:body-cell-tipo="props">
                <q-td :props="props">
                  <q-chip
                    :color="getColorForType(props.row.tipo)"
                    text-color="white"
                    dense
                  >
                    {{ props.row.tipo }}
                  </q-chip>
                </q-td>
              </template>
              <template v-slot:body-cell-porcentaje="props">
                <q-td :props="props">
                  <div class="progress-container">
                    <q-linear-progress
                      :value="getPorcentaje(props.row.cantidad)"
                      :color="getColorForType(props.row.tipo)"
                      class="q-mr-sm"
                      style="width: 100px"
                    />
                    <span>{{ getPorcentajeTexto(props.row.cantidad) }}%</span>
                  </div>
                </q-td>
              </template>
            </q-table>
          </q-card-section>
        </q-card>

        <!-- Users Table -->
        <q-card class="users-card" flat bordered>
          <q-card-section>
            <div class="card-header">
              <div class="header-left">
                <q-icon name="table_chart" size="28px" color="primary" class="q-mr-sm" />
                <span class="text-h6 text-weight-bold">Usuarios y Resultados de Tests</span>
              </div>
              <div class="header-right">
                <q-btn
                  flat
                  color="green"
                  icon="download"
                  label="Excel"
                  @click="exportarExcel"
                  no-caps
                  class="q-mr-sm"
                />
                <q-btn
                  flat
                  color="red"
                  icon="picture_as_pdf"
                  label="PDF"
                  @click="exportarPDF"
                  no-caps
                />
              </div>
            </div>
          </q-card-section>

          <q-card-section class="q-pt-none">
            <q-input
              v-model="filtro"
              outlined
              dense
              placeholder="Buscar por nombre, email o tipo..."
              class="q-mb-md"
            >
              <template v-slot:prepend>
                <q-icon name="search" />
              </template>
              <template v-slot:append v-if="filtro">
                <q-icon name="close" class="cursor-pointer" @click="filtro = ''" />
              </template>
            </q-input>

            <q-table
              :rows="usuariosFiltrados"
              :columns="columnsUsuarios"
              row-key="id_sesion"
              flat
              bordered
              :pagination="paginacion"
              @update:pagination="paginacion = $event"
              class="users-table"
            >
              <template v-slot:body-cell-nombre_completo="props">
                <q-td :props="props">
                  <div class="user-info">
                    <q-avatar size="32px" color="primary" text-color="white" class="q-mr-sm">
                      {{ getInitials(props.row.nombre, props.row.apellidos) }}
                    </q-avatar>
                    <div>
                      <div class="text-weight-medium">{{ props.row.nombre }} {{ props.row.apellidos }}</div>
                      <div class="text-caption text-grey-6">{{ props.row.email }}</div>
                    </div>
                  </div>
                </q-td>
              </template>
              <template v-slot:body-cell-tipo_personalidad="props">
                <q-td :props="props">
                  <q-chip
                    :color="getColorForType(props.row.tipo_personalidad)"
                    text-color="white"
                    dense
                  >
                    {{ props.row.tipo_personalidad }}
                  </q-chip>
                </q-td>
              </template>
              <template v-slot:body-cell-fecha_test="props">
                <q-td :props="props">
                  {{ formatDate(props.row.fecha_test) }}
                </q-td>
              </template>
              <template v-slot:body-cell-acciones="props">
                <q-td :props="props">
                  <q-btn
                    flat
                    round
                    dense
                    icon="visibility"
                    color="primary"
                    @click="verResultados(props.row.id_sesion)"
                  >
                    <q-tooltip>Ver resultados</q-tooltip>
                  </q-btn>
                </q-td>
              </template>
            </q-table>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { api } from 'src/services/api'

export default defineComponent({
  name: 'AdminDashboardPage',

  setup() {
    const $q = useQuasar()
    const router = useRouter()

    const loading = ref(true)
    const filtro = ref('')
    const stats = ref({
      total_tests: 0,
      total_usuarios: 0,
      tests_ultimo_mes: 0,
      distribucion_tipos: []
    })
    const usuariosTests = ref([])
    const paginacion = ref({
      sortBy: 'fecha_test',
      descending: true,
      page: 1,
      rowsPerPage: 10
    })

    const columnsDistribucion = [
      { name: 'tipo', label: 'Tipo', field: 'tipo', align: 'left', sortable: true },
      { name: 'cantidad', label: 'Cantidad', field: 'cantidad', align: 'center', sortable: true },
      { name: 'porcentaje', label: 'Porcentaje', field: 'cantidad', align: 'left' }
    ]

    const columnsUsuarios = [
      { name: 'nombre_completo', label: 'Usuario', field: 'nombre', align: 'left', sortable: true },
      { name: 'institucion', label: 'Institución', field: 'institucion', align: 'left', sortable: true },
      { name: 'tipo_personalidad', label: 'Tipo MBTI', field: 'tipo_personalidad', align: 'center', sortable: true },
      { name: 'fecha_test', label: 'Fecha Test', field: 'fecha_test', align: 'center', sortable: true },
      { name: 'acciones', label: 'Acciones', field: 'acciones', align: 'center' }
    ]

    const usuariosFiltrados = computed(() => {
      if (!filtro.value) return usuariosTests.value
      const busqueda = filtro.value.toLowerCase()
      return usuariosTests.value.filter(u =>
        u.nombre?.toLowerCase().includes(busqueda) ||
        u.apellidos?.toLowerCase().includes(busqueda) ||
        u.email?.toLowerCase().includes(busqueda) ||
        u.tipo_personalidad?.toLowerCase().includes(busqueda) ||
        u.institucion?.toLowerCase().includes(busqueda)
      )
    })

    const totalTests = computed(() => stats.value.total_tests || 1)

    const cargarDatos = async () => {
      loading.value = true
      try {
        const response = await api.get('/test/admin/dashboard-stats')
        if (response.data.success) {
          stats.value = response.data.stats
          usuariosTests.value = response.data.usuarios_tests || []
        }
      } catch (error) {
        console.error('Error cargando datos:', error)
        $q.notify({
          type: 'negative',
          message: 'Error al cargar estadísticas'
        })
      } finally {
        loading.value = false
      }
    }

    const getColorForType = (tipo) => {
      const colores = {
        'INTJ': 'deep-purple', 'INTP': 'indigo', 'ENTJ': 'purple', 'ENTP': 'violet',
        'INFJ': 'green', 'INFP': 'teal', 'ENFJ': 'light-green', 'ENFP': 'lime',
        'ISTJ': 'blue', 'ISFJ': 'light-blue', 'ESTJ': 'cyan', 'ESFJ': 'blue-grey',
        'ISTP': 'orange', 'ISFP': 'deep-orange', 'ESTP': 'amber', 'ESFP': 'yellow-9'
      }
      return colores[tipo] || 'primary'
    }

    const getPorcentaje = (cantidad) => {
      return cantidad / totalTests.value
    }

    const getPorcentajeTexto = (cantidad) => {
      return ((cantidad / totalTests.value) * 100).toFixed(1)
    }

    const getInitials = (nombre, apellidos) => {
      const n = nombre?.charAt(0) || ''
      const a = apellidos?.charAt(0) || ''
      return (n + a).toUpperCase()
    }

    const formatDate = (dateString) => {
      if (!dateString) return '-'
      const date = new Date(dateString)
      return date.toLocaleDateString('es-ES', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      })
    }

    const verResultados = (idSesion) => {
      router.push(`/dashboard/test-resultados/${idSesion}`)
    }

    const exportarExcel = () => {
      // Crear CSV
      const headers = ['Nombre', 'Apellidos', 'Email', 'Institución', 'Tipo Personalidad', 'Fecha Test']
      const rows = usuariosFiltrados.value.map(u => [
        u.nombre || '',
        u.apellidos || '',
        u.email || '',
        u.institucion || '',
        u.tipo_personalidad || '',
        formatDate(u.fecha_test)
      ])

      let csvContent = '\uFEFF' // BOM para UTF-8
      csvContent += headers.join(',') + '\n'
      rows.forEach(row => {
        csvContent += row.map(cell => `"${cell}"`).join(',') + '\n'
      })

      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
      const link = document.createElement('a')
      link.href = URL.createObjectURL(blob)
      link.download = `tests_vocacionales_${new Date().toISOString().split('T')[0]}.csv`
      link.click()

      $q.notify({
        type: 'positive',
        message: 'Archivo Excel (CSV) descargado exitosamente'
      })
    }

    const exportarPDF = () => {
      // Crear contenido HTML para imprimir
      const printContent = `
        <!DOCTYPE html>
        <html>
        <head>
          <title>Reporte de Tests Vocacionales</title>
          <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #7C3AED; text-align: center; }
            h2 { color: #333; margin-top: 30px; }
            .stats { display: flex; justify-content: space-around; margin: 20px 0; }
            .stat-box { text-align: center; padding: 15px; border: 1px solid #ddd; border-radius: 8px; }
            .stat-value { font-size: 24px; font-weight: bold; color: #7C3AED; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #7C3AED; color: white; }
            tr:nth-child(even) { background-color: #f9f9f9; }
            .fecha { text-align: right; color: #666; font-size: 12px; margin-bottom: 20px; }
          </style>
        </head>
        <body>
          <h1>ElijoHoy - Reporte de Tests Vocacionales</h1>
          <p class="fecha">Generado el: ${new Date().toLocaleDateString('es-ES')}</p>

          <div class="stats">
            <div class="stat-box">
              <div class="stat-value">${stats.value.total_tests}</div>
              <div>Tests Completados</div>
            </div>
            <div class="stat-box">
              <div class="stat-value">${stats.value.total_usuarios}</div>
              <div>Usuarios Registrados</div>
            </div>
            <div class="stat-box">
              <div class="stat-value">${stats.value.tests_ultimo_mes}</div>
              <div>Tests (Último Mes)</div>
            </div>
          </div>

          <h2>Distribución por Tipo de Personalidad</h2>
          <table>
            <tr><th>Tipo MBTI</th><th>Cantidad</th><th>Porcentaje</th></tr>
            ${stats.value.distribucion_tipos?.map(t =>
              `<tr><td>${t.tipo}</td><td>${t.cantidad}</td><td>${getPorcentajeTexto(t.cantidad)}%</td></tr>`
            ).join('') || ''}
          </table>

          <h2>Usuarios y Resultados</h2>
          <table>
            <tr><th>Nombre</th><th>Email</th><th>Institución</th><th>Tipo MBTI</th><th>Fecha</th></tr>
            ${usuariosFiltrados.value.map(u =>
              `<tr>
                <td>${u.nombre} ${u.apellidos}</td>
                <td>${u.email}</td>
                <td>${u.institucion || '-'}</td>
                <td>${u.tipo_personalidad}</td>
                <td>${formatDate(u.fecha_test)}</td>
              </tr>`
            ).join('')}
          </table>
        </body>
        </html>
      `

      const printWindow = window.open('', '_blank')
      printWindow.document.write(printContent)
      printWindow.document.close()
      printWindow.print()

      $q.notify({
        type: 'positive',
        message: 'PDF listo para imprimir/guardar'
      })
    }

    onMounted(() => {
      cargarDatos()
    })

    return {
      loading,
      filtro,
      stats,
      usuariosTests,
      usuariosFiltrados,
      paginacion,
      columnsDistribucion,
      columnsUsuarios,
      cargarDatos,
      getColorForType,
      getPorcentaje,
      getPorcentajeTexto,
      getInitials,
      formatDate,
      verResultados,
      exportarExcel,
      exportarPDF
    }
  }
})
</script>

<style scoped>
.admin-dashboard-page {
  background: #f5f7fa;
  min-height: 100vh;
  padding: 24px;
}

.admin-container {
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 16px;
}

.header-content h1 {
  margin: 0;
  display: flex;
  align-items: center;
}

.header-content p {
  margin: 4px 0 0 0;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  border-radius: 16px;
  overflow: hidden;
}

.stat-card .q-card__section {
  display: flex;
  align-items: center;
  padding: 24px;
}

.stat-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
}

.stat-primary { background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%); color: white; }
.stat-primary .stat-icon { background: rgba(255,255,255,0.2); }

.stat-secondary { background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%); color: white; }
.stat-secondary .stat-icon { background: rgba(255,255,255,0.2); }

.stat-accent { background: linear-gradient(135deg, #10B981 0%, #059669 100%); color: white; }
.stat-accent .stat-icon { background: rgba(255,255,255,0.2); }

.stat-info { background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%); color: white; }
.stat-info .stat-icon { background: rgba(255,255,255,0.2); }

.stat-value {
  font-size: 32px;
  font-weight: 700;
  line-height: 1;
}

.stat-label {
  font-size: 14px;
  opacity: 0.9;
  margin-top: 4px;
}

/* Content Grid */
.content-grid {
  display: grid;
  grid-template-columns: 350px 1fr;
  gap: 24px;
}

@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}

.distribution-card,
.users-card {
  border-radius: 16px;
  background: white;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
}

.header-left {
  display: flex;
  align-items: center;
}

.progress-container {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
}

/* Table styling */
.distribution-table,
.users-table {
  border-radius: 8px;
}

.distribution-table :deep(.q-table__top),
.users-table :deep(.q-table__top) {
  padding: 0;
}

.distribution-table :deep(th),
.users-table :deep(th) {
  font-weight: 600;
  background: #f8f9fa;
}

@media (max-width: 768px) {
  .admin-dashboard-page {
    padding: 16px;
  }

  .stats-grid {
    grid-template-columns: 1fr 1fr;
  }

  .stat-card .q-card__section {
    padding: 16px;
    flex-direction: column;
    text-align: center;
  }

  .stat-icon {
    margin-right: 0;
    margin-bottom: 12px;
  }

  .stat-value {
    font-size: 24px;
  }
}
</style>
