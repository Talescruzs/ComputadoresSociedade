-- Total de embarques por parada (diferença positiva de ocupação entre registros consecutivos da mesma viagem)
SELECT 
  p.id_parada,
  p.nome AS parada_nome,
  COALESCE(SUM(t.embarques),0) AS pessoas_total
FROM parada p
LEFT JOIN (
  SELECT 
    rl.id_parada_origem AS id_parada_origem,
    GREATEST(
      rl.qtd_pessoas - COALESCE((
        SELECT rl2.qtd_pessoas
        FROM registro_lotacao rl2
        WHERE rl2.id_viagem = rl.id_viagem
          AND rl2.data_hora < rl.data_hora
        ORDER BY rl2.data_hora DESC, rl2.id_lotacao DESC
        LIMIT 1
      ),0),
    0) AS embarques
  FROM registro_lotacao rl
) t ON t.id_parada_origem = p.id_parada
GROUP BY p.id_parada, p.nome
ORDER BY p.nome;

-- Observação:
-- Se a ocupação diminui ou permanece igual, considera-se 0 embarques.
-- O primeiro registro de cada viagem conta todos os ocupantes como embarques naquela parada.
