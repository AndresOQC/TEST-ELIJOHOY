-- Tabla de sesiones de test
CREATE TABLE IF NOT EXISTS sesiones_test (
    id_sesion SERIAL PRIMARY KEY,
    id_usuario INTEGER NULL,
    token_anonimo VARCHAR(64) UNIQUE,
    fecha_inicio TIMESTAMP NOT NULL DEFAULT NOW(),
    fecha_fin TIMESTAMP NULL,
    completado BOOLEAN NOT NULL DEFAULT FALSE,
    resultado_ie INTEGER NULL,
    resultado_sn INTEGER NULL,
    resultado_ft INTEGER NULL,
    resultado_jp INTEGER NULL,
    tipo_personalidad VARCHAR(4) NULL,
    ip_address VARCHAR(45) NULL,
    user_agent TEXT NULL,

    CONSTRAINT fk_sesiones_usuario
        FOREIGN KEY (id_usuario)
        REFERENCES usuarios(id)
        ON DELETE SET NULL,

    CONSTRAINT fk_sesiones_tipo
        FOREIGN KEY (tipo_personalidad)
        REFERENCES tipos_personalidad(codigo)
        ON DELETE SET NULL,

    CONSTRAINT chk_resultado_ie CHECK (resultado_ie IS NULL OR resultado_ie BETWEEN 8 AND 38),
    CONSTRAINT chk_resultado_sn CHECK (resultado_sn IS NULL OR resultado_sn BETWEEN 4 AND 44),
    CONSTRAINT chk_resultado_ft CHECK (resultado_ft IS NULL OR resultado_ft BETWEEN 8 AND 38),
    CONSTRAINT chk_resultado_jp CHECK (resultado_jp IS NULL OR resultado_jp BETWEEN 10 AND 40),
    CONSTRAINT chk_fecha_fin CHECK (fecha_fin IS NULL OR fecha_fin >= fecha_inicio),
    CONSTRAINT chk_completado_resultados CHECK (
        (completado = FALSE AND tipo_personalidad IS NULL) OR
        (completado = TRUE AND tipo_personalidad IS NOT NULL)
    )
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_sesiones_usuario ON sesiones_test(id_usuario);
CREATE INDEX IF NOT EXISTS idx_sesiones_token ON sesiones_test(token_anonimo);
CREATE INDEX IF NOT EXISTS idx_sesiones_tipo ON sesiones_test(tipo_personalidad);
CREATE INDEX IF NOT EXISTS idx_sesiones_fecha_inicio ON sesiones_test(fecha_inicio);
CREATE INDEX IF NOT EXISTS idx_sesiones_completado ON sesiones_test(completado);
CREATE INDEX IF NOT EXISTS idx_sesiones_usuario_completado ON sesiones_test(id_usuario, completado);

-- Comentarios
COMMENT ON TABLE sesiones_test IS 'Registra cada intento de test, anónimo o de usuario';
COMMENT ON COLUMN sesiones_test.token_anonimo IS 'Token único para sesiones anónimas, se mantiene tras registro';
COMMENT ON COLUMN sesiones_test.resultado_ie IS 'Puntuación IE: 8-38, punto de corte 24';
COMMENT ON COLUMN sesiones_test.resultado_sn IS 'Puntuación SN: 4-44, punto de corte 24';
COMMENT ON COLUMN sesiones_test.resultado_ft IS 'Puntuación FT: 8-38, punto de corte 24';
COMMENT ON COLUMN sesiones_test.resultado_jp IS 'Puntuación JP: 10-40, punto de corte 24';
