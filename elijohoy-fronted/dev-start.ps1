# Script de desarrollo - ElijoHoy Frontend
# Este script configura y ejecuta el frontend Quasar

Write-Host "🎨 Iniciando ElijoHoy Frontend..." -ForegroundColor Cyan

# Verificar si Node.js está instalado
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js detectado: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js no está instalado. Por favor instala Node.js primero." -ForegroundColor Red
    exit 1
}

# Verificar si existe package.json
if (-not (Test-Path "package.json")) {
    Write-Host "❌ package.json no encontrado. Asegúrate de estar en la carpeta del frontend." -ForegroundColor Red
    exit 1
}

# Instalar dependencias si no existen
if (-not (Test-Path "node_modules")) {
    Write-Host "📦 Instalando dependencias..." -ForegroundColor Yellow
    npm install
}

# Verificar si Quasar CLI está instalado globalmente
try {
    $quasarVersion = quasar --version
    Write-Host "✅ Quasar CLI detectado: $quasarVersion" -ForegroundColor Green
} catch {
    Write-Host "📦 Instalando Quasar CLI globalmente..." -ForegroundColor Yellow
    npm install -g @quasar/cli
}

# Mostrar información importante
Write-Host ""
Write-Host "📋 Información del proyecto:" -ForegroundColor Cyan
Write-Host "🌐 Frontend se ejecutará en: http://localhost:9000" -ForegroundColor White
Write-Host "🔗 Asegúrate de que el backend esté ejecutándose en: http://localhost:5000" -ForegroundColor White
Write-Host "⏹️  Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""

# Ejecutar el servidor de desarrollo
Write-Host "🚀 Iniciando servidor de desarrollo..." -ForegroundColor Green
quasar dev