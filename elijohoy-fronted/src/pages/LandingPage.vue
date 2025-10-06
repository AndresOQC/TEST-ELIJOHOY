<!-- Eliminado script setup para evitar duplicidad de imports y lógica -->
<template>
  <q-page class="landing-page">
    <!-- Hero Section -->
    <div class="hero-section">
      <div class="container">
        <div class="row items-center">
          <div class="col-12 col-md-6 q-pr-md">
            <div class="hero-badge q-mb-md">
              <q-icon name="stars" size="20px" class="q-mr-xs" />
              Plataforma #1 en Orientación Vocacional
            </div>
            <h1 class="hero-title text-h2 text-weight-bold q-mb-md">
              ElijeHoy: Descubre tu Vocación y Construye tu Futuro
            </h1>

            <p class="hero-subtitle text-h6 q-mb-xl">
              La plataforma líder en orientación vocacional que ha ayudado a miles de jóvenes a encontrar su verdadero camino profesional. Descubre tus talentos únicos y toma decisiones educativas con confianza absoluta.
            </p>

            <div class="hero-actions">
              <q-btn
                unelevated
                size="lg"
                color="purple-7"
                label="Comenzar Test Gratuito"
                icon="rocket_launch"
                to="/test"
                class="q-mr-md q-mb-sm btn-gradient-purple"
                no-caps
              />

              <q-btn
                outline
                size="lg"
                color="purple-7"
                label="Iniciar Sesión"
                icon="login"
                to="/auth/login"
                class="q-mb-sm btn-outline"
                no-caps
              />
            </div>

            <!-- Stats -->
            <div class="row q-mt-xl q-gutter-md">
              <div class="stat-item">
                <div class="stat-number">10,000+</div>
                <div class="stat-label">Estudiantes</div>
              </div>
              <div class="stat-item">
                <div class="stat-number">95%</div>
                <div class="stat-label">Satisfacción</div>
              </div>
              <div class="stat-item">
                <div class="stat-number">50+</div>
                <div class="stat-label">Carreras</div>
              </div>
            </div>
          </div>

          <div class="col-12 col-md-6 text-center q-mt-lg">
            <div class="hero-image-wrapper">
              <div class="floating-card card-1">
                <q-icon name="psychology" size="40px" color="purple-7" />
                <div class="text-weight-bold q-mt-sm">Test Vocacional</div>
              </div>
              <div class="floating-card card-2">
                <q-icon name="school" size="40px" color="amber-8" />
                <div class="text-weight-bold q-mt-sm">Orientación</div>
              </div>
              <div class="floating-card card-3">
                <q-icon name="trending_up" size="40px" color="pink-7" />
                <div class="text-weight-bold q-mt-sm">Seguimiento</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ¿Por qué elegir ElijeHoy? -->
    <div class="features-section q-py-xl">
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

        <div class="row q-col-gutter-lg">
          <div class="col-12 col-md-4">
            <q-card class="feature-card full-height">
              <q-card-section>
                <div class="feature-icon bg-purple-1">
                  <q-icon name="groups" size="48px" color="purple-7" />
                </div>
                <h3 class="text-h5 text-weight-bold text-purple-10 q-mb-md q-mt-md">
                  Más de 10,000 Estudiantes
                </h3>
                <p class="text-body1 text-grey-7">
                  Miles de jóvenes han encontrado su camino profesional utilizando nuestro test vocacional personalizado y científicamente validado.
                </p>
              </q-card-section>
            </q-card>
          </div>

          <div class="col-12 col-md-4">
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
              </q-card-section>
            </q-card>
          </div>

          <div class="col-12 col-md-4">
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
              </q-card-section>
            </q-card>
          </div>
        </div>
      </div>
    </div>

    <!-- Cómo Funciona -->
    <div class="process-section bg-purple-1 q-py-xl">
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

    <!-- Testimonios -->
    <div class="testimonials-section bg-purple-1 q-py-xl">
      <div class="container">
        <div class="text-center q-mb-xl">
          <div class="section-badge q-mb-md">
            <q-icon name="format_quote" size="20px" class="q-mr-xs" />
            Testimonios
          </div>
          <h2 class="text-h3 text-weight-bold text-purple-10 q-mb-md">
            Testimonios Reales que Inspiran
          </h2>
          <p class="text-h6 text-grey-7" style="max-width: 700px; margin: 0 auto;">
            Descubre cómo ElijeHoy ha transformado la vida de miles de estudiantes
          </p>
        </div>

        <div class="row q-col-gutter-lg">
          <div class="col-12 col-md-4">
            <q-card class="testimonial-card">
              <q-card-section>
                <div class="row items-center q-mb-md">
                  <q-rating
                    v-model="rating1"
                    size="md"
                    color="amber-8"
                    readonly
                  />
                </div>
                <p class="text-body1 text-grey-8 q-mb-md">
                  "Gracias a ElijeHoy, supe exactamente qué estudiar y ahora estoy en la universidad que siempre soñé. ¡Cambió mi vida completamente!"
                </p>
                <div class="row items-center q-mt-md">
                  <q-avatar size="48px" color="purple-7" text-color="white" icon="person" />
                  <div class="q-ml-md">
                    <div class="text-weight-bold text-purple-10">Ana G.</div>
                    <div class="text-caption text-grey-6">Estudiante de Medicina</div>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>

          <div class="col-12 col-md-4">
            <q-card class="testimonial-card">
              <q-card-section>
                <div class="row items-center q-mb-md">
                  <q-rating
                    v-model="rating2"
                    size="md"
                    color="amber-8"
                    readonly
                  />
                </div>
                <p class="text-body1 text-grey-8 q-mb-md">
                  "El test ayudó a mi hijo a descubrir su verdadera pasión por la ingeniería y tomar una decisión sin miedo ni incertidumbre."
                </p>
                <div class="row items-center q-mt-md">
                  <q-avatar size="48px" color="amber-8" text-color="white" icon="person" />
                  <div class="q-ml-md">
                    <div class="text-weight-bold text-purple-10">Carlos M.</div>
                    <div class="text-caption text-grey-6">Padre de Familia</div>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>

          <div class="col-12 col-md-4">
            <q-card class="testimonial-card">
              <q-card-section>
                <div class="row items-center q-mb-md">
                  <q-rating
                    v-model="rating3"
                    size="md"
                    color="amber-8"
                    readonly
                  />
                </div>
                <p class="text-body1 text-grey-8 q-mb-md">
                  "Plataforma fácil, rápida y extremadamente útil para orientarme en un momento muy difícil y confuso de mi vida académica."
                </p>
                <div class="row items-center q-mt-md">
                  <q-avatar size="48px" color="pink-7" text-color="white" icon="person" />
                  <div class="q-ml-md">
                    <div class="text-weight-bold text-purple-10">Luis P.</div>
                    <div class="text-caption text-grey-6">Bachiller</div>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>
      </div>
    </div>

    <!-- FAQ Section -->
    <div class="faq-section q-py-xl">
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
    <div class="lp-footer bg-grey-10 text-white">
      <div class="q-pa-lg">
        <div class="row q-col-gutter-lg">
          <div class="col-12 col-md-6">
            <div class="text-h6 q-mb-sm">
              <q-icon name="school" size="28px" class="q-mr-sm" />
              ElijoHoy
            </div>
            <p class="text-body2 text-grey-5">
              La plataforma líder en orientación vocacional. Ayudamos a estudiantes a descubrir su vocación y tomar decisiones informadas sobre su futuro profesional.
            </p>
          </div>

          <div class="col-12 col-md-6">
            <div class="text-h6 q-mb-sm">Contacto</div>
            <p class="text-body2 text-grey-5">
              <q-icon name="email" size="sm" class="q-mr-xs" />
              contacto@elijohoy.com
            </p>
            <p class="text-body2 text-grey-5">
              <q-icon name="phone" size="sm" class="q-mr-xs" />
              +51 999 999 999
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
  min-height: 90vh;
  background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%);
  display: flex;
  align-items: center;
  padding: 80px 0 60px;
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(253, 184, 19, 0.2) 0%, transparent 70%);
  border-radius: 50%;
  animation: pulse 4s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.1); opacity: 0.7; }
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  padding: 8px 16px;
  background: rgba(253, 184, 19, 0.2);
  border-radius: 50px;
  color: #FDB813;
  font-weight: 600;
  font-size: 14px;
  border: 1px solid rgba(253, 184, 19, 0.3);
}

.hero-title {
  color: white;
  line-height: 1.2;
}

.hero-subtitle {
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.6;
}

.btn-gradient-purple {
  background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%);
  color: white;
  font-weight: 600;
  border-radius: 12px;
  padding: 14px 32px;
  box-shadow: 0 4px 15px rgba(124, 58, 237, 0.4);
  transition: all 0.3s ease;
}

.btn-gradient-purple:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(124, 58, 237, 0.6);
}

.btn-outline {
  border: 2px solid white;
  color: white;
  font-weight: 600;
  border-radius: 12px;
  padding: 12px 32px;
  transition: all 0.3s ease;
}

.btn-outline:hover {
  background: rgba(255, 255, 255, 0.1);
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: #FDB813;
  line-height: 1;
}

.stat-label {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
  margin-top: 4px;
}

/* Hero Image */
.hero-image-wrapper {
  position: relative;
  height: 400px;
}

.floating-card {
  position: absolute;
  background: white;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  text-align: center;
  animation: float 3s ease-in-out infinite;
}

.card-1 {
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.card-2 {
  top: 50%;
  right: 10%;
  animation-delay: 1s;
}

.card-3 {
  bottom: 10%;
  left: 30%;
  animation-delay: 2s;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
}

/* Sections */
.features-section,
.benefits-section,
.faq-section {
  padding: 80px 0;
  background: white;
}

.process-section,
.testimonials-section {
  padding: 80px 0;
}

.section-badge {
  display: inline-flex;
  align-items: center;
  padding: 6px 14px;
  background: rgba(124, 58, 237, 0.1);
  border-radius: 50px;
  color: #7C3AED;
  font-weight: 600;
  font-size: 13px;
}

/* Feature Cards */
.feature-card {
  border-radius: 16px;
  border: 2px solid #F3F4F6;
  transition: all 0.3s ease;
  overflow: hidden;
}

.feature-card:hover {
  border-color: #7C3AED;
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(124, 58, 237, 0.15);
}

.feature-icon {
  width: 80px;
  height: 80px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Process Cards */
.process-card {
  background: white;
  border-radius: 20px;
  padding: 32px;
  text-align: center;
  position: relative;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.process-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.process-number {
  position: absolute;
  top: 20px;
  right: 20px;
  font-size: 3rem;
  font-weight: 700;
  color: rgba(124, 58, 237, 0.1);
  line-height: 1;
}

.process-icon {
  width: 80px;
  height: 80px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}

/* Benefit Cards */
.benefit-card {
  border-radius: 16px;
  border: 2px solid #F3F4F6;
  transition: all 0.3s ease;
}

.benefit-card:hover {
  border-color: #FDB813;
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(253, 184, 19, 0.15);
}

.benefit-icon {
  width: 80px;
  height: 80px;
  border-radius: 16px;
  background: rgba(124, 58, 237, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

/* Testimonial Cards */
.testimonial-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  height: 100%;
}

.testimonial-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

/* FAQ */
.faq-list {
  border-radius: 12px;
  overflow: hidden;
}

.faq-list :deep(.q-item) {
  padding: 20px;
  border-bottom: 1px solid #F3F4F6;
}

/* CTA Section */
.cta-section {
  padding: 100px 0;
  background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%);
  position: relative;
  overflow: hidden;
}

.cta-section::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(236, 72, 153, 0.2) 0%, transparent 70%);
  border-radius: 50%;
}

.cta-icon {
  animation: bounce 2s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.text-white-7 {
  color: rgba(255, 255, 255, 0.7);
}

.btn-gradient-yellow {
  background: linear-gradient(135deg, #FDB813 0%, #F59E0B 100%);
  color: #4C1D95;
  font-weight: 700;
  border-radius: 12px;
  padding: 16px 40px;
  box-shadow: 0 4px 15px rgba(253, 184, 19, 0.4);
  transition: all 0.3s ease;
}

.btn-gradient-yellow:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(253, 184, 19, 0.6);
}

.btn-outline-white {
  border: 2px solid white;
  color: white;
  font-weight: 600;
  border-radius: 12px;
  padding: 14px 40px;
  transition: all 0.3s ease;
}

.btn-outline-white:hover {
  background: rgba(255, 255, 255, 0.1);
}

.social-btn {
  transition: all 0.3s ease;
}

.social-btn:hover {
  transform: scale(1.1);
  background: rgba(255, 255, 255, 0.1);
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
    height: 300px;
    margin-top: 40px;
  }

  .floating-card {
    padding: 15px;
  }

  .floating-card .q-icon {
    font-size: 32px !important;
  }

  .floating-card .text-weight-bold {
    font-size: 0.85rem;
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
</style>
