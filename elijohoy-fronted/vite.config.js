import { defineConfig } from 'vite';

export default defineConfig({
    server: {
        allowedHosts: ['elijohoy.com', 'www.elijohoy.com', 'localhost', '185.111.156.248'],
        host: '0.0.0.0',
        port: 9000,
    }
    // ...otras configuraciones
});