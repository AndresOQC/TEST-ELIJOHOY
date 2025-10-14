import { defineConfig } from 'vite';

export default defineConfig({
    server: {
        allowedHosts: ['elijohoy.com', 'www.elijohoy.com'], // Agrega los dominios permitidos
        host: '0.0.0.0', // Escucha en todas las interfaces
        port: 9000, // Puerto del frontend
    },
    // Agrega la ruta permitida
    envDir: '/root/elijohoy/elijohoy-fronted',
    // ...otras configuraciones
});