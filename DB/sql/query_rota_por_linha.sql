-- View com a rota completa das linhas (paradas ordenadas)
CREATE OR REPLACE VIEW vw_rota_por_linha AS
SELECT
  l.id_linha,
  l.nome AS linha_nome,
  r.ordem,
  p.id_parada,
  p.nome AS parada_nome,
  p.localizacao
FROM rota r
JOIN linha l   ON l.id_linha = r.id_linha
JOIN parada p  ON p.id_parada = r.id_parada;

-- Exemplos de consulta (opcionais):
-- 1) Rota completa de uma linha por ID (em ordem)
--    SET @linha_id := 1;
--    SELECT * FROM vw_rota_por_linha WHERE id_linha = @linha_id ORDER BY ordem;

-- 2) Rota completa de uma linha por nome (em ordem)
--    SET @linha_nome := 'Bombeiros/UFSM - Faixa Velha';
--    SELECT * FROM vw_rota_por_linha WHERE linha_nome = @linha_nome ORDER BY ordem;

-- 3) Todas as linhas com suas rotas (ordenadas)
--    SELECT * FROM vw_rota_por_linha ORDER BY id_linha, ordem, id_parada;
