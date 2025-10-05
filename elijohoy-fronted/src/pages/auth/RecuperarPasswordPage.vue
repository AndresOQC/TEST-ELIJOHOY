<template>
  <q-page class="recover-page">
    <div class="recover-container">
      <q-card class="recover-card glass-card">
        <q-card-section v-if="!emailSent" class="text-center">
          <div class="recover-icon-wrapper q-mb-lg">
            <q-icon name="help" size="52px" color="white" />
          </div>
          <div class="text-h4 text-weight-bold text-white q-mb-sm">
            ¿Olvidaste tu contraseña?
          </div>
          <div class="text-h6 text-weight-medium text-yellow-9 q-mb-sm">
            No te preocupes
          </div>
          <div class="text-body1 text-white-7 q-mb-lg">
            Ingresa tu correo electrónico y te enviaremos las instrucciones para crear una nueva contraseña
          </div>

          <q-form @submit="recoverPassword" class="q-gutter-md">
            <q-input
              v-model="email"
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

            <q-btn
              unelevated
              type="submit"
              size="lg"
              color="yellow-9"
              text-color="purple-10"
              label="Enviar Instrucciones"
              icon-right="send"
              class="full-width btn-gradient text-weight-bold"
              :loading="loading"
              no-caps
            />
          </q-form>
        </q-card-section>

        <!-- Email Enviado con éxito -->
        <q-card-section v-else class="text-center">
          <div class="success-icon-wrapper q-mb-md">
            <q-icon name="mark_email_read" size="64px" color="white" />
          </div>
          <div class="text-h4 text-weight-bold text-white q-mb-sm">
            ¡Correo Enviado!
          </div>
          <div class="text-body1 text-white-7 q-mb-md">
            Hemos enviado las instrucciones para restablecer tu contraseña a
          </div>
          <div class="text-h6 text-yellow-9 text-weight-bold q-mb-lg">
            {{ email }}
          </div>
          <div class="text-body2 text-white-7 q-pa-md bg-white-5 rounded-borders">
            <q-icon name="info" size="20px" class="q-mr-xs" />
            Si no recibes el correo en unos minutos, revisa tu carpeta de spam o intenta nuevamente.
          </div>

          <q-btn
            unelevated
            color="yellow-9"
            text-color="purple-10"
            label="Enviar Nuevamente"
            icon="refresh"
            class="full-width q-mt-md btn-gradient"
            @click="emailSent = false"
            no-caps
          />
        </q-card-section>

        <q-card-section class="text-center q-pt-md">
          <div class="text-body2 text-white">
            ¿Recordaste tu contraseña?
            <q-btn
              flat
              no-caps
              color="yellow-9"
              label="Volver al login"
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
import { defineComponent, ref } from 'vue'
import { useQuasar } from 'quasar'
import AuthService from 'src/services/auth'

export default defineComponent({
  name: 'RecuperarPasswordPage',

  setup() {
    const $q = useQuasar()

    const email = ref('')
    const loading = ref(false)
    const emailSent = ref(false)

    const recoverPassword = async () => {
      loading.value = true

      try {
        const result = await AuthService.sendPasswordReset(email.value)

        if (result.success) {
          emailSent.value = true
          $q.notify({
            message: 'Instrucciones enviadas exitosamente',
            color: 'positive',
            icon: 'check_circle',
            position: 'top'
          })
        } else {
          $q.notify({
            message: result.message || 'Error al enviar las instrucciones',
            color: 'negative',
            icon: 'error',
            position: 'top'
          })
        }
      } catch (error) {
        console.error('Recover password error:', error)
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

    return {
      email,
      loading,
      emailSent,
      recoverPassword
    }
  }
})
</script>

<style scoped>
.recover-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100%;
  padding: 20px;
  background: transparent;
}

.recover-container {
  width: 100%;
  max-width: 520px;
  position: relative;
  z-index: 10;
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

.recover-icon-wrapper,
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
  background: rgba(16, 185, 129, 0.2);
  border-color: rgba(16, 185, 129, 0.4);
}

.text-white-7 {
  color: rgba(255, 255, 255, 0.7);
}

.bg-white-5 {
  background: rgba(255, 255, 255, 0.05);
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
@media (max-width: 600px) {
  .recover-page {
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

  .recover-icon-wrapper,
  .success-icon-wrapper {
    width: 80px;
    height: 80px;
  }

  .recover-icon-wrapper .q-icon,
  .success-icon-wrapper .q-icon {
    font-size: 48px !important;
  }

  .text-h4 {
    font-size: 1.5rem;
  }
}

@media (max-width: 400px) {
  .shape-1,
  .shape-2,
  .shape-3 {
    width: 150px;
    height: 150px;
  }
}
</style>
