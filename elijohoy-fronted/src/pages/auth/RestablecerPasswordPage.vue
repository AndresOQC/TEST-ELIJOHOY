<template>
  <q-page class="reset-page">
    <div class="reset-container">
      <q-card class="reset-card glass-card">
        <q-card-section v-if="!passwordReset" class="text-center">
          <div class="reset-icon-wrapper q-mb-lg">
            <q-icon name="vpn_key" size="52px" color="white" />
          </div>
          <div class="text-h4 text-weight-bold text-white q-mb-sm">
            Nueva Contraseña
          </div>
          <div class="text-h6 text-weight-medium text-yellow-9 q-mb-sm">
            Ya casi terminamos
          </div>
          <div class="text-body1 text-white-7 q-mb-lg">
            Crea una contraseña segura para completar el restablecimiento
          </div>

          <q-form @submit="resetPassword" class="q-gutter-md">
            <q-input
              v-model="form.new_password"
              :type="showPassword ? 'text' : 'password'"
              label="Nueva Contraseña"
              outlined
              color="purple-7"
              :rules="passwordRules"
              lazy-rules
              class="modern-input"
            >
              <template v-slot:prepend>
                <q-icon name="lock" color="purple-7" />
              </template>
              <template v-slot:append>
                <q-icon
                  :name="showPassword ? 'visibility' : 'visibility_off'"
                  class="cursor-pointer"
                  color="purple-7"
                  @click="showPassword = !showPassword"
                />
              </template>
              <template v-slot:hint>
                <div class="text-caption" style="color: #7C3AED;">
                  Mín. 8 caracteres, una mayúscula, una minúscula, un número y un símbolo
                </div>
              </template>
            </q-input>

            <q-input
              v-model="form.confirm_password"
              :type="showConfirmPassword ? 'text' : 'password'"
              label="Confirmar Nueva Contraseña"
              outlined
              color="purple-7"
              :rules="[
                val => !!val || 'Confirma tu contraseña',
                val => val === form.new_password || 'Las contraseñas no coinciden'
              ]"
              lazy-rules
              class="modern-input"
            >
              <template v-slot:prepend>
                <q-icon name="lock_check" color="purple-7" />
              </template>
              <template v-slot:append>
                <q-icon
                  :name="showConfirmPassword ? 'visibility' : 'visibility_off'"
                  class="cursor-pointer"
                  color="purple-7"
                  @click="showConfirmPassword = !showConfirmPassword"
                />
              </template>
            </q-input>

            <q-btn
              unelevated
              type="submit"
              size="lg"
              color="yellow-9"
              text-color="purple-10"
              label="Restablecer Contraseña"
              icon-right="check_circle"
              class="full-width btn-gradient text-weight-bold"
              :loading="loading"
              no-caps
            />
          </q-form>
        </q-card-section>

        <!-- Contraseña Restablecida -->
        <q-card-section v-else class="text-center">
          <div class="success-icon-wrapper q-mb-md">
            <q-icon name="check_circle" size="64px" color="white" />
          </div>
          <div class="text-h4 text-weight-bold text-white q-mb-sm">
            ¡Contraseña Restablecida!
          </div>
          <div class="text-body1 text-white-7 q-mb-lg">
            Tu contraseña ha sido restablecida exitosamente. Ahora puedes iniciar sesión con tu nueva contraseña.
          </div>

          <q-btn
            unelevated
            size="lg"
            color="yellow-9"
            text-color="purple-10"
            label="Ir al Login"
            icon="login"
            to="/auth/login"
            class="full-width btn-gradient"
            no-caps
          />
        </q-card-section>
      </q-card>

      <!-- Link para volver -->
      <div class="text-center q-mt-md">
        <q-btn
          flat
          no-caps
          color="white"
          label="Volver al Inicio"
          to="/"
          icon="arrow_back"
        />
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import AuthService from 'src/services/auth'

export default defineComponent({
  name: 'RestablecerPasswordPage',

  setup() {
    const $q = useQuasar()
    const route = useRoute()
    const router = useRouter()

    const form = ref({
      new_password: '',
      confirm_password: ''
    })

    const showPassword = ref(false)
    const showConfirmPassword = ref(false)
    const loading = ref(false)
    const passwordReset = ref(false)
    const token = ref('')

    const passwordRules = computed(() => [
      val => !!val || 'La contraseña es requerida',
      val => val.length >= 8 || 'Mínimo 8 caracteres',
      val => /[A-Z]/.test(val) || 'Debe contener al menos una mayúscula',
      val => /[a-z]/.test(val) || 'Debe contener al menos una minúscula',
      val => /[0-9]/.test(val) || 'Debe contener al menos un número',
      val => /[!@#$%^&*(),.?":{}|<>]/.test(val) || 'Debe contener al menos un símbolo'
    ])

    const resetPassword = async () => {
      if (!token.value) {
        $q.notify({
          message: 'Token inválido o expirado',
          color: 'negative',
          icon: 'error',
          position: 'top'
        })
        return
      }

      loading.value = true

      try {
        const result = await AuthService.resetPassword(token.value, form.value.new_password)

        if (result.success) {
          passwordReset.value = true
          $q.notify({
            message: '¡Contraseña restablecida exitosamente!',
            color: 'positive',
            icon: 'check_circle',
            position: 'top'
          })
        } else {
          $q.notify({
            message: result.message || 'Error al restablecer la contraseña',
            color: 'negative',
            icon: 'error',
            position: 'top'
          })
        }
      } catch (error) {
        console.error('Reset password error:', error)
        $q.notify({
          message: 'Error de conexión. Por favor intenta nuevamente.',
          color: 'negative',
          icon: 'error',
          position: 'top'
        })
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      token.value = route.params.token

      if (!token.value) {
        $q.notify({
          message: 'Token de restablecimiento inválido',
          color: 'negative',
          icon: 'error',
          position: 'top'
        })
        router.push('/auth/login')
      }
    })

    return {
      form,
      showPassword,
      showConfirmPassword,
      loading,
      passwordReset,
      passwordRules,
      resetPassword
    }
  }
})
</script>

<style scoped>
.reset-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 64px);
  height: 100%;
  padding: 20px;
  background: transparent;
}

.reset-container {
  width: 100%;
  max-width: 520px;
  position: relative;
  z-index: 10;
  margin: auto;
}

/* Formas decorativas */
.shape-decoration {
  position: fixed;
  border-radius: 50%;
  opacity: 0.12;
  z-index: 1;
}

.shape-1 {
  width: 350px;
  height: 350px;
  background: #FDB813;
  top: -80px;
  right: -80px;
}

.shape-2 {
  width: 250px;
  height: 250px;
  background: #EC4899;
  bottom: 100px;
  left: -60px;
}

.shape-3 {
  width: 200px;
  height: 200px;
  background: #10B981;
  top: 50%;
  right: -50px;
}

/* Tarjeta con efecto glass */
.glass-card {
  background: rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 24px !important;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
  padding: 30px;
}

.reset-icon-wrapper,
.success-icon-wrapper {
  width: 85px;
  height: 85px;
  margin: 0 auto;
  background: linear-gradient(135deg, rgba(253, 184, 19, 0.3), rgba(251, 146, 60, 0.3));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 3px solid rgba(253, 184, 19, 0.5);
  box-shadow: 0 8px 24px rgba(253, 184, 19, 0.2);
}

.success-icon-wrapper {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.3), rgba(34, 197, 94, 0.3));
  border-color: rgba(16, 185, 129, 0.5);
  box-shadow: 0 8px 24px rgba(16, 185, 129, 0.2);
}

.text-white-7 {
  color: rgba(255, 255, 255, 0.7);
}

/* Inputs modernos */
.modern-input :deep(.q-field__control) {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
}

.modern-input :deep(.q-field__control):before {
  border-color: rgba(124, 58, 237, 0.3);
}

.modern-input :deep(.q-field__control):hover:before {
  border-color: rgba(253, 184, 19, 0.8);
}

.modern-input :deep(.q-field__native) {
  color: #4C1D95;
  font-weight: 500;
}

.modern-input :deep(.q-field__label) {
  color: #7C3AED;
  font-weight: 500;
}

/* Botón con gradiente */
.btn-gradient {
  background: linear-gradient(135deg, #FDB813 0%, #F59E0B 100%);
  border-radius: 12px;
  font-size: 16px;
  padding: 14px 0;
  box-shadow: 0 4px 15px rgba(253, 184, 19, 0.4);
  transition: all 0.3s ease;
}

.btn-gradient:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(253, 184, 19, 0.6);
}

/* Responsive */
@media (max-width: 768px) {
  .reset-page {
    min-height: calc(100vh - 60px);
    padding: 16px;
  }
  
  .glass-card {
    padding: 24px;
  }
  
  .text-h4 {
    font-size: 1.8rem;
  }
  
  .text-h6 {
    font-size: 1.1rem;
  }
}

@media (max-width: 600px) {
  .reset-page {
    padding: 15px;
  }

  .glass-card {
    padding: 20px;
  }

  .shape-1,
  .shape-2,
  .shape-3 {
    width: 200px;
    height: 200px;
  }

  .reset-icon-wrapper,
  .success-icon-wrapper {
    width: 70px;
    height: 70px;
  }

  .reset-icon-wrapper .q-icon,
  .success-icon-wrapper .q-icon {
    font-size: 42px !important;
  }

  .text-h4 {
    font-size: 1.5rem;
  }
}

@media (max-width: 400px) {
  .reset-page {
    padding: 12px;
  }
  
  .glass-card {
    padding: 16px;
  }
  
  .shape-1,
  .shape-2,
  .shape-3 {
    width: 150px;
    height: 150px;
  }
  
  .text-h4 {
    font-size: 1.3rem;
  }
}

@media (max-height: 700px) {
  .reset-page {
    padding: 10px;
  }
  
  .reset-icon-wrapper,
  .success-icon-wrapper {
    width: 60px;
    height: 60px;
    margin-bottom: 8px !important;
  }
  
  .reset-icon-wrapper .q-icon,
  .success-icon-wrapper .q-icon {
    font-size: 36px !important;
  }
  
  .text-h4 {
    font-size: 1.4rem;
    margin-bottom: 4px !important;
  }
  
  .text-h6 {
    font-size: 1rem;
    margin-bottom: 4px !important;
  }
  
  .text-body1 {
    font-size: 0.875rem;
    margin-bottom: 8px !important;
  }
  
  .glass-card {
    padding: 16px;
  }
}
</style>
