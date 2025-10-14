import { defineConfig } from 'vite';

export default defineConfig({
    server: {
        allowedHosts: ['elijohoy.com', 'www.elijohoy.com'],
        host: '0.0.0.0',
        port: 9000,
    }
    // ...otras configuraciones
});