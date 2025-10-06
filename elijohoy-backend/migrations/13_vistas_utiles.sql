-- =============================================================
-- VISTA: Sesiones completas con información de usuario y tipo
-- =============================================================
CREATE OR REPLACE VIEW v_sesiones_completas AS
SELECT
    s.id_sesion,
    s.id_usuario,
    CONCAT(a.nombre, ' ', a.apellidos) as nombre_completo,
    u.email,
    s.fecha_inicio,
    s.fecha_fin,
    EXTRACT(EPOCH FROM (s.fecha_fin - s.fecha_inicio)) / 60 AS duracion_minutos,
    s.tipo_personalidad,
    s.resultado_ie,
    s.resultado_sn,
    s.resultado_ft,
    s.resultado_jp,
    t.nombre AS nombre_tipo,
    t.descripcion_corta
FROM sesiones_test s
LEFT JOIN usuarios u ON s.id_usuario = u.id
LEFT JOIN alumnos a ON u.id = a.usuario_id
LEFT JOIN tipos_personalidad t ON s.tipo_personalidad = t.codigo
WHERE s.completado = TRUE;

COMMENT ON VIEW v_sesiones_completas IS 'Vista consolidada de sesiones completadas con datos de usuario y tipo';

-- =============================================================
-- VISTA: Distribución de tipos de personalidad
-- =============================================================
CREATE OR REPLACE VIEW v_distribucion_tipos AS
SELECT
    t.codigo,
    t.nombre,
    COUNT(s.id_sesion) as cantidad_tests,
    ROUND(COUNT(s.id_sesion) * 100.0 / NULLIF((SELECT COUNT(*) FROM sesiones_test WHERE completado = TRUE), 0), 2) as porcentaje_muestra,
    t.porcentaje_poblacion as porcentaje_teorico
FROM tipos_personalidad t
LEFT JOIN sesiones_test s ON t.codigo = s.tipo_personalidad AND s.completado = TRUE
GROUP BY t.codigo, t.nombre, t.porcentaje_poblacion
ORDER BY cantidad_tests DESC;

COMMENT ON VIEW v_distribucion_tipos IS 'Distribución de tipos de personalidad en la muestra vs población general';

-- =============================================================
-- VISTA: Estadísticas por usuario
-- =============================================================
CREATE OR REPLACE VIEW v_estadisticas_usuario AS
SELECT
    u.id as id_usuario,
    CONCAT(a.nombre, ' ', a.apellidos) as nombre_completo,
    u.email,
    COUNT(s.id_sesion) as tests_realizados,
    MAX(s.fecha_fin) as ultimo_test,
    MODE() WITHIN GROUP (ORDER BY s.tipo_personalidad) as tipo_mas_frecuente
FROM usuarios u
LEFT JOIN alumnos a ON u.id = a.usuario_id
LEFT JOIN sesiones_test s ON u.id = s.id_usuario AND s.completado = TRUE
GROUP BY u.id, a.nombre, a.apellidos, u.email;

COMMENT ON VIEW v_estadisticas_usuario IS 'Estadísticas agregadas por usuario';
