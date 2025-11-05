-- View com as linhas que passam por cada parada (inclui ordem na rota)
CREATE OR REPLACE VIEW vw_linhas_por_parada AS
SELECT
  p.id_parada,
  p.nome AS parada_nome,
  l.id_linha,
  l.nome AS linha_nome,
  r.ordem
FROM rota r
JOIN parada p ON p.id_parada = r.id_parada
JOIN linha  l ON l.id_linha  = r.id_linha;

-- Exemplos de consulta (opcionais):
-- 1) Linhas que passam por uma parada por ID (ordenado pela ordem de passagem)
--    SET @parada_id := 10;
--    SELECT * FROM vw_linhas_por_parada WHERE id_parada = @parada_id ORDER BY ordem, linha_nome;

-- 2) Linhas que passam por uma parada por nome
--    SET @parada_nome := 'UFSM';
--    SELECT * FROM vw_linhas_por_parada WHERE parada_nome = @parada_nome ORDER BY ordem, linha_nome;

-- 3) Todas as paradas com suas linhas
--    SELECT * FROM vw_linhas_por_parada ORDER BY parada_nome, ordem, linha_nome;
