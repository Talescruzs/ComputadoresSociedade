SET @linha_nome := 'UFSM/Vale Machado - Faixa Nova';
SET @id_linha := (SELECT id_linha FROM linha WHERE nome=@linha_nome LIMIT 1);

-- Garantir paradas (idempotente)
INSERT INTO parada (nome, localizacao) SELECT 'UFSM','UFSM' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='UFSM');
INSERT INTO parada (nome, localizacao) SELECT 'AV RORAIMA','AV RORAIMA' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='AV RORAIMA');
INSERT INTO parada (nome, localizacao) SELECT 'ROD RS-287','ROD RS-287' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='ROD RS-287');
INSERT INTO parada (nome, localizacao) SELECT 'R PEDRO PEREIRA','R PEDRO PEREIRA' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='R PEDRO PEREIRA');
INSERT INTO parada (nome, localizacao) SELECT 'R GENERAL NETO','R GENERAL NETO' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='R GENERAL NETO');
INSERT INTO parada (nome, localizacao) SELECT 'R GUILHERME JOÃO FABRIN','R GUILHERME JOÃO FABRIN' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='R GUILHERME JOÃO FABRIN');
INSERT INTO parada (nome, localizacao) SELECT 'R ENGENHEIRO LUIZ BOLLICK','R ENGENHEIRO LUIZ BOLLICK' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='R ENGENHEIRO LUIZ BOLLICK');
INSERT INTO parada (nome, localizacao) SELECT 'R OTÁVIO ALVES DE OLIVEIRA','R OTÁVIO ALVES DE OLIVEIRA' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='R OTÁVIO ALVES DE OLIVEIRA');
INSERT INTO parada (nome, localizacao) SELECT 'R RIACHUELO','R RIACHUELO' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='R RIACHUELO');
INSERT INTO parada (nome, localizacao) SELECT 'R ÂNGELO UGLIONE','R ÂNGELO UGLIONE' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='R ÂNGELO UGLIONE');
INSERT INTO parada (nome, localizacao) SELECT 'R ANDRÉ MARQUES','R ANDRÉ MARQUES' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='R ANDRÉ MARQUES');
INSERT INTO parada (nome, localizacao) SELECT 'TERMINAL VALE MACHADO','TERMINAL VALE MACHADO' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='TERMINAL VALE MACHADO');

-- Associação na rota com ordem e ativa (0..12)
INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 0, 1 FROM parada p WHERE p.nome='UFSM' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=0);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 1, 1 FROM parada p WHERE p.nome='AV RORAIMA' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=1);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 2, 1 FROM parada p WHERE p.nome='ROD RS-287' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=2);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 3, 1 FROM parada p WHERE p.nome='R PEDRO PEREIRA' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=3);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 4, 1 FROM parada p WHERE p.nome='R GENERAL NETO' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=4);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 5, 1 FROM parada p WHERE p.nome='R GUILHERME JOÃO FABRIN' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=5);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 6, 1 FROM parada p WHERE p.nome='R ENGENHEIRO LUIZ BOLLICK' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=6);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 7, 1 FROM parada p WHERE p.nome='R OTÁVIO ALVES DE OLIVEIRA' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=7);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 8, 1 FROM parada p WHERE p.nome='R GENERAL NETO' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=8);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 9, 1 FROM parada p WHERE p.nome='R RIACHUELO' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=9);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 10, 1 FROM parada p WHERE p.nome='R ÂNGELO UGLIONE' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=10);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 11, 1 FROM parada p WHERE p.nome='R ANDRÉ MARQUES' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=11);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 12, 1 FROM parada p WHERE p.nome='TERMINAL VALE MACHADO' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=12);
