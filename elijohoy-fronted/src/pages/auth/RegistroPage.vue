<template>
  <q-page class="register-page">
    <div class="register-container">
      <q-card class="register-card glass-card">
        <!-- Header -->
        <q-card-section class="text-center q-pb-md">
          <div class="register-icon-wrapper q-mb-lg">
            <q-icon name="how_to_reg" size="44px" color="white" />
          </div>
          <div class="text-h3 text-weighimport { defineComponent, ref } from 'vue'
import { useRouter } from 'vue-router'
import { Notify } from 'quasar'
import { useAuthStore } from 'src/stores/auth'
import { useTestStore } from 'src/stores/test' text-white q-mb-sm">
            ¡Únete a nosotros!
          </div>
          <div class="text-body1 text-white-7">
            Completa tu registro y comienza a descubrir tu vocación ideal
          </div>
        </q-card-section>

        <!-- Stepper -->
        <q-card-section class="q-pt-none">
          <q-stepper
            v-model="step"
            ref="stepper"
            color="yellow-9"
            animated
            header-nav
            dark
            flat
            class="transparent-stepper"
          >
            <!-- Paso 1: Información Personal y Ubicación -->
            <q-step
              :name="1"
              title="Datos Personales"
              icon="person"
              :done="step > 1"
              active-icon="person"
              done-icon="check"
            >
              <div class="q-gutter-md">
                <div class="row q-col-gutter-sm">
                  <div class="col-12 col-sm-6">
                    <q-input
                      v-model="form.nombre"
                      label="Nombre"
                      outlined
                      color="purple-7"
                      :rules="[val => !!val || 'Requerido', val => val.length >= 2 || 'Mínimo 2 caracteres']"
                      lazy-rules
                      class="modern-input"
                    >
                      <template v-slot:prepend>
                        <q-icon name="badge" color="purple-7" />
                      </template>
                    </q-input>
                  </div>

                  <div class="col-12 col-sm-6">
                    <q-input
                      v-model="form.apellidos"
                      label="Apellidos"
                      outlined
                      color="purple-7"
                      :rules="[val => !!val || 'Requerido', val => val.length >= 2 || 'Mínimo 2 caracteres']"
                      lazy-rules
                      class="modern-input"
                    >
                      <template v-slot:prepend>
                        <q-icon name="badge" color="purple-7" />
                      </template>
                    </q-input>
                  </div>
                </div>

                <div class="row q-col-gutter-sm">
                  <div class="col-12 col-sm-6">
                    <q-input
                      v-model.number="form.edad"
                      type="number"
                      label="Edad"
                      outlined
                      color="purple-7"
                      :rules="[val => !!val || 'Requerido', val => val >= 10 && val <= 100 || 'Edad inválida']"
                      lazy-rules
                      class="modern-input"
                    >
                      <template v-slot:prepend>
                        <q-icon name="cake" color="purple-7" />
                      </template>
                    </q-input>
                  </div>

                  <div class="col-12 col-sm-6">
                    <q-select
                      v-model="form.genero"
                      :options="generoOptions"
                      label="Género"
                      outlined
                      color="purple-7"
                      :rules="[val => !!val || 'Requerido']"
                      lazy-rules
                      class="modern-input"
                      dropdown-icon="expand_more"
                    >
                      <template v-slot:prepend>
                        <q-icon name="wc" color="purple-7" />
                      </template>
                    </q-select>
                  </div>
                </div>

                <div class="row q-col-gutter-sm">
                  <div class="col-12 col-sm-6">
                    <q-input
                      v-model="form.ciudad"
                      label="Ciudad"
                      outlined
                      color="purple-7"
                      :rules="[val => !!val || 'Requerido']"
                      lazy-rules
                      class="modern-input"
                    >
                      <template v-slot:prepend>
                        <q-icon name="location_city" color="purple-7" />
                      </template>
                    </q-input>
                  </div>

                  <div class="col-12 col-sm-6">
                    <q-input
                      v-model="form.pais"
                      label="País"
                      outlined
                      color="purple-7"
                      :rules="[val => !!val || 'Requerido']"
                      lazy-rules
                      class="modern-input"
                    >
                      <template v-slot:prepend>
                        <q-icon name="public" color="purple-7" />
                      </template>
                    </q-input>
                  </div>
                </div>
              </div>
            </q-step>

            <!-- Paso 2: Información Educativa -->
            <q-step
              :name="2"
              title="Institución"
              icon="school"
              :done="step > 2"
              active-icon="school"
              done-icon="check"
            >
              <div class="q-gutter-md">
                <q-input
                  v-model="form.institucion_educativa"
                  label="Institución Educativa"
                  outlined
                  color="purple-7"
                  :rules="[val => !!val || 'Requerido']"
                  lazy-rules
                  class="modern-input"
                >
                  <template v-slot:prepend>
                    <q-icon name="school" color="purple-7" />
                  </template>
                </q-input>

                <div class="row q-col-gutter-sm">
                  <div class="col-12 col-sm-4">
                    <q-input
                      v-model="form.grado"
                      label="Grado"
                      outlined
                      color="purple-7"
                      :rules="[val => !!val || 'Requerido']"
                      lazy-rules
                      class="modern-input"
                      placeholder="Ej: 5to"
                    >
                      <template v-slot:prepend>
                        <q-icon name="grade" color="purple-7" />
                      </template>
                    </q-input>
                  </div>

                  <div class="col-12 col-sm-4">
                    <q-input
                      v-model="form.seccion"
                      label="Sección"
                      outlined
                      color="purple-7"
                      :rules="[val => !!val || 'Requerido']"
                      lazy-rules
                      class="modern-input"
                      placeholder="Ej: A"
                    >
                      <template v-slot:prepend>
                        <q-icon name="class" color="purple-7" />
                      </template>
                    </q-input>
                  </div>

                  <div class="col-12 col-sm-4">
                    <q-select
                      v-model="form.turno"
                      :options="turnoOptions"
                      label="Turno"
                      outlined
                      color="purple-7"
                      :rules="[val => !!val || 'Requerido']"
                      lazy-rules
                      class="modern-input"
                    >
                      <template v-slot:prepend>
                        <q-icon name="schedule" color="purple-7" />
                      </template>
                    </q-select>
                  </div>
                </div>
              </div>
            </q-step>

            <!-- Paso 3: Credenciales -->
            <q-step
              :name="3"
              title="Credenciales"
              icon="lock"
              active-icon="lock"
              done-icon="check"
            >
              <div class="q-gutter-md">
                <q-input
                  v-model="form.email"
                  type="email"
                  label="Correo Electrónico"
                  outlined
                  color="purple-7"
                  :rules="[
                    val => !!val || 'Requerido',
                    val => /.+@.+\..+/.test(val) || 'Correo inválido'
                  ]"
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
                  label="Confirmar Contraseña"
                  outlined
                  color="purple-7"
                  :rules="[
                    val => !!val || 'Requerido',
                    val => val === form.password || 'Las contraseñas no coinciden'
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

                <q-checkbox
                  v-model="acceptTerms"
                  color="purple-7"
                  class="text-white"
                >
                  <template v-slot:default>
                    <div class="text-white">
                      Acepto los
                      <a href="#" class="text-yellow-9 text-weight-bold" @click.prevent>términos y condiciones</a>
                    </div>
                  </template>
                </q-checkbox>
              </div>
            </q-step>

            <template v-slot:navigation>
              <q-stepper-navigation class="row q-gutter-sm">
                <q-btn
                  v-if="step > 1"
                  flat
                  color="yellow-9"
                  @click="$refs.stepper.previous()"
                  label="Anterior"
                  icon="arrow_back"
                  class="col"
                />
                <q-space v-if="step > 1" />
                <q-btn
                  v-if="step < 3"
                  unelevated
                  @click="$refs.stepper.next()"
                  color="yellow-9"
                  text-color="purple-10"
                  label="Siguiente"
                  icon-right="arrow_forward"
                  class="btn-gradient col"
                />
                <q-btn
                  v-if="step === 3"
                  unelevated
                  @click="register"
                  color="yellow-9"
                  text-color="purple-10"
                  label="Crear Cuenta"
                  icon-right="check_circle"
                  class="btn-gradient col"
                  :loading="loading"
                  :disable="!acceptTerms"
                />
              </q-stepper-navigation>
            </template>
          </q-stepper>
        </q-card-section>

        <!-- Footer -->
        <q-card-section class="text-center q-pt-none">
          <div class="text-body2 text-white">
            ¿Ya tienes cuenta?
            <q-btn
              flat
              no-caps
              color="yellow-9"
              label="Inicia sesión aquí"
              to="/auth/login"
              dense
              class="text-weight-bold"
            />
          </div>
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
import { defineComponent, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Notify } from 'quasar'
import { useAuthStore } from 'src/stores/auth'

export default defineComponent({
  name: 'RegistroPage',

  setup() {
    const router = useRouter()
    const authStore = useAuthStore()

    const step = ref(1)
    const stepper = ref(null)

    const form = ref({
      nombre: '',
      apellidos: '',
      edad: null,
      genero: null,
      email: '',
      password: '',
      confirm_password: '',
      ciudad: '',
      pais: '',
      institucion_educativa: '',
      grado: '',
      seccion: '',
      turno: null
    })

    const showPassword = ref(false)
    const showConfirmPassword = ref(false)
    const acceptTerms = ref(false)
    const loading = ref(false)

    const generoOptions = ['Masculino', 'Femenino', 'Otro', 'Prefiero no decir']
    const turnoOptions = ['Mañana', 'Tarde', 'Noche']

    const passwordRules = computed(() => [
      val => !!val || 'La contraseña es requerida',
      val => val.length >= 8 || 'Mínimo 8 caracteres',
      val => /[A-Z]/.test(val) || 'Debe contener al menos una mayúscula',
      val => /[a-z]/.test(val) || 'Debe contener al menos una minúscula',
      val => /[0-9]/.test(val) || 'Debe contener al menos un número',
      val => /[!@#$%^&*(),.?":{}|<>]/.test(val) || 'Debe contener al menos un símbolo'
    ])

    const register = async () => {
      if (!acceptTerms.value) {
        Notify.create({
          message: 'Debes aceptar los términos y condiciones',
          color: 'warning',
          icon: 'warning',
          position: 'top'
        })
        return
      }

      loading.value = true

      try {
        const payload = { ...form.value }
        delete payload.confirm_password

        const result = await authStore.register(payload)

        if (result.success) {
          Notify.create({
            message: '¡Registro exitoso! Bienvenido a ElijoHoy',
            color: 'positive',
            icon: 'check_circle',
            position: 'top'
          })

          // Verificar si hay respuestas de test en localStorage
          const respuestasGuardadas = localStorage.getItem('testRespuestas')

          // Verificar si hay una finalización de test pendiente
          const pendingFinalization = localStorage.getItem('pendingTestFinalization')

          if (pendingFinalization === 'true') {
            console.log('Finalización de test pendiente, redirigiendo al test...')
            // Mantener el indicador para que el test se finalice automáticamente
            router.push('/dashboard/test')
          } else if (respuestasGuardadas) {
            console.log('Detectadas respuestas de test, se sincronizarán en la página del test...')
            
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
            message: result.message || 'Error al registrar usuario',
            color: 'negative',
            icon: 'error',
            position: 'top'
          })
        }
      } catch (error) {
        console.error('Register error:', error)
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
      step,
      stepper,
      form,
      showPassword,
      showConfirmPassword,
      acceptTerms,
      loading,
      generoOptions,
      turnoOptions,
      passwordRules,
      register
    }
  }
})
</script>

<style scoped>
.register-page {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  min-height: 100vh;
  height: 100%;
  padding: clamp(0.4rem, 1vw, 0.6rem);
  background: transparent;
  overflow-y: auto;
}

.register-container {
  width: 100%;
  max-width: clamp(18rem, 95vw, 35rem);
  position: relative;
  z-index: 10;
  margin: clamp(0.4rem, 1vw, 0.6rem) auto;
}

/* Tarjeta con efecto glass */
.glass-card {
  background: rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(1.25rem);
  -webkit-backdrop-filter: blur(1.25rem);
  border-radius: clamp(0.75rem, 2.5vw, 1.25rem) !important;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 0.5rem 2rem 0 rgba(0, 0, 0, 0.37);
  padding: clamp(0.6rem, 2vw, 0.875rem);
}

.register-icon-wrapper {
  width: clamp(2.5rem, 5.5vw, 3.75rem);
  height: clamp(2.5rem, 5.5vw, 3.75rem);
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

/* Stepper transparente */
.transparent-stepper {
  background: transparent !important;
}

.transparent-stepper :deep(.q-stepper__header) {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 10px;
  margin-bottom: 20px;
}

.transparent-stepper :deep(.q-stepper__tab) {
  color: rgba(255, 255, 255, 0.7);
}

.transparent-stepper :deep(.q-stepper__tab--active) {
  color: #FDB813;
}

.transparent-stepper :deep(.q-stepper__tab--done) {
  color: #10B981;
}

.transparent-stepper :deep(.q-stepper__dot) {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
}

.transparent-stepper :deep(.q-stepper__dot--active) {
  background: #FDB813;
  border-color: #FDB813;
}

.transparent-stepper :deep(.q-stepper__dot--done) {
  background: #10B981;
  border-color: #10B981;
}

.transparent-stepper :deep(.q-stepper__line) {
  background: rgba(255, 255, 255, 0.2) !important;
}

.transparent-stepper :deep(.q-stepper__line):after {
  background: #FDB813 !important;
}

/* Inputs modernos */
.modern-input :deep(.q-field__control) {
  background: rgba(255, 255, 255, 0.95);
  border-radius: clamp(0.625rem, 2vw, 0.75rem);
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
  font-size: clamp(0.875rem, 1.5vw, 1rem);
}

.modern-input :deep(.q-field__label) {
  color: #7C3AED;
  font-weight: 500;
  font-size: clamp(0.875rem, 1.5vw, 1rem);
}

.modern-input :deep(.q-field__append .q-icon) {
  color: #7C3AED;
}

/* Botón con gradiente */
.btn-gradient {
  background: linear-gradient(135deg, #FDB813 0%, #F59E0B 100%);
  border-radius: clamp(0.625rem, 2vw, 0.75rem);
  font-size: clamp(0.875rem, 1.5vw, 0.9375rem);
  font-weight: 600;
  box-shadow: 0 0.25rem 0.9375rem rgba(253, 184, 19, 0.4);
  transition: all 0.3s ease;
}

.btn-gradient:hover {
  transform: translateY(-0.125rem);
  box-shadow: 0 0.375rem 1.25rem rgba(253, 184, 19, 0.6);
}

/* Responsive con unidades fluidas */
@media (max-width: 48rem) {
  .register-page {
    padding: clamp(0.5rem, 2vw, 1rem);
  }
}

@media (max-height: 43.75rem) {
  .register-page {
    padding: clamp(0.5rem, 1.5vw, 0.75rem);
  }
  
  .register-container {
    margin: clamp(0.5rem, 1.5vw, 0.75rem) auto;
  }
  
  .glass-card {
    padding: clamp(0.75rem, 2vw, 1rem);
  }
  
  .transparent-stepper :deep(.q-stepper__header) {
    padding: clamp(0.375rem, 1vw, 0.5rem);
    margin-bottom: clamp(0.5rem, 1.5vw, 0.75rem);
  }
}
</style>
