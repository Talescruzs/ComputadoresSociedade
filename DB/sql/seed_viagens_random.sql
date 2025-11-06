-- Seed determinístico: cria 1 viagem por par (ônibus, linha elegível) na ordem dos IDs.
-- Sem aleatoriedade. Garante data_hora_inicio (NOT NULL) e idempotência.

-- Linhas elegíveis: possuem rota com pelo menos 2 paradas
DROP TEMPORARY TABLE IF EXISTS tmp_lines;
SET @r2 := 0;
CREATE TEMPORARY TABLE tmp_lines AS
SELECT t.id_linha, (@r2 := @r2 + 1) AS rn
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

-- Ônibus ordenados por id
DROP TEMPORARY TABLE IF EXISTS tmp_buses;
SET @r1 := 0;
CREATE TEMPORARY TABLE tmp_buses AS
SELECT o.id_onibus, (@r1 := @r1 + 1) AS rn
FROM (
  SELECT @r1 := 0
) vars, onibus o
ORDER BY o.id_onibus;

-- Inserir 1 viagem por par (ônibus, linha) de mesmo índice (rn), até o mínimo entre as contagens
INSERT INTO viagem (id_onibus, id_linha, data_hora_inicio)
SELECT
  b.id_onibus,
  l.id_linha,
  NOW() AS data_hora_inicio
FROM tmp_buses b
JOIN tmp_lines l USING (rn)
WHERE NOT EXISTS (SELECT 1 FROM viagem v WHERE v.id_onibus = b.id_onibus)
  AND NOT EXISTS (SELECT 1 FROM viagem v2 WHERE v2.id_linha = l.id_linha);
