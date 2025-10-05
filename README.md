# ElijHoy - Sistema de Orientación Vocacional

Sistema web para orientación vocacional de estudiantes con autenticación, gestión de perfiles y preparado para tests vocacionales.

## Estructura del Proyecto

- `elijohoy-backend/`: API REST con Flask y PostgreSQL
- `elijohoy-fronted/`: Aplicación web con Vue.js y Quasar

## Características

### Backend
- ✅ Autenticación con JWT (login, registro, logout)
- ✅ Recuperación de contraseña con email (SMTP Gmail)
- ✅ Gestión de usuarios y estudiantes
- ✅ Roles: admin y estudiante
- ✅ Perfil de estudiante con datos personales e institucionales
- ✅ Rate limiting y seguridad
- ✅ PostgreSQL con migraciones

### Frontend
- ✅ Landing page profesional con header y footer
- ✅ Sistema de autenticación completo
- ✅ Dashboard con sidebar
- ✅ Página de configuración de perfil
- ✅ Diseño responsive y moderno
- ✅ Componentes reutilizables

## Requisitos

- Python 3.9+
- Node.js 16+
- PostgreSQL 13+
- Redis (opcional, para rate limiting y caché)
- Cuenta Gmail con App Password (para SMTP)

## Configuración

### 1. Base de Datos

Crear la base de datos PostgreSQL:
```bash
psql -U postgres
CREATE DATABASE elijohoy_db;
CREATE USER elijohoy_user WITH PASSWORD 'elijohoy_password';
GRANT ALL PRIVILEGES ON DATABASE elijohoy_db TO elijohoy_user;
\q
```

### 2. Backend

1. Crear entorno virtual:
```bash
cd elijohoy-backend
python -m venv venv

# En Windows:
venv\Scripts\activate

# En Linux/Mac:
source venv/bin/activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:
```bash
cp .env.example .env
```

Editar `.env` con tus configuraciones:
```env
# Flask
FLASK_ENV=development
SECRET_KEY=tu-secret-key-segura
JWT_SECRET_KEY=tu-jwt-secret-key-segura

# Database
DATABASE_URL=postgresql+psycopg://elijohoy_user:elijohoy_password@localhost:5432/elijohoy_db

# SMTP Gmail (importante para recuperación de contraseña)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu-email@gmail.com
SMTP_PASSWORD=tu-app-password

# Frontend URL
FRONTEND_URL=http://localhost:9000
```

**Nota sobre SMTP Gmail:**
- Necesitas crear un "App Password" en tu cuenta de Gmail
- Ve a: Cuenta de Google → Seguridad → Verificación en 2 pasos → Contraseñas de aplicaciones
- Genera una contraseña de aplicación y úsala en `SMTP_PASSWORD`

4. Inicializar base de datos:
```bash
# Inicializar migraciones (si es primera vez)
flask db init

# Crear migración inicial
flask db migrate -m "Initial migration"

# Aplicar migraciones
flask db upgrade

# Crear roles por defecto
python -c "from app import create_app, init_database; app = create_app(); init_database(app)"
```

5. Crear usuario administrador (opcional):
```bash
flask create-admin
```

6. Ejecutar servidor:
```bash
python app.py
# El servidor correrá en http://localhost:5000
```

### 3. Frontend

1. Instalar dependencias:
```bash
cd elijohoy-fronted
npm install
```

2. Configurar API URL (si es necesario):
Editar `src/boot/axios.js` si la URL del backend es diferente de `http://localhost:5000`

3. Ejecutar en desarrollo:
```bash
npm run dev
# o
quasar dev

# La aplicación correrá en http://localhost:9000
```

4. Compilar para producción:
```bash
npm run build
# o
quasar build
```

## Uso

1. Abre http://localhost:9000 en tu navegador
2. Regístrate como estudiante nuevo
3. Completa tu perfil en Configuraciones
4. Explora el dashboard (TestResultados estará disponible próximamente)

## Estructura de la Base de Datos

### Tablas Principales:
- `usuarios`: Datos de autenticación y básicos
- `estudiantes`: Perfil extendido del estudiante (vinculado a usuarios)
- `roles`: Roles del sistema (admin, estudiante)
- `usuario_rol`: Relación many-to-many entre usuarios y roles
- `otp_tokens`: Tokens de recuperación de contraseña
- `password_reset_tokens`: Tokens para reset de contraseña
- `session_tokens`: Sesiones activas
- `blacklisted_tokens`: Tokens revocados

## API Endpoints

### Autenticación (`/api/auth`)
- `POST /register` - Registro de usuario
- `POST /login` - Iniciar sesión
- `POST /logout` - Cerrar sesión
- `GET /me` - Obtener usuario actual
- `PUT /update-profile` - Actualizar perfil de estudiante
- `POST /recover-password` - Solicitar recuperación de contraseña
- `POST /reset-password` - Restablecer contraseña con token

### Salud
- `GET /` - Info de la API
- `GET /health` - Health check

## Tecnologías

### Backend
- Flask 3.0
- SQLAlchemy 2.0
- PostgreSQL (psycopg3)
- Flask-JWT-Extended (autenticación)
- Argon2 (hashing de passwords)
- Flask-CORS
- Flask-Limiter (rate limiting)
- SMTP (email)

### Frontend
- Vue 3 (Composition API)
- Quasar Framework 2
- Pinia (state management)
- Vue Router
- Axios
- Diseño responsive

## Seguridad

- Passwords hasheados con Argon2
- JWT tokens con expiración
- Rate limiting en endpoints críticos
- CORS configurado
- Validación de inputs
- Bloqueo de cuenta por intentos fallidos
- Tokens de recuperación con expiración

## Próximas Funcionalidades

- [ ] Tests vocacionales
- [ ] Resultados y análisis
- [ ] Recomendaciones de carreras
- [ ] Panel de administración
- [ ] Reportes y estadísticas
- [ ] Notificaciones

## Troubleshooting

### Error de conexión a PostgreSQL
- Verifica que PostgreSQL esté corriendo
- Verifica las credenciales en `.env`
- Asegúrate de que la base de datos existe

### Error de SMTP
- Verifica que uses un App Password de Gmail, no tu contraseña normal
- Verifica que la verificación en 2 pasos esté activada en Gmail

### Error al ejecutar migraciones
```bash
# Eliminar carpeta de migraciones y empezar de nuevo
rm -rf migrations/
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## Licencia

Propietario - © 2024 ElijHoy