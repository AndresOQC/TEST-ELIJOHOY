-- Tabla de preguntas del test OEJTS
CREATE TABLE IF NOT EXISTS preguntas (
    id_pregunta INTEGER PRIMARY KEY,
    texto_izquierda VARCHAR(200) NOT NULL,
    texto_derecha VARCHAR(200) NOT NULL,
    dimension VARCHAR(2) NOT NULL CHECK (dimension IN ('IE', 'SN', 'FT', 'JP')),
    peso INTEGER NOT NULL CHECK (peso IN (-1, 1)),
    orden INTEGER NOT NULL UNIQUE,
    activa BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT chk_id_pregunta_rango CHECK (id_pregunta BETWEEN 1 AND 32)
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_preguntas_dimension ON preguntas(dimension);
CREATE INDEX IF NOT EXISTS idx_preguntas_orden ON preguntas(orden);
CREATE INDEX IF NOT EXISTS idx_preguntas_activa ON preguntas(activa);

-- Comentarios
COMMENT ON TABLE preguntas IS 'Catálogo de las 32 preguntas del test OEJTS';
COMMENT ON COLUMN preguntas.dimension IS 'IE=Intro/Extra, SN=Sens/Intui, FT=Feel/Think, JP=Judg/Perc';
COMMENT ON COLUMN preguntas.peso IS 'Peso en la fórmula: +1 o -1';
