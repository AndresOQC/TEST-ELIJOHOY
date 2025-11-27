<template>
  <q-page class="register-page">
    <div class="register-container">
      <q-card class="register-card glass-card">
        <!-- Header -->
        <q-card-section class="text-center q-pb-md">
          <div class="register-icon-wrapper q-mb-lg">
            <q-icon name="how_to_reg" size="44px" color="white" />
          </div>
          <div class="text-h4 text-weight-bold text-white q-mb-sm">
            ¡Únete a nosotros!
          </div>
          <div class="text-body2 text-white-7">
            Completa tu registro en 3 simples pasos
          </div>
        </q-card-section>

        <!-- Tabs Navigation (horizontal in one row) -->
        <q-card-section class="q-pt-none q-px-md">
          <q-tabs
            v-model="step"
            dense
            class="modern-tabs"
            active-color="yellow-9"
            indicator-color="yellow-9"
            align="justify"
          >
            <q-tab :name="1" icon="person" label="Datos" class="tab-step" />
            <q-tab :name="2" icon="school" label="Institución" :disable="step < 2" class="tab-step" />
            <q-tab :name="3" icon="lock" label="Credenciales" :disable="step < 3" class="tab-step" />
          </q-tabs>
        </q-card-section>

        <!-- Content -->
        <q-card-section class="q-pt-sm q-px-md">
          <q-tab-panels
            v-model="step"
            animated
            transition-prev="slide-right"
            transition-next="slide-left"
            class="transparent-panels"
          >
            <!-- Panel 1: Información Personal y Ubicación -->
            <q-tab-panel :name="1" class="q-pa-none">
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
                    <q-select
                      v-model="form.pais"
                      :options="filteredCountries"
                      option-label="name"
                      option-value="name"
                      label="País"
                      outlined
                      dense
                      use-input
                      input-debounce="300"
                      @filter="filterCountries"
                      @update:model-value="onCountryChange"
                      color="purple-7"
                      :rules="[val => !!val || 'Requerido']"
                      lazy-rules
                      class="modern-input"
                      :loading="loadingCountries"
                    >
                      <template v-slot:prepend>
                        <q-icon name="public" color="purple-7" />
                      </template>
                      <template v-slot:no-option>
                        <q-item>
                          <q-item-section class="text-grey">
                            No se encontraron países
                          </q-item-section>
                        </q-item>
                      </template>
                    </q-select>
                  </div>

                  <div class="col-12 col-sm-6">
                    <q-select
                      v-model="form.ciudad"
                      :options="filteredCities"
                      label="Ciudad"
                      outlined
                      dense
                      use-input
                      input-debounce="300"
                      @filter="filterCities"
                      color="purple-7"
                      :rules="[val => !!val || 'Requerido']"
                      lazy-rules
                      class="modern-input"
                      :loading="loadingCities"
                      :disable="!form.pais"
                    >
                      <template v-slot:prepend>
                        <q-icon name="location_city" color="purple-7" />
                      </template>
                      <template v-slot:no-option>
                        <q-item>
                          <q-item-section class="text-grey">
                            {{ form.pais ? 'No se encontraron ciudades' : 'Selecciona un país primero' }}
                          </q-item-section>
                        </q-item>
                      </template>
                    </q-select>
                  </div>
                </div>

                <div class="row q-mt-md">
                  <div class="col-12">
                    <q-btn
                      unelevated
                      @click="step = 2"
                      color="yellow-9"
                      text-color="purple-10"
                      label="Siguiente"
                      icon-right="arrow_forward"
                      class="btn-gradient full-width"
                      no-caps
                    />
                  </div>
                </div>
              </div>
            </q-tab-panel>

            <!-- Panel 2: Información Educativa -->
            <q-tab-panel :name="2" class="q-pa-none">
              <div class="q-gutter-md">
                <div class="text-center q-mb-md">
                  <div class="text-caption text-white-7">
                    Esta información es opcional y nos ayuda a personalizar tu experiencia
                  </div>
                </div>

                <q-input
                  v-model="form.institucion_educativa"
                  label="Institución Educativa (Opcional)"
                  outlined
                  color="purple-7"
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
                      label="Grado (Opcional)"
                      outlined
                      color="purple-7"
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
                      label="Sección (Opcional)"
                      outlined
                      color="purple-7"
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
                      label="Turno (Opcional)"
                      outlined
                      color="purple-7"
                      class="modern-input"
                    >
                      <template v-slot:prepend>
                        <q-icon name="schedule" color="purple-7" />
                      </template>
                    </q-select>
                  </div>
                </div>

                <div class="row q-col-gutter-sm q-mt-md">
                  <div class="col-4">
                    <q-btn
                      flat
                      color="yellow-9"
                      @click="step = 1"
                      label="Anterior"
                      icon="arrow_back"
                      class="full-width"
                      no-caps
                    />
                  </div>
                  <div class="col-4">
                    <q-btn
                      flat
                      color="white"
                      @click="step = 3"
                      label="Omitir"
                      class="full-width"
                      no-caps
                    />
                  </div>
                  <div class="col-4">
                    <q-btn
                      unelevated
                      @click="step = 3"
                      color="yellow-9"
                      text-color="purple-10"
                      label="Siguiente"
                      icon-right="arrow_forward"
                      class="btn-gradient full-width"
                      no-caps
                    />
                  </div>
                </div>
              </div>
            </q-tab-panel>

            <!-- Panel 3: Credenciales -->
            <q-tab-panel :name="3" class="q-pa-none">
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

                <div class="row q-col-gutter-sm q-mt-md">
                  <div class="col-6">
                    <q-btn
                      flat
                      color="yellow-9"
                      @click="step = 2"
                      label="Anterior"
                      icon="arrow_back"
                      class="full-width"
                      no-caps
                    />
                  </div>
                  <div class="col-6">
                    <q-btn
                      unelevated
                      @click="register"
                      color="yellow-9"
                      text-color="purple-10"
                      label="Crear Cuenta"
                      icon-right="check_circle"
                      class="btn-gradient full-width"
                      :loading="loading"
                      :disable="!acceptTerms"
                      no-caps
                    />
                  </div>
                </div>
              </div>
            </q-tab-panel>
          </q-tab-panels>
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
import { defineComponent, ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Notify } from 'quasar'
import { useAuthStore } from 'src/stores/auth'
import { useTestStore } from 'src/stores/test'

export default defineComponent({
  name: 'RegistroPage',

  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const testStore = useTestStore()

    const step = ref(1)

    const form = ref({
      nombre: '',
      apellidos: '',
      edad: null,
      genero: null,
      email: '',
      password: '',
      confirm_password: '',
      ciudad: '',
      pais: null,
      institucion_educativa: '',
      grado: '',
      seccion: '',
      turno: null
    })

    const showPassword = ref(false)
    const showConfirmPassword = ref(false)
    const acceptTerms = ref(false)
    const loading = ref(false)

    // Country and City data
    const countries = ref([])
    const cities = ref([])
    const filteredCountries = ref([])
    const filteredCities = ref([])
    const loadingCountries = ref(false)
    const loadingCities = ref(false)

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

    // Fetch countries from REST Countries API
    const fetchCountries = async () => {
      loadingCountries.value = true
      try {
        const response = await fetch('https://restcountries.com/v3.1/all?fields=name,cca2')
        const data = await response.json()
        countries.value = data
          .map(country => ({
            name: country.name.common,
            code: country.cca2
          }))
          .sort((a, b) => a.name.localeCompare(b.name))
        filteredCountries.value = countries.value
        console.log(`Loaded ${countries.value.length} countries from REST Countries API`)
      } catch (error) {
        console.error('Error fetching countries:', error)
        countries.value = [
          { name: 'Perú', code: 'PE' },
          { name: 'Argentina', code: 'AR' },
          { name: 'Chile', code: 'CL' },
          { name: 'Colombia', code: 'CO' },
          { name: 'México', code: 'MX' },
          { name: 'España', code: 'ES' }
        ]
        filteredCountries.value = countries.value
      } finally {
        loadingCountries.value = false
      }
    }

    // Helper function to convert country code to name for API
    const getCountryNameByCode = (code) => {
      // Mapeo de países comunes que pueden tener nombres diferentes en la API
      const countryMapping = {
        'PE': 'Peru',
        'US': 'United States',
        'MX': 'Mexico',
        'AR': 'Argentina',
        'CL': 'Chile',
        'CO': 'Colombia',
        'EC': 'Ecuador',
        'BR': 'Brazil',
        'ES': 'Spain',
        'GB': 'United Kingdom'
      }
      
      // Si existe mapeo directo, usarlo
      if (countryMapping[code]) {
        return countryMapping[code]
      }
      
      // Sino, buscar por código
      const country = countries.value.find(c => c.code === code)
      return country ? country.name : code
    }

    // Fetch cities from countriesnow API directly by country (principales ciudades)
    const fetchCitiesByCountry = async (countryCode) => {
      if (!countryCode) return
      
      loadingCities.value = true
      const countryName = getCountryNameByCode(countryCode)
      console.log(`Buscando ciudades para: ${countryName} (código: ${countryCode})`)
      
      try {
        // Using countriesnow API to get all cities of a country
        const response = await fetch(
          'https://countriesnow.space/api/v0.1/countries/cities',
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              country: countryName
            })
          }
        )
        
        if (response.ok) {
          const data = await response.json()
          console.log('Cities API response:', data)
          
          if (data.data && data.data.length > 0) {
            // Get cities and sort alphabetically
            const cityNames = [...new Set(data.data)]
              .sort((a, b) => a.localeCompare(b))
            cities.value = cityNames
            filteredCities.value = cityNames
            console.log(`Loaded ${cityNames.length} cities for country: ${countryCode}`)
          } else {
            cities.value = []
            filteredCities.value = []
            console.warn(`No cities found for country: ${countryCode}`)
          }
        } else {
          console.error('Cities API error:', response.status)
          cities.value = []
          filteredCities.value = []
        }
      } catch (error) {
        console.error('Error fetching cities:', error)
        cities.value = []
        filteredCities.value = []
      } finally {
        loadingCities.value = false
      }
    }

    const filterCountries = (val, update) => {
      if (val === '') {
        update(() => {
          filteredCountries.value = countries.value
        })
        return
      }

      update(() => {
        const needle = val.toLowerCase()
        filteredCountries.value = countries.value.filter(
          country => country.name.toLowerCase().indexOf(needle) > -1
        )
      })
    }

    const filterCities = (val, update) => {
      if (val === '') {
        update(() => {
          filteredCities.value = cities.value
        })
        return
      }

      update(() => {
        const needle = val.toLowerCase()
        filteredCities.value = cities.value.filter(
          city => city.toLowerCase().indexOf(needle) > -1
        )
      })
    }

    const onCountryChange = (val) => {
      if (val) {
        // Reset city field
        form.value.ciudad = ''
        
        // Fetch cities for the selected country
        if (val.code) {
          console.log(`Country changed to: ${val.name} (${val.code})`)
          fetchCitiesByCountry(val.code)
        }
      }
    }

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
        const payload = {
          ...form.value,
          pais: form.value.pais?.name || form.value.pais,
          // Limpiar campos opcionales vacíos
          institucion_educativa: form.value.institucion_educativa || null,
          grado: form.value.grado || null,
          seccion: form.value.seccion || null,
          turno: form.value.turno || null
        }
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
          const pendingFinalization = localStorage.getItem('pendingTestFinalization')

          // Si hay test pendiente de finalización, procesarlo aquí
          if ((pendingFinalization === 'true' || respuestasGuardadas) && respuestasGuardadas) {
            console.log('Finalizando test pendiente después del registro...')
            localStorage.removeItem('pendingTestFinalization')

            try {
              const respuestasParseadas = JSON.parse(respuestasGuardadas)
              const cantidadRespuestas = Object.keys(respuestasParseadas).length

              if (cantidadRespuestas >= 32) {
                Notify.create({
                  message: 'Procesando tu test...',
                  color: 'info',
                  icon: 'hourglass_empty',
                  position: 'top'
                })

                // 1. Crear sesión de test
                const sesionResponse = await testStore.iniciarTest()
                if (!sesionResponse.success) {
                  throw new Error('Error al crear sesión de test')
                }

                // 2. Sincronizar respuestas
                const sincResponse = await testStore.sincronizarRespuestas(respuestasParseadas)
                if (!sincResponse.success) {
                  throw new Error('Error al sincronizar respuestas')
                }

                // 3. Finalizar test
                const finResponse = await testStore.finalizarTest()
                if (finResponse.success) {
                  // Limpiar localStorage
                  localStorage.removeItem('testRespuestas')

                  Notify.create({
                    message: '¡Test completado! Mostrando tus resultados...',
                    color: 'positive',
                    icon: 'check_circle',
                    position: 'top'
                  })

                  // Redirigir a resultados
                  router.push(`/dashboard/test-resultados/${testStore.getSesion.id_sesion}`)
                  return
                }
              }
            } catch (testError) {
              console.error('Error al finalizar test:', testError)
              Notify.create({
                message: 'Error al procesar el test. Ve a Test Resultados.',
                color: 'warning',
                icon: 'warning',
                position: 'top'
              })
            }
          }

          // Si no hay test pendiente o falló, ir al dashboard
          router.push('/dashboard')
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

    // Fetch countries on component mount
    onMounted(() => {
      fetchCountries()
    })

    return {
      step,
      form,
      showPassword,
      showConfirmPassword,
      acceptTerms,
      loading,
      generoOptions,
      turnoOptions,
      passwordRules,
      filteredCountries,
      filteredCities,
      loadingCountries,
      loadingCities,
      filterCountries,
      filterCities,
      onCountryChange,
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

/* Modern Tabs (horizontal navigation) */
.modern-tabs {
  background: rgba(255, 255, 255, 0.05);
  border-radius: clamp(0.75rem, 2vw, 1rem);
  padding: clamp(0.25rem, 0.5vw, 0.375rem);
  margin-bottom: clamp(0.75rem, 1.5vw, 1rem);
}

.modern-tabs :deep(.q-tab) {
  color: rgba(255, 255, 255, 0.6);
  font-weight: 600;
  font-size: clamp(0.7rem, 1.3vw, 0.8rem);
  min-height: clamp(2.5rem, 4vw, 3rem);
  transition: all 0.3s ease;
  flex: 1;
}

.modern-tabs :deep(.q-tab--active) {
  color: #FDB813;
  background: rgba(253, 184, 19, 0.15);
  border-radius: clamp(0.5rem, 1.5vw, 0.75rem);
}

.modern-tabs :deep(.q-tab--disabled) {
  opacity: 0.4;
}

.modern-tabs :deep(.q-tab__icon) {
  font-size: clamp(1rem, 1.8vw, 1.125rem);
}

.modern-tabs :deep(.q-tab__label) {
  font-size: clamp(0.65rem, 1.1vw, 0.75rem);
  margin-top: 0.25rem;
}

/* Transparent panels */
.transparent-panels {
  background: transparent;
}

.transparent-panels :deep(.q-tab-panel) {
  padding: 0;
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
