import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    host: '0.0.0.0',
    port: 9000,
    allowedHosts: ['elijohoy.com', 'www.elijohoy.com', 'localhost', '127.0.0.1'],
    hmr: { host: 'elijohoy.com', protocol: 'wss', clientPort: 443 } // detrás de HTTPS
  }
});