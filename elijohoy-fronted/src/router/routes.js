const routes = [
  // Landing page
  {
    path: '/',
    component: () => import('layouts/LandingLayout.vue'),
    children: [
      { path: '', component: () => import('pages/LandingPage.vue') }
    ]
  },
  
  // Authentication routes
  {
    path: '/auth',
    component: () => import('layouts/AuthLayout.vue'),
    children: [
      { path: 'login', component: () => import('pages/auth/LoginPage.vue') },
      { path: 'registro', component: () => import('pages/auth/RegistroPage.vue') },
      { path: 'recuperar-password', component: () => import('pages/auth/RecuperarPasswordPage.vue') },
      { path: 'restablecer-password/:token', component: () => import('pages/auth/RestablecerPasswordPage.vue') }
    ]
  },

  // Test público (sin autenticación requerida)
  {
    path: '/test',
    component: () => import('layouts/LandingLayout.vue'),
    children: [
      { path: '', name: 'test-publico', component: () => import('pages/dashboard/TestPage.vue') },
      { path: 'resultados/:id', name: 'test-resultados-publico', component: () => import('pages/dashboard/TestResultadosDetailPage.vue') }
    ]
  },
  
  // Dashboard routes (authenticated)
  {
    path: '/dashboard',
    component: () => import('layouts/DashboardLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', component: () => import('pages/dashboard/DashboardPage.vue') },
      { path: 'configuraciones', component: () => import('pages/dashboard/ConfiguracionesPage.vue') },
      { path: 'test', name: 'test', component: () => import('pages/dashboard/TestPage.vue') },
      { path: 'test-resultados', component: () => import('pages/dashboard/TestResultadosPage.vue') },
      { path: 'test-resultados/:id', name: 'test-resultados', component: () => import('pages/dashboard/TestResultadosDetailPage.vue') },
      { path: 'admin', name: 'admin-dashboard', component: () => import('pages/dashboard/AdminDashboardPage.vue'), meta: { requiresAdmin: true } },
      { path: 'admin/preguntas', name: 'admin-preguntas', component: () => import('pages/dashboard/AdminPreguntasPage.vue'), meta: { requiresAdmin: true } }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
