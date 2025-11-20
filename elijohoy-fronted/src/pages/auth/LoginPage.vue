<template>
  <q-page class="login-page">
    <div class="login-container">
      <q-card class="login-card glass-card">
        <q-card-section class="text-center q-pb-md">
          <div class="login-icon-wrapper q-mb-lg">
            <q-icon name="login" size="56px" color="white" />
          </div>
          <div class="text-h3 text-weight-bold text-white q-mb-sm">
            ¡Bienvenido de vuelta!
          </div>
          <div class="text-h6 text-weight-medium text-yellow-9 q-mb-xs">
            Iniciar Sesión
          </div>
          <div class="text-body1 text-white-7">
            Accede a tu cuenta y continúa descubriendo tu vocación
          </div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-form @submit="login" class="q-gutter-md">
            <q-input
              v-model="form.email"
              type="email"
              label="Correo Electrónico"
              outlined
              color="purple-7"
              :rules="[val => !!val || 'El correo es requerido', val => /.+@.+\..+/.test(val) || 'Correo inválido']"
              lazy-rules
              class="modern-input"
            >
              <template v-slot:prepend>
                <q-icon name="email" color="purple-7" />
              </template>
            </q-input>

            <q-input
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              label="Contraseña"
              outlined
              color="purple-7"
              :rules="[val => !!val || 'La contraseña es requerida']"
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
            </q-input>

            <div class="row justify-between items-center">
              <q-checkbox
                v-model="rememberMe"
                label="Recordarme"
                color="purple-7"
                class="text-white"
              />
              <q-btn
                flat
                no-caps
                color="yellow-9"
                label="¿Olvidaste tu contraseña?"
                to="/auth/recuperar-password"
                size="sm"
              />
            </div>

            <q-btn
              unelevated
              type="submit"
              size="lg"
              color="yellow-9"
              text-color="purple-10"
              label="Iniciar Sesión"
              icon-right="login"
              class="full-width btn-gradient text-weight-bold"
              :loading="loading"
              no-caps
            />

            <div class="text-center q-mt-md">
              <div class="text-body2 text-white q-mb-sm">
                ¿No tienes cuenta?
              </div>
              <q-btn
                outline
                no-caps
                color="yellow-9"
                label="Regístrate Gratis"
                to="/auth/registro"
                class="full-width"
                icon="person_add"
              />
            </div>
          </q-form>
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
import { defineComponent, ref } from 'vue'
import { useRouter } from 'vue-router'
import { Notify } from 'quasar'
import { useAuthStore } from 'src/stores/auth'

export default defineComponent({
  name: 'LoginPage',

  setup() {
    const router = useRouter()
    const authStore = useAuthStore()

    const form = ref({
      email: '',
      password: ''
    })

    const showPassword = ref(false)
    const rememberMe = ref(false)
    const loading = ref(false)

    const login = async () => {
      loading.value = true

      try {
        const result = await authStore.login(form.value)

        if (result.success && authStore.isAuthenticated) {
          Notify.create({
            message: '¡Bienvenido de nuevo!',
            color: 'positive',
            icon: 'check_circle',
            position: 'top'
          })

          // Verificar si hay respuestas de test en localStorage
          const respuestasGuardadas = localStorage.getItem('testRespuestas')

          // Verificar si hay una finalización de test pendiente
          const pendingFinalization = localStorage.getItem('pendingTestFinalization')

          if (pendingFinalization === 'true') {
            // Mantener el indicador para que el test se finalice automáticamente
            router.push('/dashboard/test')
          } else if (respuestasGuardadas) {
            Notify.create({
              message: 'Respuestas detectadas, continuando con el test...',
              color: 'positive',
              icon: 'save',
              position: 'top'
            })
            router.push('/dashboard/test')
          } else {
            router.push('/dashboard')
          }
        } else {
          Notify.create({
            message: result.message || 'Credenciales incorrectas',
            color: 'negative',
            icon: 'error',
            position: 'top'
          })
        }
      } catch (error) {
        console.error('Login error:', error)
        Notify.create({
          message: 'Error de conexión. Por favor intenta nuevamente.',
          color: 'negative',
          icon: 'error',
          position: 'top'
        })
      } finally {
        loading.value = false
      }
    }

    return {
      form,
      showPassword,
      rememberMe,
      loading,
      login
    }
  }
})
</script>

<style scoped>
.login-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  height: 100%;
  padding: clamp(0.4rem, 1vw, 0.6rem);
  background: transparent;
}

.login-container {
  width: 100%;
  max-width: clamp(18rem, 90vw, 30rem);
  position: relative;
  z-index: 10;
  margin: auto;
}

/* Tarjeta con efecto glass */
.glass-card {
  background: rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(1.25rem);
  -webkit-backdrop-filter: blur(1.25rem);
  border-radius: clamp(0.75rem, 2.5vw, 1.25rem) !important;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 0.5rem 2rem 0 rgba(0, 0, 0, 0.37);
  padding: clamp(0.75rem, 2.5vw, 1rem);
}

.login-icon-wrapper {
  width: clamp(2.75rem, 6vw, 4rem);
  height: clamp(2.75rem, 6vw, 4rem);
  margin: 0 auto;
  background: linear-gradient(135deg, rgba(253, 184, 19, 0.3), rgba(251, 146, 60, 0.3));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 0.1875rem solid rgba(253, 184, 19, 0.5);
  box-shadow: 0 0.5rem 1.5rem rgba(253, 184, 19, 0.2);
}

.text-white-7 {
  color: rgba(255, 255, 255, 0.7);
}

/* Inputs modernos */
.modern-input :deep(.q-field__control) {
  background: rgba(255, 255, 255, 0.95);
  border-radius: clamp(0.5rem, 1.5vw, 0.625rem);
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
  font-size: clamp(0.8rem, 1.2vw, 0.9rem);
}

.modern-input :deep(.q-field__label) {
  color: #7C3AED;
  font-weight: 500;
  font-size: clamp(0.8rem, 1.2vw, 0.9rem);
}

/* Botón con gradiente */
.btn-gradient {
  background: linear-gradient(135deg, #FDB813 0%, #F59E0B 100%);
  border-radius: clamp(0.5rem, 1.5vw, 0.625rem);
  font-size: clamp(0.8rem, 1.2vw, 0.9rem);
  padding: clamp(0.6rem, 1.5vw, 0.75rem) 0;
  box-shadow: 0 0.25rem 0.9375rem rgba(253, 184, 19, 0.4);
  transition: all 0.3s ease;
}

.btn-gradient:hover {
  transform: translateY(-0.125rem);
  box-shadow: 0 0.375rem 1.25rem rgba(253, 184, 19, 0.6);
}

/* Responsive con unidades fluidas */
@media (max-width: 48rem) {
  .login-page {
    padding: clamp(0.4rem, 1vw, 0.6rem);
  }
}

@media (max-width: 37.5rem) {
  .shape-1,
  .shape-2,
  .shape-3 {
    width: clamp(9.375rem, 25vw, 12.5rem);
    height: clamp(9.375rem, 25vw, 12.5rem);
  }
}

@media (max-height: 43.75rem) {
  .login-page {
    padding: clamp(0.35rem, 0.8vw, 0.5rem);
  }
  
  .login-icon-wrapper {
    margin-bottom: 0.4rem !important;
  }
  
  .glass-card {
    padding: clamp(0.6rem, 1.5vw, 0.8rem);
  }
}
</style>
