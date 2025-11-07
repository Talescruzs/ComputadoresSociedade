-- Seed determinístico: cria 2 viagens por linha (cada uma com um ônibus distinto).
-- Idempotente por par (id_onibus, id_linha). Define data_hora_inicio (NOT NULL).

-- Linhas elegíveis: possuem rota com pelo menos 2 paradas
DROP TEMPORARY TABLE IF EXISTS tmp_lines;
SET @r := 0;
CREATE TEMPORARY TABLE tmp_lines AS
SELECT t.id_linha, (@r := @r + 1) AS rn
FROM (
  SELECT l.id_linha
  FROM linha l
  WHERE l.id_linha IN (
    SELECT r.id_linha
    FROM rota r
    GROUP BY r.id_linha
    HAVING COUNT(*) >= 2
  )
  ORDER BY l.id_linha
) AS t;

-- Ônibus disponíveis (sem viagem ainda), ordenados por id
DROP TEMPORARY TABLE IF EXISTS tmp_buses;
SET @b := 0;
CREATE TEMPORARY TABLE tmp_buses AS
SELECT o.id_onibus, (@b := @b + 1) AS rn
FROM onibus o
ORDER BY o.id_onibus;

SET @bus_count := (SELECT COUNT(*) FROM tmp_buses);

-- Gera horas de 06 até 19 (inclusive) sem CTE (compatível com MySQL < 8)
INSERT INTO viagem (id_onibus, id_linha, data_hora_inicio)
SELECT
  b.id_onibus,
  l.id_linha,
  TIMESTAMP(CURDATE(), CONCAT(LPAD(h.h,2,'0'),':00:00')) AS data_hora_inicio
FROM tmp_lines l
JOIN (
  SELECT 6 AS h UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9
  UNION ALL SELECT 10 UNION ALL SELECT 11 UNION ALL SELECT 12 UNION ALL SELECT 13
  UNION ALL SELECT 14 UNION ALL SELECT 15 UNION ALL SELECT 16 UNION ALL SELECT 17
  UNION ALL SELECT 18 UNION ALL SELECT 19
) AS h
JOIN tmp_buses b
  ON b.rn = ((l.rn + h.h - 6) % @bus_count) + 1
WHERE NOT EXISTS (
  SELECT 1
  FROM viagem v
  WHERE v.id_onibus = b.id_onibus
    AND v.id_linha = l.id_linha
    AND v.data_hora_inicio = TIMESTAMP(CURDATE(), CONCAT(LPAD(h.h,2,'0'),':00:00'))
);
