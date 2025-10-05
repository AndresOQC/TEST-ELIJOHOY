-- Tabla unificada de tokens (JWT y recuperación)
CREATE TABLE IF NOT EXISTS tokens (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    jti VARCHAR(120) UNIQUE NOT NULL,  -- JWT ID o token de recuperación
    tipo VARCHAR(20) NOT NULL,         -- 'access', 'refresh', 'password_reset'
    
    -- Timestamps
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    fecha_expiracion TIMESTAMP NOT NULL,
    
    -- Estado
    revocado BOOLEAN DEFAULT FALSE NOT NULL
);

-- Índices para tokens
CREATE INDEX IF NOT EXISTS idx_tokens_jti ON tokens(jti);
CREATE INDEX IF NOT EXISTS idx_tokens_tipo ON tokens(tipo);
CREATE INDEX IF NOT EXISTS idx_tokens_usuario_id ON tokens(usuario_id);
CREATE INDEX IF NOT EXISTS idx_tokens_revocado ON tokens(revocado);

-- Comentarios
COMMENT ON TABLE tokens IS 'Tokens JWT para autenticación';
COMMENT ON COLUMN tokens.jti IS 'JWT ID único';
COMMENT ON COLUMN tokens.tipo IS 'Tipo de token: access, refresh, password_reset';
COMMENT ON COLUMN tokens.revocado IS 'Indica si el token fue revocado';