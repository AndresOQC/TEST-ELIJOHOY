module.exports = {
  apps: [
    {
      name: 'elijohoy-frontend-dev',
      cwd: '/root/elijohoy/elijohoy-fronted',
      script: 'npm',
      args: 'run dev -- --host 0.0.0.0 --port 9000 --open false',
      env: {
        NODE_ENV: 'development'
      },
      // si usas nvm con node en otro PATH, pm2 startup pedirá ajustar PATH
    }
  ]
}
