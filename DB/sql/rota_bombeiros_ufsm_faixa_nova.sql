SET @linha_nome := 'Bombeiros/UFSM - Faixa Nova';
SET @id_linha := (SELECT id_linha FROM linha WHERE nome=@linha_nome LIMIT 1);

INSERT INTO parada (nome, localizacao) SELECT 'R BARÃO DO TRIUNFO','R BARÃO DO TRIUNFO' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='R BARÃO DO TRIUNFO');
INSERT INTO parada (nome, localizacao) SELECT 'R CORONEL NIEDERAUER','R CORONEL NIEDERAUER' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='R CORONEL NIEDERAUER');
INSERT INTO parada (nome, localizacao) SELECT 'R DUQUE DE CAXIAS','R DUQUE DE CAXIAS' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='R DUQUE DE CAXIAS');
INSERT INTO parada (nome, localizacao) SELECT 'AV PRESIDENTE VARGAS','AV PRESIDENTE VARGAS' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='AV PRESIDENTE VARGAS');
INSERT INTO parada (nome, localizacao) SELECT 'R JOSÉ BONIFÁCIO','R JOSÉ BONIFÁCIO' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='R JOSÉ BONIFÁCIO');
INSERT INTO parada (nome, localizacao) SELECT 'R DO ACAMPAMENTO','R DO ACAMPAMENTO' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='R DO ACAMPAMENTO');
INSERT INTO parada (nome, localizacao) SELECT 'AV FERNANDO FERRARI','AV FERNANDO FERRARI' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='AV FERNANDO FERRARI');
INSERT INTO parada (nome, localizacao) SELECT 'R GENERAL NETO','R GENERAL NETO' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='R GENERAL NETO');
INSERT INTO parada (nome, localizacao) SELECT 'R PEDRO PEREIRA','R PEDRO PEREIRA' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='R PEDRO PEREIRA');
INSERT INTO parada (nome, localizacao) SELECT 'ROD RS-287','ROD RS-287' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='ROD RS-287');
INSERT INTO parada (nome, localizacao) SELECT 'AV RORAIMA','AV RORAIMA' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='AV RORAIMA');
INSERT INTO parada (nome, localizacao) SELECT 'UFSM','UFSM' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM parada WHERE nome='UFSM');

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
SELECT @id_linha, p.id_parada, 6, 1 FROM parada p WHERE p.nome='AV FERNANDO FERRARI' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=6);
INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 7, 1 FROM parada p WHERE p.nome='R GENERAL NETO' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=7);
INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 8, 1 FROM parada p WHERE p.nome='R PEDRO PEREIRA' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=8);
INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 9, 1 FROM parada p WHERE p.nome='ROD RS-287' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=9);
INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 10, 1 FROM parada p WHERE p.nome='AV RORAIMA' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=10);
INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa)
SELECT @id_linha, p.id_parada, 11, 1 FROM parada p WHERE p.nome='UFSM' AND @id_linha IS NOT NULL
AND NOT EXISTS (SELECT 1 FROM rota r WHERE r.id_linha=@id_linha AND r.id_parada=p.id_parada AND r.ordem=11);
