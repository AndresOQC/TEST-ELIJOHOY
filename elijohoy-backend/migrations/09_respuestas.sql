-- Tabla de respuestas individuales
CREATE TABLE IF NOT EXISTS respuestas (
    id_respuesta SERIAL PRIMARY KEY,
    id_sesion INTEGER NOT NULL,
    id_pregunta INTEGER NOT NULL,
    valor_respuesta INTEGER NOT NULL CHECK (valor_respuesta BETWEEN 1 AND 5),
    tiempo_respuesta INTEGER NULL,
    fecha_respuesta TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_respuestas_sesion
        FOREIGN KEY (id_sesion)
        REFERENCES sesiones_test(id_sesion)
        ON DELETE CASCADE,

    CONSTRAINT fk_respuestas_pregunta
        FOREIGN KEY (id_pregunta)
        REFERENCES preguntas(id_pregunta)
        ON DELETE RESTRICT,

    CONSTRAINT uk_sesion_pregunta UNIQUE (id_sesion, id_pregunta),
    CONSTRAINT chk_tiempo_respuesta CHECK (tiempo_respuesta IS NULL OR tiempo_respuesta >= 0)
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_respuestas_sesion ON respuestas(id_sesion);
CREATE INDEX IF NOT EXISTS idx_respuestas_pregunta ON respuestas(id_pregunta);
CREATE INDEX IF NOT EXISTS idx_respuestas_fecha ON respuestas(fecha_respuesta);

-- Comentarios
COMMENT ON TABLE respuestas IS 'Almacena cada respuesta individual del test';
COMMENT ON COLUMN respuestas.valor_respuesta IS 'Valor de 1 a 5: 1=totalmente izquierda, 5=totalmente derecha';
COMMENT ON COLUMN respuestas.tiempo_respuesta IS 'Tiempo en segundos que tomó responder';
