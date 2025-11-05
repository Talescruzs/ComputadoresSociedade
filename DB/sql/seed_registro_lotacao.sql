-- Cria registros em 'registro_lotacao' para as viagens existentes,
-- usando pares de paradas consecutivas da 'rota' da respectiva linha
-- e uma data/hora coerente com a ordem (incremento de minutos).
-- Idempotente: não insere se já existir o mesmo (viagem, origem, destino).

INSERT INTO registro_lotacao (id_viagem, id_parada_origem, id_parada_destino, data_hora, qtd_pessoas, id_parada)
SELECT
  v.id_viagem,
  r1.id_parada AS id_parada_origem,
  r2.id_parada AS id_parada_destino,
  -- Base de tempo: início da viagem + 7 minutos por segmento (ordem)
  DATE_ADD(
    COALESCE(v.data_hora_inicio, NOW()),
    INTERVAL (r1.ordem * 7) MINUTE
  ) AS data_hora,
  -- Lotação: maior em horários de pico (7-9h e 17-19h)
  CAST(
    CASE
      WHEN HOUR(DATE_ADD(COALESCE(v.data_hora_inicio, NOW()), INTERVAL (r1.ordem * 7) MINUTE)) BETWEEN 7 AND 9
        OR HOUR(DATE_ADD(COALESCE(v.data_hora_inicio, NOW()), INTERVAL (r1.ordem * 7) MINUTE)) BETWEEN 17 AND 19
      THEN 30 + (RAND() * 30)  -- pico: 30..60
      ELSE 10 + (RAND() * 25)  -- normal: 10..35
    END AS UNSIGNED
  ) AS qtd_pessoas,
  r2.id_parada AS id_parada  -- preenche coluna legada com o destino
FROM viagem v
JOIN rota r1 ON r1.id_linha = v.id_linha
JOIN rota r2 ON r2.id_linha = v.id_linha AND r2.ordem = r1.ordem + 1
LEFT JOIN registro_lotacao rl
  ON rl.id_viagem = v.id_viagem
 AND rl.id_parada_origem = r1.id_parada
 AND rl.id_parada_destino = r2.id_parada
WHERE rl.id_lotacao IS NULL
  AND (r1.esta_ativa IS NULL OR r1.esta_ativa = 1)
  AND (r2.esta_ativa IS NULL OR r2.esta_ativa = 1);
