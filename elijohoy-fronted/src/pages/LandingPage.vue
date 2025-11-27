<!-- Eliminado script setup para evitar duplicidad de imports y lógica -->
<template>
  <q-page class="landing-page">
    <!-- Hero Section -->
    <div id="hero" class="hero-section">
      <div class="container">
        <div class="row items-center">
          <div class="col-12 col-md-6 q-pr-md q-pa-md">
            <div class="hero-badge q-mb-sm">
              <q-icon name="stars" size="15px" class="q-mr-xs" />
              Plataforma #1 en Orientación Vocacional
            </div>
            <h1 class="hero-title text-h2 text-weight-bold q-mb-sm">
              ElijeHoy: Descubre tu Vocación y Construye tu Futuro
            </h1>

            <p class="hero-subtitle text-h6 q-mb-md">
              La plataforma líder en orientación vocacional que ha ayudado a miles de jóvenes a encontrar su verdadero camino profesional. Descubre tus talentos únicos y toma decisiones educativas con confianza absoluta.
            </p>

            <div class="hero-actions" style="position: relative; z-index: 10;">
              <q-btn
                unelevated
                size="lg"
                color="purple-7"
                label="Comenzar Test Gratuito"
                icon="rocket_launch"
                to="/test"
                class="q-mr-sm q-mb-xs btn-gradient-purple"
                no-caps
              />

              <q-btn
                flat
                size="lg"
                color="white"
                label="Iniciar Sesión"
                icon="login"
                to="/auth/login"
                class="q-mb-xs btn-learn-more"
                no-caps
              />
            </div>
          </div>

          <div class="col-12 col-md-6 text-center q-mt-lg">
            <div class="hero-image-wrapper">
              <img
                src="/hero-avatars-rocket.png"
                alt="Avatares MBTI con cohete despegando"
                class="hero-rocket-image"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ¿Por qué elegir ElijeHoy? -->
    <div id="features" class="features-section q-py-xl">
      <div class="container">
        <div class="text-center q-mb-xl">
          <div class="section-badge q-mb-md">
            <q-icon name="verified" size="20px" class="q-mr-xs" />
            Características
          </div>
          <h2 class="text-h3 text-weight-bold text-purple-10 q-mb-md">
            ¿Por qué elegir ElijeHoy?
          </h2>
          <p class="text-h6 text-grey-7" style="max-width: 700px; margin: 0 auto;">
            Herramientas profesionales diseñadas específicamente para ayudarte en tu decisión vocacional
          </p>
        </div>

        <div class="row q-col-gutter-lg justify-center">
          <div class="col-12 col-md-5">
            <q-card class="feature-card full-height">
              <q-card-section>
                <div class="feature-icon bg-amber-1">
                  <q-icon name="verified_user" size="48px" color="amber-8" />
                </div>
                <h3 class="text-h5 text-weight-bold text-purple-10 q-mb-md q-mt-md">
                  Resultados Confiables
                </h3>
                <p class="text-body1 text-grey-7">
                  Análisis profundo basado en tus intereses genuinos, habilidades naturales y rasgos únicos de personalidad para orientarte con precisión.
                </p>
                <q-btn
                  flat
                  no-caps
                  label="Ver Resultados"
                  to="/auth/registro"
                  color="amber-8"
                  class="q-mt-md feature-link"
                  icon="arrow_forward"
                />
              </q-card-section>
            </q-card>
          </div>

          <div class="col-12 col-md-5">
            <q-card class="feature-card full-height">
              <q-card-section>
                <div class="feature-icon bg-pink-1">
                  <q-icon name="support_agent" size="48px" color="pink-7" />
                </div>
                <h3 class="text-h5 text-weight-bold text-purple-10 q-mb-md q-mt-md">
                  Acompañamiento Integral
                </h3>
                <p class="text-body1 text-grey-7">
                  Te brindamos el apoyo necesario para tomar decisiones educativas y profesionales importantes con total confianza y seguridad.
                </p>
                <q-btn
                  flat
                  no-caps
                  label="Obtener Apoyo"
                  to="/auth/login"
                  color="pink-7"
                  class="q-mt-md feature-link"
                  icon="arrow_forward"
                />
              </q-card-section>
            </q-card>
          </div>
        </div>
      </div>
    </div>

    <!-- Cómo Funciona -->
    <div id="how-it-works" class="process-section bg-purple-1 q-py-xl">
      <div class="container">
        <div class="text-center q-mb-xl">
          <div class="section-badge q-mb-md">
            <q-icon name="auto_awesome" size="20px" class="q-mr-xs" />
            Proceso Simple
          </div>
          <h2 class="text-h3 text-weight-bold text-purple-10 q-mb-md">
            Cómo Funciona Nuestro Test Vocacional
          </h2>
          <p class="text-h6 text-grey-7" style="max-width: 700px; margin: 0 auto;">
            En solo 3 pasos descubre tu verdadera vocación
          </p>
        </div>

        <div class="row q-col-gutter-lg">
          <div class="col-12 col-md-4">
            <div class="process-card">
              <div class="process-number">01</div>
              <div class="process-icon bg-purple-7">
                <q-icon name="quiz" size="40px" color="white" />
              </div>
              <h3 class="text-h5 text-weight-bold text-purple-10 q-mb-md q-mt-md">
                Responde Preguntas Estratégicas
              </h3>
              <p class="text-body1 text-grey-7">
                Cuestionario científicamente diseñado para identificar tus fortalezas naturales, intereses genuinos y preferencias profesionales únicas.
              </p>
            </div>
          </div>

          <div class="col-12 col-md-4">
            <div class="process-card">
              <div class="process-number">02</div>
              <div class="process-icon bg-amber-8">
                <q-icon name="analytics" size="40px" color="white" />
              </div>
              <h3 class="text-h5 text-weight-bold text-purple-10 q-mb-md q-mt-md">
                Obtén tu Perfil Vocacional
              </h3>
              <p class="text-body1 text-grey-7">
                Recibe un análisis detallado con recomendaciones personalizadas de carreras, áreas de estudio y opciones profesionales ideales para ti.
              </p>
            </div>
          </div>

          <div class="col-12 col-md-4">
            <div class="process-card">
              <div class="process-number">03</div>
              <div class="process-icon bg-pink-7">
                <q-icon name="explore" size="40px" color="white" />
              </div>
              <h3 class="text-h5 text-weight-bold text-purple-10 q-mb-md q-mt-md">
                Explora Recursos Exclusivos
              </h3>
              <p class="text-body1 text-grey-7">
                Accede a guías especializadas, información de universidades y herramientas para planificar estratégicamente tu futuro académico.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Beneficios para Estudiantes y Padres -->
    <div class="benefits-section q-py-xl">
      <div class="container">
        <div class="text-center q-mb-xl">
          <div class="section-badge q-mb-md">
            <q-icon name="diamond" size="20px" class="q-mr-xs" />
            Beneficios
          </div>
          <h2 class="text-h3 text-weight-bold text-purple-10 q-mb-md">
            Beneficios para Estudiantes y Padres
          </h2>
        </div>

        <div class="row q-col-gutter-lg">
          <div class="col-12 col-md-4">
            <q-card class="benefit-card full-height">
              <q-card-section>
                <div class="benefit-icon">
                  <q-icon name="school" size="48px" color="purple-7" />
                </div>
                <h3 class="text-h5 text-weight-bold text-purple-10 q-mb-md">
                  Para Estudiantes
                </h3>
                <p class="text-body1 text-grey-7">
                  Obtén claridad total y seguridad emocional para elegir tu carrera o estudios superiores. Elimina dudas y toma decisiones fundamentadas en tu verdadero potencial.
                </p>
              </q-card-section>
            </q-card>
          </div>

          <div class="col-12 col-md-4">
            <q-card class="benefit-card full-height">
              <q-card-section>
                <div class="benefit-icon">
                  <q-icon name="family_restroom" size="48px" color="amber-8" />
                </div>
                <h3 class="text-h5 text-weight-bold text-purple-10 q-mb-md">
                  Para Padres
                </h3>
                <p class="text-body1 text-grey-7">
                  Recibe herramientas valiosas para entender mejor a tus hijos y acompañarlos de manera efectiva en este momento crucial de elección profesional.
                </p>
              </q-card-section>
            </q-card>
          </div>

          <div class="col-12 col-md-4">
            <q-card class="benefit-card full-height">
              <q-card-section>
                <div class="benefit-icon">
                  <q-icon name="devices" size="48px" color="pink-7" />
                </div>
                <h3 class="text-h5 text-weight-bold text-purple-10 q-mb-md">
                  Acceso Universal
                </h3>
                <p class="text-body1 text-grey-7">
                  Plataforma completamente accesible desde cualquier dispositivo móvil, tablet o computadora, con resultados inmediatos y descargables al instante.
                </p>
              </q-card-section>
            </q-card>
          </div>
        </div>
      </div>
    </div>

    <!-- FAQ Section -->
    <div id="faq" class="faq-section q-py-xl">
      <div class="container">
        <div class="text-center q-mb-xl">
          <div class="section-badge q-mb-md">
            <q-icon name="help_outline" size="20px" class="q-mr-xs" />
            FAQs
          </div>
          <h2 class="text-h3 text-weight-bold text-purple-10 q-mb-md">
            Preguntas Frecuentes
          </h2>
        </div>

        <div class="row justify-center">
          <div class="col-12 col-md-10">
            <q-list class="faq-list">
              <q-expansion-item
                expand-separator
                icon="help"
                label="¿Cuánto tiempo dura el test completo?"
                header-class="text-purple-10 text-weight-bold text-h6"
                expand-icon-class="text-purple-7"
              >
                <q-card flat class="bg-purple-1">
                  <q-card-section>
                    <p class="text-body1 text-grey-8">
                      Aproximadamente 15 minutos para completar todas las secciones. Puedes pausar y continuar cuando gustes sin perder progreso.
                    </p>
                  </q-card-section>
                </q-card>
              </q-expansion-item>

              <q-expansion-item
                expand-separator
                icon="help"
                label="¿Es realmente completamente gratis?"
                header-class="text-purple-10 text-weight-bold text-h6"
                expand-icon-class="text-purple-7"
              >
                <q-card flat class="bg-purple-1">
                  <q-card-section>
                    <p class="text-body1 text-grey-8">
                      Sí, el test vocacional básico es totalmente gratuito. Ofrecemos opciones premium con análisis más profundos para quien lo necesite.
                    </p>
                  </q-card-section>
                </q-card>
              </q-expansion-item>

              <q-expansion-item
                expand-separator
                icon="help"
                label="¿Puedo repetir el test las veces que quiera?"
                header-class="text-purple-10 text-weight-bold text-h6"
                expand-icon-class="text-purple-7"
              >
                <q-card flat class="bg-purple-1">
                  <q-card-section>
                    <p class="text-body1 text-grey-8">
                      Absolutamente. Puedes realizar el test nuevamente para ver cómo evolucionan tus intereses y preferencias a lo largo del tiempo.
                    </p>
                  </q-card-section>
                </q-card>
              </q-expansion-item>

              <q-expansion-item
                expand-separator
                icon="help"
                label="¿Qué hago después de recibir mis resultados?"
                header-class="text-purple-10 text-weight-bold text-h6"
                expand-icon-class="text-purple-7"
              >
                <q-card flat class="bg-purple-1">
                  <q-card-section>
                    <p class="text-body1 text-grey-8">
                      Te proporcionamos asesoría personalizada y recursos adicionales para que puedas seguir avanzando en tu proceso de decisión profesional.
                    </p>
                  </q-card-section>
                </q-card>
              </q-expansion-item>
            </q-list>
          </div>
        </div>
      </div>

      <div class="text-center q-mt-xl q-mb-lg">
        <div class="text-h6 text-grey-7 q-mb-md">¿No encuentras tu respuesta?</div>
        <div class="q-gutter-sm">
          <q-btn
            outline
            color="purple-7"
            label="Contactar Soporte"
            to="#contact"
            icon="contact_support"
            class="faq-support-btn"
            no-caps
          />
        </div>
      </div>
    </div>

    <!-- CTA Final Section -->
    <div class="cta-section q-py-xl">
      <div class="container text-center">
        <div class="cta-icon q-mb-md">
          <q-icon name="stars" size="64px" color="amber-8" />
        </div>
        <h2 class="text-h3 text-weight-bold text-white q-mb-md">
          ¡Empieza Hoy!
        </h2>
        <h3 class="text-h5 text-white q-mb-md">
          Construye tu Futuro con ElijeHoy
        </h3>
        <p class="text-h6 text-white-7 q-mb-xl" style="max-width: 800px; margin: 0 auto 2rem;">
          No esperes más para descubrir tu verdadera vocación. Miles de estudiantes ya han transformado su futuro profesional con nuestra plataforma. Es tu momento de brillar y encontrar el camino que realmente te apasiona.
        </p>

        <div class="q-mb-xl">
          <q-btn
            unelevated
            size="xl"
            label="Realizar Test Vocacional Ahora"
            icon="rocket_launch"
            to="/test"
            class="q-mr-md q-mb-md btn-gradient-yellow"
            no-caps
          />
          <q-btn
            outline
            size="xl"
            color="white"
            label="Contacto y Soporte"
            icon="support_agent"
            class="q-mb-md btn-outline-white"
            no-caps
          />
        </div>

        <div class="text-body1 text-white-7 q-mb-md">
          Síguenos en nuestras redes sociales
        </div>

        <div class="social-links">
          <q-btn
            flat
            round
            icon="fab fa-facebook"
            size="lg"
            color="white"
            class="q-mx-sm social-btn"
          />
          <q-btn
            flat
            round
            icon="fab fa-instagram"
            size="lg"
            color="white"
            class="q-mx-sm social-btn"
          />
          <q-btn
            flat
            round
            icon="fab fa-linkedin"
            size="lg"
            color="white"
            class="q-mx-sm social-btn"
          />
        </div>
      </div>
    </div>

    <!-- Footer -->
    <div id="contact" class="lp-footer bg-grey-10 text-white">
      <div class="q-pa-lg">
        <div class="row q-col-gutter-lg">
          <div class="col-12 col-md-3">
            <div class="text-h6 q-mb-sm">
              <q-icon name="school" size="28px" class="q-mr-sm" />
              ElijoHoy
            </div>
            <p class="text-body2 text-grey-5">
              La plataforma líder en orientación vocacional. Ayudamos a estudiantes a descubrir su vocación y tomar decisiones informadas sobre su futuro profesional.
            </p>
            <div class="q-mt-md">
              <q-btn
                flat
                no-caps
                label="Política de Privacidad"
                class="footer-link q-pa-none"
                color="grey-5"
                size="sm"
              />
              <br>
              <q-btn
                flat
                no-caps
                label="Términos de Servicio"
                class="footer-link q-pa-none"
                color="grey-5"
                size="sm"
              />
            </div>
          </div>

          <div class="col-12 col-md-3">
            <div class="text-h6 q-mb-sm">Plataforma</div>
            <div class="q-gutter-sm">
              <q-btn
                flat
                no-caps
                label="Hacer Test Vocacional"
                to="/test"
                class="footer-link q-pa-none"
                color="grey-5"
                size="sm"
              />
              <br>
              <q-btn
                flat
                no-caps
                label="Iniciar Sesión"
                to="/auth/login"
                class="footer-link q-pa-none"
                color="grey-5"
                size="sm"
              />
              <br>
              <q-btn
                flat
                no-caps
                label="Crear Cuenta"
                to="/auth/registro"
                class="footer-link q-pa-none"
                color="grey-5"
                size="sm"
              />
              <br>
              <q-btn
                flat
                no-caps
                label="Dashboard"
                to="/dashboard"
                class="footer-link q-pa-none"
                color="grey-5"
                size="sm"
              />
            </div>
          </div>

          <div class="col-12 col-md-3">
            <div class="text-h6 q-mb-sm">Recursos</div>
          </div> <!-- Closing div added here -->

          <div class="col-12 col-md-3">
            <div class="text-h6 q-mb-sm">Contacto</div>
            <p class="text-body2 text-grey-5">
              <q-icon name="email" size="sm" class="q-mr-xs" />
              andresquilichechavez@gmail.com
            </p>
            <p class="text-body2 text-grey-5">
              <q-icon name="phone" size="sm" class="q-mr-xs" />
              +51 973791654
            </p>
            <p class="text-body2 text-grey-5">
              <q-icon name="location_on" size="sm" class="q-mr-xs" />
              Lima, Perú
            </p>
          </div>
        </div>

        <q-separator class="q-my-md" dark />

        <div class="text-center text-caption text-grey-6">
          &copy; {{ currentYear }} ElijoHoy. Todos los derechos reservados.
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, computed, onMounted } from 'vue'

export default defineComponent({
  name: 'LandingPage',
  setup() {
    const rating1 = ref(5)
    const rating2 = ref(5)
    const rating3 = ref(5)

    const currentYear = computed(() => new Date().getFullYear())

    onMounted(() => {
      // Limpiar TODOS los datos al entrar al landing (test, autenticación, etc.)
      console.log('Landing: Limpiando todos los datos del test y sesión')

      // Datos de test
      localStorage.removeItem('testSesion')
      localStorage.removeItem('testRespuestas')
      localStorage.removeItem('tokenAnonimo')

      // Datos de autenticación
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
      localStorage.removeItem('user_data')
      localStorage.removeItem('user_token')
      localStorage.removeItem('idUsuario')

      console.log('Landing: Limpieza completada')
    })

    return {
      rating1,
      rating2,
      rating3,
      currentYear
    }
  }
})
</script>

<style scoped>
.landing-page {
  min-height: 100vh;
}

.lp-footer {
  width: 100%;
}

/* Hero Section */
.hero-section {
  height: calc(100vh - 3.5rem);
  min-height: 500px;
  background: linear-gradient(135deg, #6366F1 0%, #4F46E5 25%, #3730A3 50%, #1E1B4B 100%);
  display: flex;
  align-items: center;
  padding: clamp(1rem, 2vh, 2rem) 0;
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: clamp(18.75rem, 45vw, 37.5rem);
  height: clamp(18.75rem, 45vw, 37.5rem);
  background: radial-gradient(circle, rgba(245, 158, 11, 0.15) 0%, transparent 70%);
  border-radius: 50%;
  animation: floatOrb 6s ease-in-out infinite;
}

.hero-section::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: clamp(12.5rem, 30vw, 25rem);
  height: clamp(12.5rem, 30vw, 25rem);
  background: radial-gradient(circle, rgba(236, 72, 153, 0.1) 0%, transparent 70%);
  border-radius: 50%;
  animation: floatOrb 8s ease-in-out infinite reverse;
}

@keyframes floatOrb {
  0%, 100% {
    transform: scale(1) translateY(0px);
    opacity: 0.6;
  }
  50% {
    transform: scale(1.1) translateY(-20px);
    opacity: 0.8;
  }
}

.container {
  max-width: clamp(56.25rem, 90vw, 75rem);
  margin: 0 auto;
  padding: 0 clamp(0.75rem, 2vw, 1.25rem);
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  padding: clamp(1rem, 1.2vw, 0.625rem) clamp(0.875rem, 2vw, 1.25rem);
  background: rgba(245, 158, 11, 0.15);
  backdrop-filter: blur(0.625rem);
  border: 1px solid rgba(245, 158, 11, 0.3);
  border-radius: clamp(1.5rem, 4vw, 3.125rem);
  color: #F59E0B;
  font-weight: 600;
  font-size: clamp(0.75rem, 1.2vw, 0.875rem);
  letter-spacing: 0.025em;
  box-shadow: 0 0.25rem 1rem rgba(245, 158, 11, 0.1);
  animation: fadeInScale 0.8s ease-out;
}

.hero-title {
  color: white;
  font-size: clamp(1.75rem, 5vw, 3.5rem);
  font-weight: 800;
  line-height: 1.1;
  letter-spacing: -0.025em;
  margin-bottom: clamp(1rem, 2vw, 1.5rem);
  animation: fadeInUp 1s ease-out 0.2s both;
}

.hero-subtitle {
  color: rgba(255, 255, 255, 0.9);
  font-size: clamp(1rem, 2vw, 1.25rem);
  font-weight: 400;
  line-height: 1.6;
  max-width: clamp(18.75rem, 90vw, 37.5rem);
  animation: fadeInUp 1s ease-out 0.4s both;
}

.btn-gradient-purple {
  background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
  color: white;
  font-weight: 600;
  border-radius: clamp(0.5rem, 1.5vw, 0.75rem);
  padding: clamp(0.75rem, 2vw, 1rem) clamp(1.5rem, 4vw, 2rem);
  box-shadow: 0 0.5rem 1.5rem rgba(99, 102, 241, 0.4);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: none;
  position: relative;
  overflow: hidden;
  z-index: 10;
}

.btn-gradient-purple::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.6s;
}

.btn-gradient-purple:hover {
  transform: translateY(-0.1875rem);
  box-shadow: 0 0.75rem 2rem rgba(99, 102, 241, 0.6);
}

.btn-gradient-purple:hover::before {
  left: 100%;
}

.btn-outline {
  border: 0.125rem solid rgba(255, 255, 255, 0.8);
  color: white;
  font-weight: 600;
  border-radius: clamp(0.5rem, 1.5vw, 0.75rem);
  padding: clamp(0.625rem, 1.8vw, 0.875rem) clamp(1.5rem, 4vw, 2rem);
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(0.625rem);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.btn-outline:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: white;
  transform: translateY(-0.125rem);
  box-shadow: 0 0.5rem 1.5rem rgba(255, 255, 255, 0.1);
}

.btn-learn-more {
  border: 0.125rem solid rgba(99, 102, 241, 0.3);
  color: #6366F1;
  font-weight: 600;
  border-radius: clamp(0.5rem, 1.5vw, 0.75rem);
  padding: clamp(0.625rem, 1.5vw, 0.75rem) clamp(1.25rem, 3vw, 1.5rem);
  background: rgba(99, 102, 241, 0.05);
  backdrop-filter: blur(0.625rem);
  transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
  position: relative;
  z-index: 10;
}

.btn-learn-more:hover {
  background: rgba(99, 102, 241, 0.1);
  border-color: rgba(99, 102, 241, 0.5);
  transform: translateY(-0.125rem);
  box-shadow: 0 0.5rem 1.5rem rgba(99, 102, 241, 0.2);
}

.feature-link {
  font-weight: 600;
  border-radius: clamp(0.4rem, 1vw, 0.5rem);
  padding: clamp(0.4rem, 1vw, 0.5rem) clamp(0.75rem, 2vw, 1rem);
  transition: all 0.3s ease;
  opacity: 0.8;
}

.feature-link:hover {
  opacity: 1;
  transform: translateX(0.25rem);
}

.btn-more-testimonials {
  border: 0.125rem solid rgba(99, 102, 241, 0.3);
  font-weight: 600;
  border-radius: clamp(0.75rem, 2vw, 1rem);
  padding: clamp(0.625rem, 1.8vw, 0.875rem) clamp(1.5rem, 4vw, 2rem);
  background: rgba(99, 102, 241, 0.05);
  backdrop-filter: blur(0.625rem);
  transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
}

.btn-more-testimonials:hover {
  background: rgba(99, 102, 241, 0.1);
  border-color: rgba(99, 102, 241, 0.5);
  transform: translateY(-0.25rem);
  box-shadow: 0 0.75rem 2rem rgba(99, 102, 241, 0.3);
}

.faq-support-btn,
.faq-guide-btn {
  border-radius: clamp(0.5rem, 1.5vw, 0.75rem);
  font-weight: 600;
  padding: clamp(0.625rem, 1.5vw, 0.75rem) clamp(1.25rem, 3vw, 1.5rem);
  margin: 0 clamp(0.4rem, 1vw, 0.5rem);
  transition: all 0.3s ease;
}

.faq-support-btn:hover,
.faq-guide-btn:hover {
  transform: translateY(-0.125rem);
  box-shadow: 0 0.5rem 1.5rem rgba(99, 102, 241, 0.2);
}

.footer-link {
  text-align: left;
  justify-content: flex-start;
  min-height: auto;
  padding: clamp(0.2rem, 0.5vw, 0.25rem) 0;
  font-size: clamp(0.775rem, 1.1vw, 0.875rem);
  transition: all 0.3s ease;
}

.footer-link:hover {
  color: #6366F1 !important;
  transform: translateX(0.25rem);
}

.social-btn {
  transition: all 0.3s ease;
}

.social-btn:hover {
  transform: translateY(-0.125rem);
  color: #6366F1 !important;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: clamp(1.5rem, 3vw, 2rem);
  font-weight: 700;
  color: #FDB813;
  line-height: 1;
}

.stat-label {
  color: rgba(255, 255, 255, 0.8);
  font-size: clamp(0.8rem, 1.2vw, 0.9rem);
  margin-top: clamp(0.2rem, 0.5vw, 0.25rem);
}

/* Hero Image */
.hero-image-wrapper {
  position: relative;
  height: clamp(400px, 60vh, 650px);
  animation: fadeInRight 1.2s ease-out 0.4s both;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-rocket-image {
  max-width: 120%;
  max-height: 120%;
  width: auto;
  height: auto;
  object-fit: contain;
  filter: drop-shadow(0 20px 40px rgba(0, 0, 0, 0.3));
  animation: floatRocket 4s ease-in-out infinite;
  transform: scale(1.3);
}

@keyframes floatRocket {
  0%, 100% {
    transform: scale(1.3) translateY(0);
  }
  50% {
    transform: scale(1.3) translateY(-15px);
  }
}

/* Sections */
.features-section,
.benefits-section,
.faq-section {
  padding: clamp(2.5rem, 6vh, 5rem) 0;
  background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
}

.process-section,
.testimonials-section {
  padding: clamp(2.5rem, 6vh, 5rem) 0;
  background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
}

.section-badge {
  display: inline-flex;
  align-items: center;
  padding: clamp(0.4rem, 1vw, 0.5rem) clamp(0.75rem, 2vw, 1rem);
  background: rgba(99, 102, 241, 0.1);
  backdrop-filter: blur(0.625rem);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: clamp(1.5rem, 4vw, 3.125rem);
  color: #6366F1;
  font-weight: 600;
  font-size: clamp(0.725rem, 1.1vw, 0.8125rem);
  letter-spacing: 0.025em;
  box-shadow: 0 0.25rem 1rem rgba(99, 102, 241, 0.1);
  animation: fadeInScale 0.8s ease-out;
}

/* Feature Cards */
.feature-card {
  border-radius: clamp(0.75rem, 2vw, 1rem);
  border: 0.125rem solid #F3F4F6;
  transition: all 0.3s ease;
  overflow: hidden;
}

.feature-card:hover {
  border-color: #7C3AED;
  transform: translateY(-0.5rem);
  box-shadow: 0 0.75rem 2.5rem rgba(124, 58, 237, 0.15);
}

.feature-icon {
  width: clamp(3.5rem, 8vw, 5rem);
  height: clamp(3.5rem, 8vw, 5rem);
  border-radius: clamp(0.75rem, 2vw, 1rem);
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Process Cards */
.process-card {
  background: white;
  border-radius: clamp(0.75rem, 2.5vw, 1.25rem);
  padding: clamp(1.5rem, 4vw, 2rem);
  text-align: center;
  position: relative;
  box-shadow: 0 0.25rem 1.25rem rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.process-card:hover {
  transform: translateY(-0.5rem);
  box-shadow: 0 0.5rem 1.875rem rgba(0, 0, 0, 0.12);
}

.process-number {
  position: absolute;
  top: clamp(1rem, 2.5vw, 1.25rem);
  right: clamp(1rem, 2.5vw, 1.25rem);
  font-size: clamp(2rem, 5vw, 3rem);
  font-weight: 700;
  color: rgba(124, 58, 237, 0.1);
  line-height: 1;
}

.process-icon {
  width: clamp(3.5rem, 8vw, 5rem);
  height: clamp(3.5rem, 8vw, 5rem);
  border-radius: clamp(0.75rem, 2vw, 1rem);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}

/* Benefit Cards */
.benefit-card {
  border-radius: clamp(0.75rem, 2vw, 1rem);
  border: 0.125rem solid #F3F4F6;
  transition: all 0.3s ease;
}

.benefit-card:hover {
  border-color: #FDB813;
  transform: translateY(-0.5rem);
  box-shadow: 0 0.75rem 2.5rem rgba(253, 184, 19, 0.15);
}

.benefit-icon {
  width: clamp(3.5rem, 8vw, 5rem);
  height: clamp(3.5rem, 8vw, 5rem);
  border-radius: clamp(0.75rem, 2vw, 1rem);
  background: rgba(124, 58, 237, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: clamp(1rem, 2.5vw, 1.25rem);
}

/* Testimonial Cards */
.testimonial-card {
  background: white;
  border-radius: clamp(0.75rem, 2vw, 1rem);
  box-shadow: 0 0.25rem 1.25rem rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  height: 100%;
}

.testimonial-card:hover {
  transform: translateY(-0.5rem);
  box-shadow: 0 0.5rem 1.875rem rgba(0, 0, 0, 0.12);
}

/* FAQ */
.faq-list {
  border-radius: clamp(0.5rem, 1.5vw, 0.75rem);
  overflow: hidden;
}

.faq-list :deep(.q-item) {
  padding: clamp(1rem, 2.5vw, 1.25rem);
  border-bottom: 1px solid #F3F4F6;
}

/* CTA Section */
.cta-section {
  padding: clamp(3rem, 8vh, 6rem) 0;
  background: linear-gradient(135deg, #6366F1 0%, #4F46E5 25%, #3730A3 50%, #1E1B4B 100%);
  position: relative;
  overflow: hidden;
}

.cta-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="rgba(255,255,255,0.03)"/><circle cx="75" cy="75" r="1" fill="rgba(255,255,255,0.03)"/><circle cx="10" cy="60" r="0.5" fill="rgba(255,255,255,0.02)"/><circle cx="90" cy="20" r="0.5" fill="rgba(255,255,255,0.02)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
  opacity: 0.5;
}

.cta-icon {
  animation: bounceIn 1s ease-out, pulse 3s ease-in-out infinite 1s;
}

@keyframes bounceIn {
  0% {
    opacity: 0;
    transform: scale(0.3);
  }
  50% {
    opacity: 1;
    transform: scale(1.05);
  }
  70% {
    transform: scale(0.9);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

.text-white-7 {
  color: rgba(255, 255, 255, 0.7);
}

.btn-gradient-yellow {
  background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
  color: #1E1B4B;
  font-weight: 700;
  border-radius: 12px;
  padding: 18px 40px;
  box-shadow: 0 8px 24px rgba(245, 158, 11, 0.4);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: none;
  position: relative;
  overflow: hidden;
}

.btn-gradient-yellow::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.6s;
}

.btn-gradient-yellow:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 32px rgba(245, 158, 11, 0.6);
}

.btn-gradient-yellow:hover::before {
  left: 100%;
}

.btn-outline-white {
  border: 2px solid rgba(255, 255, 255, 0.8);
  color: white;
  font-weight: 600;
  border-radius: 12px;
  padding: 16px 40px;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.btn-outline-white:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: white;
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(255, 255, 255, 0.1);
}

.social-links {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 2rem;
}

.social-btn {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 50%;
  padding: 12px;
}

.social-btn:hover {
  transform: scale(1.1) translateY(-2px);
  background: rgba(255, 255, 255, 0.1) !important;
  box-shadow: 0 8px 24px rgba(255, 255, 255, 0.1);
}

/* Responsive */
@media (max-width: 768px) {
  .hero-section {
    min-height: auto;
    padding: 60px 0 40px;
  }

  .hero-title {
    font-size: 2rem;
  }

  .hero-subtitle {
    font-size: 1rem;
  }

  .hero-actions .q-btn {
    display: block;
    width: 100%;
    margin: 0 0 16px 0 !important;
  }

  .stat-item {
    flex: 1;
  }

  .hero-image-wrapper {
    height: 350px;
    margin-top: 20px;
  }

  .hero-rocket-image {
    max-height: 350px;
    transform: scale(1.2);
  }

  .features-section,
  .process-section,
  .benefits-section,
  .testimonials-section,
  .faq-section,
  .cta-section {
    padding: 40px 0;
  }

  .text-h3 {
    font-size: 1.75rem;
  }

  .process-number {
    font-size: 2rem;
    top: 15px;
    right: 15px;
  }
}

@media (max-width: 400px) {
  .hero-badge,
  .section-badge {
    font-size: 12px;
    padding: 6px 12px;
  }

  .stat-number {
    font-size: 1.5rem;
  }
}

/* Professional Animations */
.fade-in-up {
  animation: fadeInUp 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-in-left {
  animation: fadeInLeft 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-in-right {
  animation: fadeInRight 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-in-scale {
  animation: fadeInScale 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInLeft {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes fadeInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
