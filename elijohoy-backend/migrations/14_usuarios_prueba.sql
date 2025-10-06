-- =============================================================
-- MIGRACIÓN 14: USUARIOS DE PRUEBA
-- =============================================================
-- Inserta usuarios de prueba para testing del sistema
-- Administrador y Alumno de ejemplo

-- Insertar roles si no existen
INSERT INTO roles (nombre, descripcion) VALUES
('administrador', 'Administrador del sistema'),
('alumno', 'Estudiante del sistema')
ON CONFLICT (nombre) DO NOTHING;

-- Insertar usuario administrador
INSERT INTO usuarios (email, password_hash, activo, creado_en, actualizado_en)
VALUES (
    'admin@elijohoy.com',
    '$2b$12$Fo7NPQZmiSBHjtnv5RjpPeoSGREtT8.2TX.ale1YFyDNuUiRpQecy', -- Admin123!
    true,
    NOW(),
    NOW()
) ON CONFLICT (email) DO NOTHING;

-- Insertar usuario alumno
INSERT INTO usuarios (email, password_hash, activo, creado_en, actualizado_en)
VALUES (
    'alumno@elijohoy.com',
    '$2b$12$fFT5kxjFyBDcj6B1RCR.xeP.sq/y4Bo8dB4GhM1Zd5nKVcLWmLcKe', -- Alumno123!
    true,
    NOW(),
    NOW()
) ON CONFLICT (email) DO NOTHING;

-- Insertar datos de alumno para el administrador
INSERT INTO alumnos (
    usuario_id,
    nombre,
    apellidos,
    edad,
    email,
    genero,
    creado_en,
    actualizado_en
)
SELECT
    u.id,
    'Administrador',
    'Sistema',
    30,
    'admin@elijohoy.com',
    'masculino',
    NOW(),
    NOW()
FROM usuarios u
WHERE u.email = 'admin@elijohoy.com'
ON CONFLICT (usuario_id) DO NOTHING;

-- Insertar datos de alumno para el usuario alumno
INSERT INTO alumnos (
    usuario_id,
    nombre,
    apellidos,
    edad,
    email,
    genero,
    ciudad,
    pais,
    creado_en,
    actualizado_en
)
SELECT
    u.id,
    'Juan',
    'Pérez',
    20,
    'alumno@elijohoy.com',
    'masculino',
    'Lima',
    'Perú',
    NOW(),
    NOW()
FROM usuarios u
WHERE u.email = 'alumno@elijohoy.com'
ON CONFLICT (usuario_id) DO NOTHING;

-- Asignar roles a los usuarios
INSERT INTO usuario_rol (usuario_id, rol_id)
SELECT u.id, r.id
FROM usuarios u
CROSS JOIN roles r
WHERE u.email = 'admin@elijohoy.com' AND r.nombre = 'administrador'
ON CONFLICT (usuario_id, rol_id) DO NOTHING;

INSERT INTO usuario_rol (usuario_id, rol_id)
SELECT u.id, r.id
FROM usuarios u
CROSS JOIN roles r
WHERE u.email = 'alumno@elijohoy.com' AND r.nombre = 'alumno'
ON CONFLICT (usuario_id, rol_id) DO NOTHING;

-- Verificación: Mostrar usuarios creados
DO $$
DECLARE
    usuario_record RECORD;
BEGIN
    RAISE NOTICE 'Usuarios de prueba creados:';
    FOR usuario_record IN
        SELECT
            u.email,
            array_agg(r.nombre) as roles,
            a.nombre,
            a.apellidos
        FROM usuarios u
        LEFT JOIN usuario_rol ur ON u.id = ur.usuario_id
        LEFT JOIN roles r ON ur.rol_id = r.id
        LEFT JOIN alumnos a ON u.id = a.usuario_id
        WHERE u.email IN ('admin@elijohoy.com', 'alumno@elijohoy.com')
        GROUP BY u.id, u.email, a.nombre, a.apellidos
    LOOP
        RAISE NOTICE 'Email: %, Roles: %, Nombre: % %',
            usuario_record.email,
            usuario_record.roles,
            usuario_record.nombre,
            usuario_record.apellidos;
    END LOOP;
END $$;