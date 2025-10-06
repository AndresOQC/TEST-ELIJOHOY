-- =============================================================
-- FUNCIÓN: Calcular resultados del test OEJTS
-- =============================================================
CREATE OR REPLACE FUNCTION calcular_resultados_test(p_id_sesion INTEGER)
RETURNS TABLE (
    ie_score INTEGER,
    sn_score INTEGER,
    ft_score INTEGER,
    jp_score INTEGER,
    tipo VARCHAR(4)
) AS $$
DECLARE
    v_ie INTEGER := 30;
    v_sn INTEGER := 12;
    v_ft INTEGER := 30;
    v_jp INTEGER := 18;
    v_tipo VARCHAR(4);
    v_count INTEGER;
BEGIN
    -- Verificar que la sesión existe
    SELECT COUNT(*) INTO v_count
    FROM sesiones_test
    WHERE id_sesion = p_id_sesion;

    IF v_count = 0 THEN
        RAISE EXCEPTION 'Sesión no encontrada: %', p_id_sesion;
    END IF;

    -- Verificar que hay 32 respuestas
    SELECT COUNT(*) INTO v_count
    FROM respuestas
    WHERE id_sesion = p_id_sesion;

    IF v_count != 32 THEN
        RAISE EXCEPTION 'Sesión incompleta. Respuestas: %/32', v_count;
    END IF;

    -- Calcular IE (Introversión/Extraversión)
    -- IE = 30 - Q3 - Q7 - Q11 + Q15 - Q19 + Q23 + Q27 - Q31
    SELECT v_ie -
        (SELECT valor_respuesta FROM respuestas WHERE id_sesion = p_id_sesion AND id_pregunta = 3) -
        (SELECT valor_respuesta FROM respuestas WHERE id_sesion = p_id_sesion AND id_pregunta = 7) -
        (SELECT valor_respuesta FROM respuestas WHERE id_sesion = p_id_sesion AND id_pregunta = 11) +
        (SELECT valor_respuesta FROM respuestas WHERE id_sesion = p_id_sesion AND id_pregunta = 15) -
        (SELECT valor_respuesta FROM respuestas WHERE id_sesion = p_id_sesion AND id_pregunta = 19) +
        (SELECT valor_respuesta FROM respuestas WHERE id_sesion = p_id_sesion AND id_pregunta = 23) +
        (SELECT valor_respuesta FROM respuestas WHERE id_sesion = p_id_sesion AND id_pregunta = 27) -
        (SELECT valor_respuesta FROM respuestas WHERE id_sesion = p_id_sesion AND id_pregunta = 31)
    INTO v_ie;

    -- Calcular SN (Sensación/Intuición)
    -- SN = 12 + Q4 + Q8 + Q12 + Q16 + Q20 - Q24 - Q28 + Q32
    SELECT v_sn +
        (SELECT valor_respuesta FROM respuestas WHERE id_sesion = p_id_sesion AND id_pregunta = 4) +
        (SELECT valor_respuesta FROM respuestas WHERE id_sesion = p_id_sesion AND id_pregunta = 8) +
        (SELECT valor_respuesta FROM respuestas WHERE id_sesion = p_id_sesion AND id_pregunta = 12) +
        (SELECT valor_respuesta FROM respuestas WHERE id_sesion = p_id_sesion AND id_pregunta = 16) +
        (SELECT valor_respuesta FROM respuestas WHERE id_sesion = p_id_sesion AND id_pregunta = 20) -
        (SELECT valor_respuesta FROM respuestas WHERE id_sesion = p_id_sesion AND id_pregunta = 24) -
        (SELECT valor_respuesta FROM respuestas WHERE id_sesion = p_id_sesion AND id_pregunta = 28) +
        (SELECT valor_respuesta FROM respuestas WHERE id_sesion = p_id_sesion AND id_pregunta = 32)
    INTO v_sn;

    -- Calcular FT (Sentimiento/Pensamiento)
    -- FT = 30 - Q2 + Q6 + Q10 - Q14 - Q18 + Q22 - Q26 - Q30
    SELECT v_ft -
        (SELECT valor_respuesta FROM respuestas WHERE id_sesion = p_id_sesion AND id_pregunta = 2) +
        (SELECT valor_respuesta FROM respuestas WHERE id_sesion = p_id_sesion AND id_pregunta = 6) +
        (SELECT valor_respuesta FROM respuestas WHERE id_sesion = p_id_sesion AND id_pregunta = 10) -
        (SELECT valor_respuesta FROM respuestas WHERE id_sesion = p_id_sesion AND id_pregunta = 14) -
        (SELECT valor_respuesta FROM respuestas WHERE id_sesion = p_id_sesion AND id_pregunta = 18) +
        (SELECT valor_respuesta FROM respuestas WHERE id_sesion = p_id_sesion AND id_pregunta = 22) -
        (SELECT valor_respuesta FROM respuestas WHERE id_sesion = p_id_sesion AND id_pregunta = 26) -
        (SELECT valor_respuesta FROM respuestas WHERE id_sesion = p_id_sesion AND id_pregunta = 30)
    INTO v_ft;

    -- Calcular JP (Juicio/Percepción)
    -- JP = 18 + Q1 + Q5 - Q9 + Q13 - Q17 + Q21 - Q25 + Q29
    SELECT v_jp +
        (SELECT valor_respuesta FROM respuestas WHERE id_sesion = p_id_sesion AND id_pregunta = 1) +
        (SELECT valor_respuesta FROM respuestas WHERE id_sesion = p_id_sesion AND id_pregunta = 5) -
        (SELECT valor_respuesta FROM respuestas WHERE id_sesion = p_id_sesion AND id_pregunta = 9) +
        (SELECT valor_respuesta FROM respuestas WHERE id_sesion = p_id_sesion AND id_pregunta = 13) -
        (SELECT valor_respuesta FROM respuestas WHERE id_sesion = p_id_sesion AND id_pregunta = 17) +
        (SELECT valor_respuesta FROM respuestas WHERE id_sesion = p_id_sesion AND id_pregunta = 21) -
        (SELECT valor_respuesta FROM respuestas WHERE id_sesion = p_id_sesion AND id_pregunta = 25) +
        (SELECT valor_respuesta FROM respuestas WHERE id_sesion = p_id_sesion AND id_pregunta = 29)
    INTO v_jp;

    -- Determinar tipo de personalidad
    v_tipo := '';
    v_tipo := v_tipo || CASE WHEN v_ie > 24 THEN 'E' ELSE 'I' END;
    v_tipo := v_tipo || CASE WHEN v_sn > 24 THEN 'N' ELSE 'S' END;
    v_tipo := v_tipo || CASE WHEN v_ft > 24 THEN 'T' ELSE 'F' END;
    v_tipo := v_tipo || CASE WHEN v_jp > 24 THEN 'P' ELSE 'J' END;

    -- Actualizar sesión con resultados
    UPDATE sesiones_test
    SET resultado_ie = v_ie,
        resultado_sn = v_sn,
        resultado_ft = v_ft,
        resultado_jp = v_jp,
        tipo_personalidad = v_tipo,
        completado = TRUE,
        fecha_fin = (NOW() AT TIME ZONE 'UTC')
    WHERE id_sesion = p_id_sesion;

    -- Retornar resultados
    RETURN QUERY SELECT v_ie, v_sn, v_ft, v_jp, v_tipo;
END;
$$ LANGUAGE plpgsql;

-- =============================================================
-- FUNCIÓN: Obtener perfil completo de usuario
-- =============================================================
CREATE OR REPLACE FUNCTION obtener_perfil_usuario(p_id_sesion INTEGER)
RETURNS JSON AS $$
DECLARE
    v_resultado JSON;
BEGIN
    SELECT json_build_object(
        'sesion', json_build_object(
            'id_sesion', s.id_sesion,
            'fecha_inicio', s.fecha_inicio,
            'fecha_fin', s.fecha_fin,
            'tipo_personalidad', s.tipo_personalidad
        ),
        'puntuaciones', json_build_object(
            'IE', s.resultado_ie,
            'SN', s.resultado_sn,
            'FT', s.resultado_ft,
            'JP', s.resultado_jp
        ),
        'dimensiones', json_build_object(
            'extraversion_introversion', CASE WHEN s.resultado_ie > 24 THEN 'Extravertido' ELSE 'Introvertido' END,
            'intuicion_sensacion', CASE WHEN s.resultado_sn > 24 THEN 'Intuitivo' ELSE 'Sensorial' END,
            'pensamiento_sentimiento', CASE WHEN s.resultado_ft > 24 THEN 'Pensamiento' ELSE 'Sentimiento' END,
            'percepcion_juicio', CASE WHEN s.resultado_jp > 24 THEN 'Perceptivo' ELSE 'Juicioso' END
        ),
        'tipo', json_build_object(
            'codigo', t.codigo,
            'nombre', t.nombre,
            'descripcion_corta', t.descripcion_corta,
            'descripcion_completa', t.descripcion_completa,
            'fortalezas', t.fortalezas,
            'debilidades', t.debilidades,
            'carreras_sugeridas', t.carreras_sugeridas,
            'famosos_tipo', t.famosos_tipo,
            'porcentaje_poblacion', t.porcentaje_poblacion
        )
    ) INTO v_resultado
    FROM sesiones_test s
    LEFT JOIN tipos_personalidad t ON s.tipo_personalidad = t.codigo
    WHERE s.id_sesion = p_id_sesion;

    RETURN v_resultado;
END;
$$ LANGUAGE plpgsql;

-- =============================================================
-- FUNCIÓN: Validar sesión completa
-- =============================================================
CREATE OR REPLACE FUNCTION validar_sesion_completa(p_id_sesion INTEGER)
RETURNS BOOLEAN AS $$
DECLARE
    v_count INTEGER;
BEGIN
    SELECT COUNT(*)
    INTO v_count
    FROM respuestas
    WHERE id_sesion = p_id_sesion;

    RETURN v_count = 32;
END;
$$ LANGUAGE plpgsql;

-- =============================================================
-- FUNCIÓN: Generar token anónimo único
-- =============================================================
CREATE OR REPLACE FUNCTION generar_token_anonimo()
RETURNS VARCHAR(64) AS $$
DECLARE
    v_token VARCHAR(64);
    v_existe BOOLEAN;
BEGIN
    LOOP
        -- Generar token aleatorio
        v_token := encode(gen_random_bytes(32), 'hex');

        -- Verificar si ya existe
        SELECT EXISTS(
            SELECT 1 FROM sesiones_test WHERE token_anonimo = v_token
        ) INTO v_existe;

        EXIT WHEN NOT v_existe;
    END LOOP;

    RETURN v_token;
END;
$$ LANGUAGE plpgsql;

-- =============================================================
-- FUNCIÓN: Estadísticas generales del sistema
-- =============================================================
CREATE OR REPLACE FUNCTION estadisticas_sistema()
RETURNS JSON AS $$
DECLARE
    v_resultado JSON;
BEGIN
    SELECT json_build_object(
        'total_usuarios', (SELECT COUNT(*) FROM usuarios WHERE activo = TRUE),
        'total_tests_completados', (SELECT COUNT(*) FROM sesiones_test WHERE completado = TRUE),
        'tests_hoy', (SELECT COUNT(*) FROM sesiones_test WHERE DATE(fecha_inicio) = CURRENT_DATE),
        'tipo_mas_comun', (
            SELECT tipo_personalidad
            FROM sesiones_test
            WHERE completado = TRUE AND tipo_personalidad IS NOT NULL
            GROUP BY tipo_personalidad
            ORDER BY COUNT(*) DESC
            LIMIT 1
        ),
        'distribucion_tipos', (
            SELECT json_object_agg(tipo_personalidad, cantidad)
            FROM (
                SELECT tipo_personalidad, COUNT(*) as cantidad
                FROM sesiones_test
                WHERE completado = TRUE AND tipo_personalidad IS NOT NULL
                GROUP BY tipo_personalidad
                ORDER BY tipo_personalidad
            ) sub
        ),
        'promedio_tiempo_test', (
            SELECT AVG(EXTRACT(EPOCH FROM (fecha_fin - fecha_inicio)) / 60)::INTEGER
            FROM sesiones_test
            WHERE completado = TRUE AND fecha_fin IS NOT NULL
        )
    ) INTO v_resultado;

    RETURN v_resultado;
END;
$$ LANGUAGE plpgsql;

-- Comentarios
COMMENT ON FUNCTION calcular_resultados_test IS 'Calcula los resultados del test OEJTS y actualiza la sesión';
COMMENT ON FUNCTION obtener_perfil_usuario IS 'Obtiene el perfil completo de usuario con tipo de personalidad';
COMMENT ON FUNCTION validar_sesion_completa IS 'Verifica si una sesión tiene las 32 respuestas';
COMMENT ON FUNCTION generar_token_anonimo IS 'Genera un token único para sesiones anónimas';
COMMENT ON FUNCTION estadisticas_sistema IS 'Retorna estadísticas generales del sistema';
