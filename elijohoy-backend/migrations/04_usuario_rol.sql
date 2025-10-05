-- Tabla de asociación usuario-rol (many-to-many)
CREATE TABLE IF NOT EXISTS usuario_rol (
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    rol_id INTEGER NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    asignado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (usuario_id, rol_id)
);