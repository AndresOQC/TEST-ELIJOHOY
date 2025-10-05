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
  
  // Dashboard routes (authenticated)
  {
    path: '/dashboard',
    component: () => import('layouts/DashboardLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', component: () => import('pages/dashboard/DashboardPage.vue') },
      { path: 'configuraciones', component: () => import('pages/dashboard/ConfiguracionesPage.vue') },
      { path: 'test-resultados', component: () => import('pages/dashboard/TestResultadosPage.vue') }
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
