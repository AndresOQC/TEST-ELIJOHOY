-- Eliminada tabla estudiantes incompleta
CREATE TABLE IF NOT EXISTS alumnos (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER UNIQUE NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    edad INTEGER NOT NULL,
    genero VARCHAR(20),
    email VARCHAR(120) UNIQUE NOT NULL,
    ciudad VARCHAR(100),
    pais VARCHAR(100),
    institucion_educativa VARCHAR(200),
    grado VARCHAR(50),
    seccion VARCHAR(50),
    turno VARCHAR(50),
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);