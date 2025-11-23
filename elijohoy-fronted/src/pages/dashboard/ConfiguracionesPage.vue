<template>
  <q-page class="configuraciones-page">
    <div class="configuraciones-container">
      <!-- Page Header -->
      <div class="page-header">
        <h1 class="text-h4 text-weight-bold text-primary q-mb-sm">
          Configuraciones
        </h1>
        <p class="text-body1 text-grey-7">
          Administra tu perfil
        </p>
      </div>

      <!-- Content Row -->
      <div class="content-row">
        <!-- Profile Information -->
        <q-card class="profile-card" flat bordered>
          <q-card-section>
            <div class="card-header">
              <q-icon name="person" size="32px" color="primary" class="q-mr-sm" />
              <div class="text-h6 text-weight-bold">Información del Perfil</div>
            </div>

            <q-form @submit="updateProfile" class="q-gutter-md">
              <div class="form-row">
                <q-input
                  v-model="profileForm.nombre"
                  label="Nombre"
                  outlined
                  color="purple-7"
                  :rules="[val => !!val || 'El nombre es requerido']"
                  lazy-rules
                >
                  <template v-slot:prepend>
                    <q-icon name="badge" color="purple-7" />
                  </template>
                </q-input>

                <q-input
                  v-model="profileForm.apellidos"
                  label="Apellidos"
                  outlined
                  color="purple-7"
                  :rules="[val => !!val || 'Los apellidos son requeridos']"
                  lazy-rules
                >
                  <template v-slot:prepend>
                    <q-icon name="badge" color="purple-7" />
                  </template>
                </q-input>
              </div>

              <div class="form-row">
                <q-input
                  v-model="profileForm.email"
                  label="Correo Electrónico"
                  type="email"
                  outlined
                  readonly
                  color="purple-7"
                  hint="El email no se puede modificar"
                >
                  <template v-slot:prepend>
                    <q-icon name="email" color="purple-7" />
                  </template>
                </q-input>

                <q-input
                  v-model="profileForm.edad"
                  type="number"
                  label="Edad"
                  outlined
                  color="purple-7"
                  :rules="[val => !!val || 'La edad es requerida', val => val > 0 || 'Edad inválida']"
                  lazy-rules
                >
                  <template v-slot:prepend>
                    <q-icon name="cake" color="purple-7" />
                  </template>
                </q-input>
              </div>

              <div class="form-row">
                <q-select
                  v-model="profileForm.genero"
                  :options="['Masculino', 'Femenino', 'Otro']"
                  label="Género"
                  outlined
                  color="purple-7"
                >
                  <template v-slot:prepend>
                    <q-icon name="wc" color="purple-7" />
                  </template>
                </q-select>

                <q-input
                  v-model="profileForm.ciudad"
                  label="Ciudad"
                  outlined
                  color="purple-7"
                >
                  <template v-slot:prepend>
                    <q-icon name="location_city" color="purple-7" />
                  </template>
                </q-input>
              </div>

              <div class="form-row">
                <q-input
                  v-model="profileForm.pais"
                  label="País"
                  outlined
                  color="purple-7"
                >
                  <template v-slot:prepend>
                    <q-icon name="public" color="purple-7" />
                  </template>
                </q-input>

                <q-input
                  v-model="profileForm.institucion_educativa"
                  label="Institución Educativa"
                  outlined
                  color="purple-7"
                >
                  <template v-slot:prepend>
                    <q-icon name="school" color="purple-7" />
                  </template>
                </q-input>
              </div>

              <div class="form-row-3">
                <q-input
                  v-model="profileForm.grado"
                  label="Grado"
                  outlined
                  color="purple-7"
                >
                  <template v-slot:prepend>
                    <q-icon name="grade" color="purple-7" />
                  </template>
                </q-input>

                <q-input
                  v-model="profileForm.seccion"
                  label="Sección"
                  outlined
                  color="purple-7"
                >
                  <template v-slot:prepend>
                    <q-icon name="class" color="purple-7" />
                  </template>
                </q-input>

                <q-input
                  v-model="profileForm.turno"
                  label="Turno"
                  outlined
                  color="purple-7"
                >
                  <template v-slot:prepend>
                    <q-icon name="schedule" color="purple-7" />
                  </template>
                </q-input>
              </div>

              <div class="text-right">
                <q-btn
                  unelevated
                  type="submit"
                  color="primary"
                  label="Guardar Cambios"
                  icon="save"
                  :loading="profileLoading"
                  no-caps
                />
              </div>
            </q-form>
          </q-card-section>
        </q-card>

        <!-- Sidebar Cards -->
        <div class="sidebar-cards">
          <!-- Account Settings -->
          <q-card class="account-card" flat bordered>
            <q-card-section>
              <div class="card-header">
                <q-icon name="security" size="32px" color="secondary" class="q-mr-sm" />
                <div class="text-h6 text-weight-bold">Configuración de Cuenta</div>
              </div>

              <div class="buttons-container">
                <q-btn
                  outline
                  color="primary"
                  icon="lock"
                  label="Cambiar Contraseña"
                  @click="showPasswordDialog = true"
                  class="full-width"
                  no-caps
                />

                <q-btn
                  outline
                  color="negative"
                  icon="logout"
                  label="Cerrar Sesión"
                  @click="logout"
                  class="full-width"
                  no-caps
                />
              </div>
            </q-card-section>
          </q-card>

          <!-- Account Status -->
          <q-card class="status-card" flat bordered>
            <q-card-section>
              <div class="text-h6 text-weight-bold q-mb-md">Estado de la Cuenta</div>

              <div class="status-items">
                <div class="status-item">
                  <q-icon
                    :name="user.email_verificado ? 'verified' : 'error'"
                    :color="user.email_verificado ? 'positive' : 'negative'"
                    class="q-mr-sm"
                  />
                  <span>Email {{ user.email_verificado ? 'Verificado' : 'No Verificado' }}</span>
                </div>

                <div class="status-item">
                  <q-icon
                    name="check_circle"
                    color="positive"
                    class="q-mr-sm"
                  />
                  <span>Cuenta Activa</span>
                </div>

                <div class="status-item">
                  <q-icon name="schedule" color="info" class="q-mr-sm" />
                  <span>Miembro desde {{ formatDate(user.creado_en) }}</span>
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </div>

    <!-- Change Password Dialog -->
    <q-dialog v-model="showPasswordDialog">
      <q-card style="min-width: 400px">
        <q-card-section class="row items-center">
          <q-icon name="lock" size="32px" color="primary" class="q-mr-sm" />
          <span class="text-h6">Cambiar Contraseña</span>
        </q-card-section>

        <q-card-section>
          <q-form @submit="changePassword" class="q-gutter-md">
            <q-input
              v-model="passwordForm.current_password"
              :type="showCurrentPassword ? 'text' : 'password'"
              label="Contraseña Actual"
              outlined
              :rules="[val => !!val || 'Ingresa tu contraseña actual']"
              lazy-rules
            >
              <template v-slot:append>
                <q-icon
                  :name="showCurrentPassword ? 'visibility' : 'visibility_off'"
                  class="cursor-pointer"
                  @click="showCurrentPassword = !showCurrentPassword"
                />
              </template>
            </q-input>

            <q-input
              v-model="passwordForm.new_password"
              :type="showNewPassword ? 'text' : 'password'"
              label="Nueva Contraseña"
              outlined
              :rules="passwordRules"
              lazy-rules
            >
              <template v-slot:append>
                <q-icon
                  :name="showNewPassword ? 'visibility' : 'visibility_off'"
                  class="cursor-pointer"
                  @click="showNewPassword = !showNewPassword"
                />
              </template>
            </q-input>

            <q-input
              v-model="passwordForm.confirm_password"
              :type="showConfirmPassword ? 'text' : 'password'"
              label="Confirmar Nueva Contraseña"
              outlined
              :rules="[val => !!val || 'Confirma la nueva contraseña',
                       val => val === passwordForm.new_password || 'Las contraseñas no coinciden']"
              lazy-rules
            >
              <template v-slot:append>
                <q-icon
                  :name="showConfirmPassword ? 'visibility' : 'visibility_off'"
                  class="cursor-pointer"
                  @click="showConfirmPassword = !showConfirmPassword"
                />
              </template>
            </q-input>

            <div class="row q-gutter-sm justify-end">
              <q-btn flat label="Cancelar" color="grey" v-close-popup />
              <q-btn 
                unelevated 
                type="submit" 
                label="Cambiar" 
                color="primary"
                :loading="passwordLoading"
              />
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import { defineComponent, ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useAuthStore } from 'src/stores/auth'
import { AuthService } from 'src/services/auth'

export default defineComponent({
  name: 'ConfiguracionesPage',

  setup() {
    const $q = useQuasar()
    const router = useRouter()
    const authStore = useAuthStore()

    const profileForm = ref({
      nombre: '',
      apellidos: '',
      edad: null,
      genero: null,
      email: '',
      ciudad: '',
      pais: '',
      institucion_educativa: '',
      grado: '',
      seccion: '',
      turno: ''
    })

    const passwordForm = ref({
      current_password: '',
      new_password: '',
      confirm_password: ''
    })

    const showPasswordDialog = ref(false)
    const showCurrentPassword = ref(false)
    const showNewPassword = ref(false)
    const showConfirmPassword = ref(false)
    const profileLoading = ref(false)
    const passwordLoading = ref(false)

    const user = computed(() => authStore.user || {})

    const passwordRules = computed(() => [
      val => !!val || 'La contraseña es requerida',
      val => val.length >= 8 || 'Mínimo 8 caracteres',
      val => /[A-Z]/.test(val) || 'Debe contener al menos una mayúscula',
      val => /[a-z]/.test(val) || 'Debe contener al menos una minúscula',
      val => /[0-9]/.test(val) || 'Debe contener al menos un número',
      val => /[!@#$%^&*(),.?":{}|<>]/.test(val) || 'Debe contener al menos un símbolo'
    ])

    const formatDate = (dateString) => {
      if (!dateString) return 'No disponible'
      const date = new Date(dateString)
      return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }

    const updateProfile = async () => {
      profileLoading.value = true

      try {
        // Preparar datos para enviar
        const profileData = { ...profileForm.value }
        
        // Convertir género a minúsculas para el backend
        if (profileData.genero) {
          profileData.genero = profileData.genero.toLowerCase()
        }

        const result = await authStore.updateProfile(profileData)

        if (result.success) {
          $q.notify({
            message: 'Perfil actualizado exitosamente',
            color: 'positive',
            icon: 'check'
          })
        } else {
          $q.notify({
            message: result.message,
            color: 'negative',
            icon: 'error'
          })
        }
      } catch (error) {
        console.error('Update profile error:', error)
        $q.notify({
          message: 'Error actualizando el perfil',
          color: 'negative',
          icon: 'error'
        })
      } finally {
        profileLoading.value = false
      }
    }

    const changePassword = async () => {
      passwordLoading.value = true

      try {
        const result = await AuthService.changePassword(
          passwordForm.value.current_password,
          passwordForm.value.new_password
        )

        if (result.success) {
          $q.notify({
            message: 'Contraseña cambiada exitosamente',
            color: 'positive',
            icon: 'check'
          })

          showPasswordDialog.value = false
          passwordForm.value = {
            current_password: '',
            new_password: '',
            confirm_password: ''
          }
        } else {
          // Mostrar mensaje de error
          let errorMsg = result.message || 'Error cambiando la contraseña'
          if (result.errors && result.errors.length > 0) {
            errorMsg = result.errors.join(', ')
          }
          $q.notify({
            message: errorMsg,
            color: 'negative',
            icon: 'error'
          })
        }
      } catch (error) {
        console.error('Change password error:', error)
        $q.notify({
          message: 'Error cambiando la contraseña',
          color: 'negative',
          icon: 'error'
        })
      } finally {
        passwordLoading.value = false
      }
    }

    const logout = async () => {
      $q.dialog({
        title: 'Cerrar Sesión',
        message: '¿Estás seguro que deseas cerrar sesión?',
        cancel: true,
        persistent: true
      }).onOk(async () => {
        try {
          await authStore.logout()
          $q.notify({
            message: 'Sesión cerrada exitosamente',
            color: 'positive',
            icon: 'check'
          })
          router.push('/')
        } catch (error) {
          console.error('Logout error:', error)
        }
      })
    }

    onMounted(() => {
      if (authStore.user) {
        // Los datos del alumno están directamente en authStore.user
        // No hay un objeto separado 'alumno'
        
        // Función para capitalizar género
        const capitalizeGenero = (genero) => {
          if (!genero) return null
          if (genero === 'masculino') return 'Masculino'
          if (genero === 'femenino') return 'Femenino'
          if (genero === 'otro') return 'Otro'
          return genero
        }
        
        profileForm.value = {
          nombre: authStore.user.nombre || '',
          apellidos: authStore.user.apellidos || '',
          edad: authStore.user.edad || null,
          genero: capitalizeGenero(authStore.user.genero) || null,
          email: authStore.user.email || '',
          ciudad: authStore.user.ciudad || '',
          pais: authStore.user.pais || '',
          institucion_educativa: authStore.user.institucion_educativa || '',
          grado: authStore.user.grado || '',
          seccion: authStore.user.seccion || '',
          turno: authStore.user.turno || ''
        }
      }
    })

    return {
      profileForm,
      passwordForm,
      showPasswordDialog,
      showCurrentPassword,
      showNewPassword,
      showConfirmPassword,
      profileLoading,
      passwordLoading,
      user,
      passwordRules,
      formatDate,
      updateProfile,
      changePassword,
      logout
    }
  }
})
</script>

<style scoped>
.configuraciones-page {
  min-height: 100vh;
  background: linear-gradient(to bottom, #F3F4F6, #FFFFFF);
  padding: 1.5rem;
  overflow-x: hidden;
}

.configuraciones-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.page-header {
  margin-bottom: 0.5rem;
}

.page-header h1 {
  color: #7C3AED !important;
}

/* Card Header */
.card-header {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

/* Content Row - Flexbox */
.content-row {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.profile-card {
  flex: 2 1 500px;
  min-width: 300px;
}

.sidebar-cards {
  flex: 1 1 280px;
  min-width: 280px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Form Rows */
.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.form-row-3 {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

/* Buttons Container */
.buttons-container {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

/* Status Items */
.status-items {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.status-item {
  display: flex;
  align-items: center;
}

.profile-card,
.account-card,
.status-card {
  border-radius: 1.25rem;
  border: 2px solid #E5E7EB;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  background: white;
}

.profile-card:hover,
.account-card:hover,
.status-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 32px rgba(124, 58, 237, 0.15);
  border-color: #7C3AED;
}

.profile-card :deep(.text-primary),
.account-card :deep(.text-secondary) {
  color: #7C3AED !important;
}

.profile-card :deep(.q-field__control) {
  background: #F9FAFB;
  border-radius: 0.75rem;
}

.profile-card :deep(.q-field__control):hover {
  background: #F3F4F6;
}

.profile-card :deep(.q-btn[type="submit"]) {
  background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%);
  border-radius: 0.75rem;
  font-weight: 600;
  padding: 0.75rem 2rem;
  box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3);
  transition: all 0.3s ease;
}

.profile-card :deep(.q-btn[type="submit"]:hover) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4);
}

.account-card :deep(.q-btn) {
  border-radius: 0.75rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.account-card :deep(.q-btn:hover) {
  transform: translateX(4px);
}

.status-card {
  border-color: #10B981;
  background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
}

/* Responsive */
@media (max-width: 768px) {
  .configuraciones-page {
    padding: 1rem;
  }

  .content-row {
    flex-direction: column;
    gap: 1rem;
  }

  .profile-card,
  .sidebar-cards {
    flex: 1 1 auto;
    min-width: 100%;
  }

  .profile-card,
  .account-card,
  .status-card {
    border-radius: 1rem;
  }

  .page-header h1 {
    font-size: 1.5rem;
  }

  .form-row,
  .form-row-3 {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .configuraciones-page {
    padding: 0.75rem;
  }

  .profile-card,
  .account-card,
  .status-card {
    border-radius: 0.875rem;
  }

  .page-header h1 {
    font-size: 1.3rem;
  }
}
</style>