SET @linha_nome := 'Vale Machado/UFSM - Faixa Velha';
SET @id_linha := (SELECT id_linha FROM linha WHERE nome=@linha_nome LIMIT 1);

-- Garantir paradas (idempotente)
INSERT INTO parada (nome, localizacao) SELECT 'R VALE MACHADO','R VALE MACHADO' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='R VALE MACHADO');
INSERT INTO parada (nome, localizacao) SELECT 'AV RIO BRANCO','AV RIO BRANCO' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='AV RIO BRANCO');
INSERT INTO parada (nome, localizacao) SELECT 'R DO ACAMPAMENTO','R DO ACAMPAMENTO' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='R DO ACAMPAMENTO');
INSERT INTO parada (nome, localizacao) SELECT 'AV NOSSA SENHORA MEDIANEIRA','AV NOSSA SENHORA MEDIANEIRA' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='AV NOSSA SENHORA MEDIANEIRA');
INSERT INTO parada (nome, localizacao) SELECT 'AV NOSSA SENHORA DAS DORES','AV NOSSA SENHORA DAS DORES' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='AV NOSSA SENHORA DAS DORES');
INSERT INTO parada (nome, localizacao) SELECT 'AV JOÃO LUIZ POZZOBON','AV JOÃO LUIZ POZZOBON' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='AV JOÃO LUIZ POZZOBON');
INSERT INTO parada (nome, localizacao) SELECT 'ROD RS-509','ROD RS-509' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='ROD RS-509');
INSERT INTO parada (nome, localizacao) SELECT 'ROD RS-509 - PISTA LATERAL','ROD RS-509 - PISTA LATERAL' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='ROD RS-509 - PISTA LATERAL');
INSERT INTO parada (nome, localizacao) SELECT 'AV RORAIMA','AV RORAIMA' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='AV RORAIMA');
INSERT INTO parada (nome, localizacao) SELECT 'UFSM','UFSM' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='UFSM');

-- Associação na rota com ordem e ativa (0..10)
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
SELECT @id_linha, p.id_parada, 3, 1 FROM parada p WHERE p.nome='AV NOSSA SENHORA MEDIANEIRA' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=3);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 4, 1 FROM parada p WHERE p.nome='AV NOSSA SENHORA DAS DORES' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=4);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 5, 1 FROM parada p WHERE p.nome='AV JOÃO LUIZ POZZOBON' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=5);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 6, 1 FROM parada p WHERE p.nome='ROD RS-509' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=6);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 7, 1 FROM parada p WHERE p.nome='ROD RS-509 - PISTA LATERAL' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=7);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 8, 1 FROM parada p WHERE p.nome='ROD RS-509' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=8);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 9, 1 FROM parada p WHERE p.nome='AV RORAIMA' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=9);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 10, 1 FROM parada p WHERE p.nome='UFSM' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=10);
