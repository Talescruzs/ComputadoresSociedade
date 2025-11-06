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
LEFT JOIN viagem v ON v.id_onibus = o.id_onibus
WHERE v.id_onibus IS NULL
ORDER BY o.id_onibus;

-- Primeira viagem por linha (ônibus ímpar do par)
INSERT INTO viagem (id_onibus, id_linha, data_hora_inicio)
SELECT
  b1.id_onibus,
  l.id_linha,
  TIMESTAMP(CURDATE(), '07:00:00') AS data_hora_inicio
FROM tmp_lines l
JOIN tmp_buses b1 ON b1.rn = (l.rn * 2) - 1
WHERE b1.id_onibus IS NOT NULL
  AND NOT EXISTS (
    SELECT 1 FROM viagem v
    WHERE v.id_onibus = b1.id_onibus AND v.id_linha = l.id_linha
  );

-- Segunda viagem por linha (ônibus par do par), com horário deslocado
INSERT INTO viagem (id_onibus, id_linha, data_hora_inicio)
SELECT
  b2.id_onibus,
  l.id_linha,
  TIMESTAMP(CURDATE(), '09:00:00') AS data_hora_inicio
FROM tmp_lines l
JOIN tmp_buses b2 ON b2.rn = (l.rn * 2)
WHERE b2.id_onibus IS NOT NULL
  AND NOT EXISTS (
    SELECT 1 FROM viagem v
    WHERE v.id_onibus = b2.id_onibus AND v.id_linha = l.id_linha
  );
