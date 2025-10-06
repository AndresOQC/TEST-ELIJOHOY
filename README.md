# ElijHoy - Sistema de Orientación Vocacional

Sistema web completo para orientación vocacional de estudiantes con tests de personalidad, análisis de resultados, autenticación avanzada y panel de administración.

## Estructura del Proyecto

- `elijohoy-backend/`: API REST con Flask y PostgreSQL
- `elijohoy-fronted/`: Aplicación web con Vue.js y Quasar

## Características

### Backend
- ✅ Autenticación completa con JWT (login, registro, logout, recuperación de contraseña)
- ✅ Gestión de usuarios y estudiantes con roles (admin/estudiante)
- ✅ **Tests vocacionales completos** con preguntas dinámicas y cálculo de personalidad
- ✅ Sistema de sesiones de test con progreso y resultados detallados
- ✅ **API completa para tests**: iniciar, responder, finalizar y obtener resultados
- ✅ Panel de administración para gestión de preguntas
- ✅ Estadísticas y reportes de tests realizados
- ✅ Rate limiting, seguridad y validaciones
- ✅ PostgreSQL con migraciones automáticas
- ✅ Email SMTP para recuperación de contraseña

### Frontend
- ✅ Landing page profesional con diseño moderno
- ✅ Sistema de autenticación completo (login/registro/recuperación)
- ✅ **Test vocacional interactivo** con interfaz intuitiva y animaciones
- ✅ **Sistema de resultados** con análisis detallado de personalidad
- ✅ Dashboard completo con navegación sidebar
- ✅ **Panel de administración** para gestión de preguntas y usuarios
- ✅ **Tests públicos** (accesibles sin registro para demostración)
- ✅ Perfiles de usuario con configuración personal
- ✅ Diseño responsive y moderno con glassmorphism
- ✅ Componentes reutilizables y arquitectura modular

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

## Rutas de la Aplicación

### Públicas (sin autenticación):
- `/` - Landing page
- `/test` - Test vocacional público
- `/test/resultados/:id` - Resultados de test público

### Autenticación:
- `/auth/login` - Iniciar sesión
- `/auth/registro` - Registro de usuario
- `/auth/recuperar-password` - Recuperar contraseña
- `/auth/restablecer-password/:token` - Restablecer contraseña

### Dashboard (requiere autenticación):
- `/dashboard` - Dashboard principal
- `/dashboard/configuraciones` - Configuración de perfil
- `/dashboard/test` - Test vocacional
- `/dashboard/test-resultados` - Lista de resultados
- `/dashboard/test-resultados/:id` - Detalle de resultados

### Administración (requiere rol admin):
- `/dashboard/admin/preguntas` - Gestión de preguntas del test

### Funcionalidades del Test Vocacional
- **33 preguntas** con sistema de 5 opciones (escala Likert)
- **Cálculo automático** de personalidad basado en 4 tipos principales
- **Resultados detallados** con porcentajes y descripciones
- **Sistema de sesiones** para guardar progreso
- **Tests públicos** para demostración sin registro
- **Panel de administración** completo para gestión

## Algoritmo de Personalidad

El sistema utiliza un test de personalidad basado en la metodología **OEJTS (Orientation Educational Job Test System)**, inspirado en el modelo MBTI (Myers-Briggs Type Indicator) pero adaptado para orientación vocacional educativa.

### Estructura del Test
- **32 preguntas** principales (más 1 pregunta adicional opcional)
- **Escala Likert** de 5 puntos (1-5) para cada respuesta
- **4 dimensiones de personalidad** evaluadas
- **16 tipos de personalidad** resultantes

### Dimensiones de Personalidad

#### 1. Introversión vs Extraversión (IE)
**Valor base:** 30 puntos
**Preguntas:** 3, 7, 11, 15, 19, 23, 27, 31
**Fórmula:** `IE = 30 - Q3 - Q7 - Q11 + Q15 - Q19 + Q23 + Q27 - Q31`
- **Introvertido (I)**: IE ≤ 24
- **Extravertido (E)**: IE > 24

#### 2. Sensación vs Intuición (SN)
**Valor base:** 12 puntos
**Preguntas:** 4, 8, 12, 16, 20, 24, 28, 32
**Fórmula:** `SN = 12 + Q4 + Q8 + Q12 + Q16 + Q20 - Q24 - Q28 + Q32`
- **Sensorial (S)**: SN ≤ 24
- **Intuitivo (N)**: SN > 24

#### 3. Sentimiento vs Pensamiento (FT)
**Valor base:** 30 puntos
**Preguntas:** 2, 6, 10, 14, 18, 22, 26, 30
**Fórmula:** `FT = 30 - Q2 + Q6 + Q10 - Q14 - Q18 + Q22 - Q26 - Q30`
- **Sentimiento (F)**: FT ≤ 24
- **Pensamiento (T)**: FT > 24

#### 4. Juicio vs Percepción (JP)
**Valor base:** 18 puntos
**Preguntas:** 1, 5, 9, 13, 17, 21, 25, 29
**Fórmula:** `JP = 18 + Q1 + Q5 - Q9 + Q13 - Q17 + Q21 - Q25 + Q29`
- **Juicioso (J)**: JP ≤ 24
- **Perceptivo (P)**: JP > 24

### Cálculo del Tipo de Personalidad

El tipo se determina combinando las 4 letras según el umbral de 24 puntos:

```
Tipo = [E/I] + [N/S] + [T/F] + [P/J]
```

**Ejemplo:** Si IE=28, SN=20, FT=26, JP=22 → Tipo = "ENTP"

### Tipos de Personalidad Resultantes

1. **ENFP** - El Inspirador (17% población)
2. **ENFJ** - El Protagonista (2.5% población)
3. **ENTP** - El Debator (3.2% población)
4. **ENTJ** - El Comandante (1.8% población)
5. **ESFJ** - El Cónsul (12% población)
6. **ESFP** - El Animador (8.5% población)
7. **ESTP** - El Empresario (4.3% población)
8. **ESTJ** - El Ejecutivo (8.7% población)
9. **INFP** - El Mediador (4.4% población)
10. **INFJ** - El Abogado (1.5% población)
11. **INTP** - El Lógico (3.3% población)
12. **INTJ** - El Arquitecto (2.1% población)
13. **ISFJ** - El Defensor (13.8% población)
14. **ISFP** - El Aventurero (8.8% población)
15. **ISTP** - El Virtuoso (5.4% población)
16. **ISTJ** - El Inspector (11.6% población)

### Validación y Procesamiento

- **Validación:** Se requiere exactamente 32 respuestas para procesar resultados
- **Almacenamiento:** Resultados se guardan en tabla `sesiones_test`
- **Formato JSON:** Resultados se devuelven en formato estructurado con:
  - Puntuaciones numéricas por dimensión
  - Clasificación cualitativa (Introvertido/Extravertido, etc.)
  - Información completa del tipo de personalidad
  - Sugerencias de carreras y características

### Adaptación Vocacional

Cada tipo incluye:
- **Descripción detallada** del perfil psicológico
- **Fortalezas y debilidades** características
- **Carreras sugeridas** basadas en el tipo
- **Figuras famosas** con el mismo tipo
- **Porcentaje en población** general

## Estructura de la Base de Datos

### Tablas Principales:
- `usuarios`: Datos de autenticación y básicos
- `estudiantes`: Perfil extendido del estudiante (vinculado a usuarios)
- `roles`: Roles del sistema (admin, estudiante)
- `usuario_rol`: Relación many-to-many entre usuarios y roles

### Tablas de Tests Vocacionales:
- `preguntas`: Preguntas del test con opciones izquierda/derecha
- `tipos_personalidad`: Tipos de personalidad (4 tipos principales)
- `sesiones_test`: Sesiones de test realizadas por usuarios
- `respuestas`: Respuestas individuales a preguntas en sesiones
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

### Tests Vocacionales (`/api/test`)
- `GET /preguntas` - Obtener todas las preguntas activas
- `POST /iniciar` - Iniciar nueva sesión de test
- `POST /responder` - Guardar respuesta a pregunta
- `POST /finalizar/<id_sesion>` - Finalizar test y calcular resultados
- `GET /resultados/<id_sesion>` - Obtener resultados detallados
- `GET /mis-sesiones` - Obtener sesiones del usuario actual
- `POST /asociar-sesion` - Asociar sesión pública a usuario registrado
- `GET /tipos` - Obtener tipos de personalidad
- `GET /tipos/<codigo>` - Obtener tipo específico de personalidad
- `GET /estadisticas` - Estadísticas generales (admin)
- `GET /admin/sesiones` - Todas las sesiones (admin)
- `GET /admin/usuarios/<id>/sesiones` - Sesiones de usuario específico (admin)
- `GET /admin/preguntas` - Gestionar preguntas (admin)
- `POST /admin/preguntas` - Crear nueva pregunta (admin)
- `PUT /admin/preguntas/<id>` - Actualizar pregunta (admin)
- `DELETE /admin/preguntas/<id>` - Eliminar pregunta (admin)
- `PATCH /admin/preguntas/<id>/toggle` - Activar/desactivar pregunta (admin)

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
- Quasar Framework 2.0+
- Pinia (state management)
- Vue Router 4
- Axios (HTTP client)
- Diseño responsive con CSS Grid/Flexbox
- Animaciones CSS modernas y glassmorphism
- Componentes reutilizables con slots y composition functions

## Seguridad

- Passwords hasheados con Argon2
- JWT tokens con expiración
- Rate limiting en endpoints críticos
- CORS configurado
- Validación de inputs
- Bloqueo de cuenta por intentos fallidos
- Tokens de recuperación con expiración

## Próximas Funcionalidades

- [ ] Sistema de recomendaciones de carreras basado en personalidad
- [ ] Exportación de resultados en PDF
- [ ] Notificaciones por email de resultados
- [ ] Dashboard avanzado con gráficos de progreso
- [ ] API para integración con sistemas externos
- [ ] Múltiples idiomas (i18n)
- [ ] Tests adicionales (aptitudes, intereses, etc.)
- [ ] Sistema de feedback y mejora continua

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

## Deployment

### Variables de Producción
Para producción, asegúrate de configurar:
- `FLASK_ENV=production`
- `SECRET_KEY` segura y única
- `JWT_SECRET_KEY` segura y única
- Base de datos PostgreSQL dedicada
- SMTP configurado correctamente
- HTTPS habilitado
- Variables de entorno para URLs del frontend

### Comandos de Build
```bash
# Backend
pip install -r requirements.txt
flask db upgrade

# Frontend
npm install
npm run build
```

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## Licencia

Propietario - © 2024-2025 ElijHoy