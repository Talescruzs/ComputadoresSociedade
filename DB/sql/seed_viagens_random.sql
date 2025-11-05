-- Vincula cada ônibus a uma viagem em alguma linha que possua rota (>= 2 paradas).
-- Idempotente: não cria nova viagem se já existir uma para o ônibus.

-- Garante que exista ao menos uma linha elegível
SET @eligible_count := (
  SELECT COUNT(*) FROM (
    SELECT r.id_linha
    FROM rota r
    GROUP BY r.id_linha
    HAVING COUNT(*) >= 2
  ) t
);

-- Insere 1 viagem por ônibus, escolhendo uma linha elegível aleatória
INSERT INTO viagem (id_onibus, id_linha)
SELECT
  o.id_onibus,
  (
    SELECT l.id_linha
    FROM linha l
    WHERE l.id_linha IN (
      SELECT r.id_linha
      FROM rota r
      GROUP BY r.id_linha
      HAVING COUNT(*) >= 2
    )
    ORDER BY RAND()
    LIMIT 1
  ) AS id_linha
FROM onibus o
WHERE @eligible_count > 0
  AND NOT EXISTS (SELECT 1 FROM viagem v WHERE v.id_onibus = o.id_onibus);
