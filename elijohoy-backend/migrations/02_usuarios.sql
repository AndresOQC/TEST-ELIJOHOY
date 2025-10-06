-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    activo BOOLEAN DEFAULT TRUE NOT NULL,
    email_verificado BOOLEAN DEFAULT TRUE NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultimo_login TIMESTAMP,
    intentos_login_fallidos INTEGER DEFAULT 0,
    bloqueado_hasta TIMESTAMP
);

-- Índice para email
CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email);

