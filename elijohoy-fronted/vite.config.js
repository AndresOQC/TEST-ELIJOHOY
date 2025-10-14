export default {
  server: {
    allowedHosts: ['elijohoy.com', 'www.elijohoy.com'], // Agrega los dominios permitidos
    fs: {
      allow: ['..', '/root/elijohoy/elijohoy-fronted', './'] // Agrega './' para permitir el uso del archivo .env.production
    }
  },
  // ...resto de la configuración
};