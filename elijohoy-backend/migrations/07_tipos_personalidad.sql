-- Tabla de tipos de personalidad
CREATE TABLE IF NOT EXISTS tipos_personalidad (
    codigo VARCHAR(4) PRIMARY KEY CHECK (
        codigo ~ '^[IE][SN][FT][JP]$'
    ),
    nombre VARCHAR(100) NOT NULL,
    descripcion_corta TEXT NOT NULL,
    descripcion_completa TEXT NOT NULL,
    fortalezas TEXT,
    debilidades TEXT,
    carreras_sugeridas TEXT,
    famosos_tipo TEXT,
    porcentaje_poblacion DECIMAL(4,2),

    CONSTRAINT chk_codigo_formato CHECK (
        codigo ~ '^[IE][SN][FT][JP]$'
    )
);

-- Comentarios
COMMENT ON TABLE tipos_personalidad IS 'Catálogo de los 16 tipos de personalidad MBTI';
COMMENT ON COLUMN tipos_personalidad.porcentaje_poblacion IS 'Porcentaje de la población mundial con este tipo';
