SET @linha_nome := 'Bombeiros/UFSM - Faixa Velha';
SET @id_linha := (SELECT id_linha FROM linha WHERE nome=@linha_nome LIMIT 1);

-- Paradas (garante existência por nome)
INSERT INTO parada (nome, localizacao) SELECT 'R BARÃO DO TRIUNFO','R BARÃO DO TRIUNFO' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='R BARÃO DO TRIUNFO');
INSERT INTO parada (nome, localizacao) SELECT 'R CORONEL NIEDERAUER','R CORONEL NIEDERAUER' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='R CORONEL NIEDERAUER');
INSERT INTO parada (nome, localizacao) SELECT 'R DUQUE DE CAXIAS','R DUQUE DE CAXIAS' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='R DUQUE DE CAXIAS');
INSERT INTO parada (nome, localizacao) SELECT 'AV PRESIDENTE VARGAS','AV PRESIDENTE VARGAS' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='AV PRESIDENTE VARGAS');
INSERT INTO parada (nome, localizacao) SELECT 'R JOSÉ BONIFÁCIO','R JOSÉ BONIFÁCIO' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='R JOSÉ BONIFÁCIO');
INSERT INTO parada (nome, localizacao) SELECT 'R DO ACAMPAMENTO','R DO ACAMPAMENTO' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='R DO ACAMPAMENTO');
INSERT INTO parada (nome, localizacao) SELECT 'AV NOSSA SENHORA MEDIANEIRA','AV NOSSA SENHORA MEDIANEIRA' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='AV NOSSA SENHORA MEDIANEIRA');
INSERT INTO parada (nome, localizacao) SELECT 'AV NOSSA SENHORA DAS DORES','AV NOSSA SENHORA DAS DORES' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='AV NOSSA SENHORA DAS DORES');
INSERT INTO parada (nome, localizacao) SELECT 'AV JOÃO LUIZ POZZOBON','AV JOÃO LUIZ POZZOBON' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='AV JOÃO LUIZ POZZOBON');
INSERT INTO parada (nome, localizacao) SELECT 'ROD RS-509','ROD RS-509' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='ROD RS-509');
INSERT INTO parada (nome, localizacao) SELECT 'ROD RS-509 - PISTA LATERAL','ROD RS-509 - PISTA LATERAL' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='ROD RS-509 - PISTA LATERAL');
INSERT INTO parada (nome, localizacao) SELECT 'AV RORAIMA','AV RORAIMA' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='AV RORAIMA');
INSERT INTO parada (nome, localizacao) SELECT 'UFSM','UFSM' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='UFSM');

-- Associação na rota com ordem e ativa
-- Helper macro-like
-- ordem 0..13 (observação: 'ROD RS-509' aparece duas vezes; ambas inserções são verificadas por ordem)
INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 0, 1 FROM parada p WHERE p.nome='R BARÃO DO TRIUNFO' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=0);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 1, 1 FROM parada p WHERE p.nome='R CORONEL NIEDERAUER' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=1);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 2, 1 FROM parada p WHERE p.nome='R DUQUE DE CAXIAS' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=2);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 3, 1 FROM parada p WHERE p.nome='AV PRESIDENTE VARGAS' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=3);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 4, 1 FROM parada p WHERE p.nome='R JOSÉ BONIFÁCIO' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=4);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 5, 1 FROM parada p WHERE p.nome='R DO ACAMPAMENTO' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=5);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 6, 1 FROM parada p WHERE p.nome='AV NOSSA SENHORA MEDIANEIRA' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=6);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 7, 1 FROM parada p WHERE p.nome='AV NOSSA SENHORA DAS DORES' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=7);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 8, 1 FROM parada p WHERE p.nome='AV JOÃO LUIZ POZZOBON' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=8);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 9, 1 FROM parada p WHERE p.nome='ROD RS-509' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=9);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 10, 1 FROM parada p WHERE p.nome='ROD RS-509 - PISTA LATERAL' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=10);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 11, 1 FROM parada p WHERE p.nome='ROD RS-509' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=11);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 12, 1 FROM parada p WHERE p.nome='AV RORAIMA' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=12);

INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 13, 1 FROM parada p WHERE p.nome='UFSM' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=13);
