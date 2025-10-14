import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    allowedHosts: ['elijohoy.com', 'www.elijohoy.com'], // Agrega los dominios permitidos
    fs: {
      allow: ['..', '/root/elijohoy/elijohoy-fronted', './'] // Agrega './' para permitir el uso del archivo .env.production
    },
    host: '0.0.0.0', // Asegúrate de que el servidor escuche en todas las interfaces
    port: 9000, // Puerto del frontend
  },
  // ...otras configuraciones
});