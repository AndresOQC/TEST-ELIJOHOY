-- ============================================================================
-- INSERCIÓN DE PREGUNTAS DEL TEST DE PERSONALIDAD OEJTS
-- ============================================================================
-- Este archivo contiene las 32 preguntas del test de personalidad basado en
-- el modelo de indicadores de tipo Myers-Briggs (MBTI)
-- 
-- Dimensiones:
--   IE = Introversión/Extraversión
--   SN = Sensación/Intuición  
--   FT = Sentimiento/Pensamiento
--   JP = Juicio/Percepción
-- ============================================================================

INSERT INTO preguntas (id_pregunta, texto_izquierda, texto_derecha, dimension, peso, orden) 
SELECT t.* FROM (VALUES
-- Dimensión JP (Juicio/Percepción)
(1, 'Hace listas de tareas', 'Confía en su memoria', 'JP', 1, 1),
(5, 'Mantiene su cuarto limpio y ordenado', 'Deja las cosas donde sea', 'JP', 1, 5),
(9, 'Desorganizado y caótico', 'Organizado y estructurado', 'JP', -1, 9),
(13, 'Planea con mucha anticipación', 'Planea a último minuto', 'JP', 1, 13),
(17, 'Mantiene sus opciones abiertas', 'Se compromete con decisiones', 'JP', -1, 17),
(21, 'Hace el trabajo de inmediato', 'Tiende a procrastinar', 'JP', 1, 21),
(25, 'Prefiere improvisar', 'Prefiere prepararse', 'JP', -1, 25),
(29, 'Trabaja duro y con dedicación', 'Juega duro y se divierte', 'JP', 1, 29),

-- Dimensión FT (Sentimiento/Pensamiento)
(2, 'Escéptico y cuestionador', 'Quiere creer en las personas', 'FT', -1, 2),
(6, 'Piensa que "robótico" es un insulto', 'Aspira a tener una mente mecánica', 'FT', 1, 6),
(10, 'Se lastima fácilmente', 'Tiene piel gruesa', 'FT', 1, 10),
(14, 'Quiere el respeto de la gente', 'Quiere su amor y cariño', 'FT', -1, 14),
(18, 'Quiere ser bueno arreglando cosas', 'Quiere ser bueno ayudando personas', 'FT', -1, 18),
(22, 'Sigue su corazón', 'Sigue su cabeza', 'FT', 1, 22),
(26, 'Basa la moralidad en la justicia', 'Basa la moralidad en la compasión', 'FT', -1, 26),
(30, 'Incómodo con las emociones', 'Valora las emociones', 'FT', -1, 30),

-- Dimensión IE (Introversión/Extraversión)
(3, 'Se aburre estando solo', 'Necesita tiempo a solas', 'IE', -1, 3),
(7, 'Energético y activo', 'Tranquilo y calmado', 'IE', -1, 7),
(11, 'Trabaja mejor en grupos', 'Trabaja mejor solo', 'IE', -1, 11),
(15, 'Se agota en fiestas', 'Se energiza en fiestas', 'IE', 1, 15),
(19, 'Habla más de lo que escucha', 'Escucha más de lo que habla', 'IE', -1, 19),
(23, 'Prefiere quedarse en casa', 'Sale a la ciudad con frecuencia', 'IE', 1, 23),
(27, 'Le cuesta gritar muy fuerte', 'Gritar a otros cuando están lejos viene naturalmente', 'IE', 1, 27),
(31, 'Le gusta actuar frente a otras personas', 'Evita hablar en público', 'IE', -1, 31),

-- Dimensión SN (Sensación/Intuición)
(4, 'Acepta las cosas como son', 'Insatisfecho con cómo son las cosas', 'SN', 1, 4),
(8, 'Prefiere exámenes de opción múltiple', 'Prefiere respuestas de ensayo', 'SN', 1, 8),
(12, 'Enfocado en el presente', 'Enfocado en el futuro', 'SN', 1, 12),
(16, 'Prefiere encajar con el grupo', 'Prefiere sobresalir y destacar', 'SN', 1, 16),
(20, 'Al describir un evento, dice qué pasó', 'Al describir un evento, dice qué significó', 'SN', 1, 20),
(24, 'Quiere la visión general', 'Quiere conocer los detalles', 'SN', -1, 24),
(28, 'Teórico y conceptual', 'Empírico y práctico', 'SN', -1, 28),
(32, 'Le gusta saber "quién", "qué", "cuándo"', 'Le gusta saber "por qué"', 'SN', 1, 32)
) AS t(id_pregunta, texto_izquierda, texto_derecha, dimension, peso, orden)
WHERE NOT EXISTS (SELECT 1 FROM preguntas WHERE id_pregunta = t.id_pregunta);

