-- Tabla de roles
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar roles por defecto
INSERT INTO roles (nombre, descripcion)
VALUES
    ('admin', 'Administrador del sistema'),
    ('estudiante', 'Estudiante del sistema')
ON CONFLICT (nombre) DO NOTHING;