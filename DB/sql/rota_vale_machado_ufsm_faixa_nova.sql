SET @linha_nome := 'Vale Machado/UFSM - Faixa Nova';
SET @id_linha := (SELECT id_linha FROM linha WHERE nome=@linha_nome LIMIT 1);

-- Garantir paradas (idempotente)
INSERT INTO parada (nome, localizacao) SELECT 'R VALE MACHADO','R VALE MACHADO' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='R VALE MACHADO');
INSERT INTO parada (nome, localizacao) SELECT 'AV RIO BRANCO','AV RIO BRANCO' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='AV RIO BRANCO');
INSERT INTO parada (nome, localizacao) SELECT 'R DO ACAMPAMENTO','R DO ACAMPAMENTO' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='R DO ACAMPAMENTO');
INSERT INTO parada (nome, localizacao) SELECT 'AV FERNANDO FERRARI','AV FERNANDO FERRARI' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='AV FERNANDO FERRARI');
INSERT INTO parada (nome, localizacao) SELECT 'R GENERAL NETO','R GENERAL NETO' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='R GENERAL NETO');
INSERT INTO parada (nome, localizacao) SELECT 'R PEDRO PEREIRA','R PEDRO PEREIRA' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='R PEDRO PEREIRA');
INSERT INTO parada (nome, localizacao) SELECT 'ROD RS-287','ROD RS-287' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='ROD RS-287');
INSERT INTO parada (nome, localizacao) SELECT 'AV RORAIMA','AV RORAIMA' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='AV RORAIMA');
INSERT INTO parada (nome, localizacao) SELECT 'UFSM','UFSM' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='UFSM');

-- Associação na rota com ordem e ativa (0..8)
INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 0, 1 FROM parada p WHERE p.nome='R VALE MACHADO' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=0);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 1, 1 FROM parada p WHERE p.nome='AV RIO BRANCO' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=1);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 2, 1 FROM parada p WHERE p.nome='R DO ACAMPAMENTO' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=2);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 3, 1 FROM parada p WHERE p.nome='AV FERNANDO FERRARI' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=3);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 4, 1 FROM parada p WHERE p.nome='R GENERAL NETO' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=4);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 5, 1 FROM parada p WHERE p.nome='R PEDRO PEREIRA' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=5);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 6, 1 FROM parada p WHERE p.nome='ROD RS-287' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=6);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 7, 1 FROM parada p WHERE p.nome='AV RORAIMA' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=7);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 8, 1 FROM parada p WHERE p.nome='UFSM' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=8);
