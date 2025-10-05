# Script para ejecutar migraciones en PostgreSQL de una sola vez
# Usar desde la raíz del proyecto

# Variables de conexión
$DB_HOST = "localhost"
$DB_PORT = "5432"
$DB_NAME = "elijohoy_db"
$DB_USER = "elijohoy_user"
$DB_PASSWORD = "elijohoy_password"

# Directorio de migraciones
$MIGRATIONS_DIR = "migrations"

# Función para encontrar psql automáticamente
function Find-PostgreSQLPath {
    # Primero verificar si psql está en el PATH
    try {
        $pathResult = Get-Command psql -ErrorAction Stop
        Write-Host "✓ psql encontrado en PATH: $($pathResult.Source)" -ForegroundColor Green
        return $pathResult.Source
    } catch {
        Write-Host "psql no encontrado en PATH, buscando instalación..." -ForegroundColor Yellow
    }
    
    # Buscar en ubicaciones comunes de PostgreSQL
    $commonPaths = @(
        "C:\Program Files\PostgreSQL\*\bin\psql.exe",
        "C:\Program Files (x86)\PostgreSQL\*\bin\psql.exe",
        "C:\PostgreSQL\*\bin\psql.exe",
        "$env:ProgramFiles\PostgreSQL\*\bin\psql.exe",
        "${env:ProgramFiles(x86)}\PostgreSQL\*\bin\psql.exe"
    )
    
    foreach ($pattern in $commonPaths) {
        $found = Get-ChildItem -Path $pattern -ErrorAction SilentlyContinue | Sort-Object Name -Descending | Select-Object -First 1
        if ($found) {
            Write-Host "✓ psql encontrado en: $($found.FullName)" -ForegroundColor Green
            return $found.FullName
        }
    }
    
    # Buscar en todo el sistema (más lento pero exhaustivo)
    Write-Host "Buscando psql.exe en todo el sistema..." -ForegroundColor Yellow
    $systemSearch = Get-ChildItem -Path "C:\" -Name "psql.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($systemSearch) {
        Write-Host "✓ psql encontrado en: $($systemSearch.FullName)" -ForegroundColor Green
        return $systemSearch.FullName
    }
    
    return $null
}

# Encontrar la ruta de psql
$PSQL_PATH = Find-PostgreSQLPath

Write-Host "=== Ejecutando todas las migraciones de ElijHoy Backend ===" -ForegroundColor Green

# Verificar si psql está disponible
if (-not $PSQL_PATH -or -not (Test-Path $PSQL_PATH)) {
    Write-Host ""
    Write-Host "❌ ERROR: No se pudo encontrar psql.exe" -ForegroundColor Red
    Write-Host ""
    Write-Host "SOLUCIONES:" -ForegroundColor Yellow
    Write-Host "1. Instalar PostgreSQL desde: https://www.postgresql.org/download/" -ForegroundColor White
    Write-Host "2. O usar winget: winget install PostgreSQL.PostgreSQL" -ForegroundColor White
    Write-Host "3. O agregar la ruta de PostgreSQL al PATH del sistema" -ForegroundColor White
    Write-Host ""
    exit 1
}

# Configurar la contraseña para evitar prompts
$env:PGPASSWORD = $DB_PASSWORD

# Crear archivo temporal con todas las migraciones
$tempFile = "temp_all_migrations.sql"

Write-Host "Combinando todas las migraciones..." -ForegroundColor Yellow

# Lista de migraciones en orden
$migrations = @(
    "01_roles.sql",
    "02_usuarios.sql", 
    "03_alumnos.sql",
    "04_usuario_rol.sql",
    "05_tokens.sql"
)

# Crear archivo temporal vacío
"" | Out-File -FilePath $tempFile -Encoding UTF8

# Combinar todas las migraciones
foreach ($migration in $migrations) {
    $migrationPath = Join-Path $MIGRATIONS_DIR $migration
    
    if (Test-Path $migrationPath) {
        Write-Host "Agregando: $migration" -ForegroundColor Cyan
        
        # Agregar comentario separador
        "-- =================================================" | Out-File -FilePath $tempFile -Append -Encoding UTF8
        "-- MIGRACIÓN: $migration" | Out-File -FilePath $tempFile -Append -Encoding UTF8
        "-- =================================================" | Out-File -FilePath $tempFile -Append -Encoding UTF8
        "" | Out-File -FilePath $tempFile -Append -Encoding UTF8
        
        # Agregar contenido del archivo
        Get-Content $migrationPath -Encoding UTF8 | Out-File -FilePath $tempFile -Append -Encoding UTF8
        
        # Agregar separador
        "" | Out-File -FilePath $tempFile -Append -Encoding UTF8
        "" | Out-File -FilePath $tempFile -Append -Encoding UTF8
    } else {
        Write-Host "⚠ No encontrado: $migrationPath" -ForegroundColor Yellow
    }
}

Write-Host "Ejecutando todas las migraciones de una vez..." -ForegroundColor Green

try {
    # Verificar conexión primero
    & $PSQL_PATH -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "SELECT 1;" | Out-Null
    Write-Host "✓ Conexión a base de datos exitosa" -ForegroundColor Green
    
    # Ejecutar el archivo combinado
    & $PSQL_PATH -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f $tempFile
    Write-Host ""
    Write-Host "✅ TODAS LAS MIGRACIONES EJECUTADAS EXITOSAMENTE" -ForegroundColor Green
    
} catch {
    Write-Host ""
    Write-Host "❌ ERROR EJECUTANDO MIGRACIONES" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host "Verifica que PostgreSQL esté ejecutándose y las credenciales sean correctas" -ForegroundColor Yellow
    
} finally {
    # Limpiar archivo temporal
    if (Test-Path $tempFile) {
        Remove-Item $tempFile -Force
        Write-Host "Archivo temporal limpiado" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "=== PROCESO COMPLETADO ===" -ForegroundColor Green
Write-Host ""
Write-Host "Próximos pasos:" -ForegroundColor Yellow
Write-Host "1. Crear roles por defecto:" -ForegroundColor White
Write-Host "   flask create-roles" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Crear usuario administrador:" -ForegroundColor White
Write-Host "   flask create-admin" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Iniciar el servidor:" -ForegroundColor White
Write-Host "   python app.py" -ForegroundColor Cyan