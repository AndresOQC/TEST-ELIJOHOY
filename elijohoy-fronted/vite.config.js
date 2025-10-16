import { defineConfig } from 'vite';

export default defineConfig({
<<<<<<< HEAD
    server: {
    allowedHosts: ['elijohoy.com', 'www.elijohoy.com'], // Agrega los dominios permitidos
    host: '0.0.0.0', // Escucha en todas las interfaces
    port: 9000, // Puerto del frontend
    },
  // ...otras configuraciones
});
=======
  server: {
    host: '0.0.0.0',
    port: 9000,
    allowedHosts: ['elijohoy.com', 'www.elijohoy.com', 'localhost', '127.0.0.1'],
    hmr: { host: 'elijohoy.com', protocol: 'wss', clientPort: 443 } // detrás de HTTPS
  }
});
>>>>>>> 90582355ed0cf382f8a94a6aba2c1f3a3e35532b
