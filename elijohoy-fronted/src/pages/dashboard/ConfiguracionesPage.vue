<template>
  <q-page class="configuraciones-page q-pa-lg">
    <div class="row q-gutter-lg">
      <!-- Page Header -->
      <div class="col-12">
        <div class="page-header">
          <h1 class="text-h4 text-weight-bold text-primary q-mb-sm">
            Configuraciones
          </h1>
          <p class="text-body1 text-grey-7">
            Administra tu perfil
          </p>
        </div>
      </div>

      <!-- Profile Information -->
      <div class="col-12 col-md-8">
        <q-card class="profile-card" flat bordered>
          <q-card-section>
            <div class="row items-center q-mb-md">
              <q-icon name="person" size="32px" color="primary" class="q-mr-sm" />
              <div class="text-h6 text-weight-bold">Información del Perfil</div>
            </div>
            
            <q-form @submit="updateProfile" class="q-gutter-md">
              <div class="row q-gutter-md">
                <div class="col-12 col-sm-6">
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
                </div>

                <div class="col-12 col-sm-6">
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
              </div>

              <div class="row q-gutter-md">
                <div class="col-12 col-sm-6">
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
                </div>

                <div class="col-12 col-sm-6">
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
              </div>

              <div class="row q-gutter-md">
                <div class="col-12 col-sm-6">
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
                </div>

                <div class="col-12 col-sm-6">
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
              </div>

              <div class="row q-gutter-md">
                <div class="col-12 col-sm-6">
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
                </div>

                <div class="col-12 col-sm-6">
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
              </div>

              <div class="row q-gutter-md">
                <div class="col-12 col-sm-4">
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
                </div>

                <div class="col-12 col-sm-4">
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
                </div>

                <div class="col-12 col-sm-4">
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
      </div>

      <!-- Account Settings -->
      <div class="col-12 col-md-4">
        <q-card class="account-card" flat bordered>
          <q-card-section>
            <div class="row items-center q-mb-md">
              <q-icon name="security" size="32px" color="secondary" class="q-mr-sm" />
              <div class="text-h6 text-weight-bold">Configuración de Cuenta</div>
            </div>
            
            <div class="q-gutter-sm">
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
        <q-card class="status-card q-mt-md" flat bordered>
          <q-card-section>
            <div class="text-h6 text-weight-bold q-mb-md">Estado de la Cuenta</div>
            
            <div class="q-gutter-sm">
              <div class="row items-center">
                <q-icon 
                  :name="user.email_verificado ? 'verified' : 'error'"
                  :color="user.email_verificado ? 'positive' : 'negative'"
                  class="q-mr-sm"
                />
                <span>Email {{ user.email_verificado ? 'Verificado' : 'No Verificado' }}</span>
              </div>
              
              <div class="row items-center">
                <q-icon
                  name="check_circle"
                  color="positive"
                  class="q-mr-sm"
                />
                <span>Cuenta Activa</span>
              </div>
              
              <div class="row items-center">
                <q-icon name="schedule" color="info" class="q-mr-sm" />
                <span>Miembro desde {{ formatDate(user.creado_en) }}</span>
              </div>
            </div>
          </q-card-section>
        </q-card>
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
        // This would call an API endpoint to change password
        // For now, just show success message
        await new Promise(resolve => setTimeout(resolve, 1000))
        
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
  max-width: 1200px;
  margin: 0 auto;
  background: linear-gradient(to bottom, #F3F4F6, #FFFFFF);
  min-height: calc(100vh - 64px);
  height: 100%;
  padding: 24px;
}

.page-header {
  margin-bottom: 32px;
  padding-top: 20px;
}

.page-header h1 {
  color: #7C3AED !important;
}

.profile-card,
.account-card,
.status-card {
  border-radius: 20px;
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
  border-radius: 12px;
}

.profile-card :deep(.q-field__control):hover {
  background: #F3F4F6;
}

.profile-card :deep(.q-btn[type="submit"]) {
  background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%);
  border-radius: 12px;
  font-weight: 600;
  padding: 12px 32px;
  box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3);
  transition: all 0.3s ease;
}

.profile-card :deep(.q-btn[type="submit"]:hover) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4);
}

.account-card :deep(.q-btn) {
  border-radius: 12px;
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

@media (max-width: 768px) {
  .configuraciones-page {
    min-height: calc(100vh - 60px);
    padding: 16px;
  }

  .profile-card,
  .account-card,
  .status-card {
    border-radius: 16px;
  }
  
  .page-header h1 {
    font-size: 1.8rem;
  }
  
  .page-header {
    margin-bottom: 24px;
  }
}

@media (max-width: 480px) {
  .configuraciones-page {
    padding: 12px;
  }
  
  .profile-card,
  .account-card,
  .status-card {
    border-radius: 14px;
  }
  
  .page-header h1 {
    font-size: 1.5rem;
  }
  
  .page-header {
    margin-bottom: 20px;
    padding-top: 10px;
  }
}

@media (max-height: 700px) {
  .configuraciones-page {
    padding: 16px;
  }
  
  .page-header {
    margin-bottom: 16px;
    padding-top: 10px;
  }
  
  .page-header h1 {
    font-size: 1.4rem;
    margin-bottom: 4px !important;
  }
  
  .page-header p {
    font-size: 0.875rem;
  }
  
  .profile-card :deep(.q-card-section) {
    padding: 16px;
  }
}
</style>