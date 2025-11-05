INSERT INTO linha (nome) SELECT 'Bombeiros/UFSM - Faixa Velha' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM linha WHERE nome='Bombeiros/UFSM - Faixa Velha');

INSERT INTO linha (nome) SELECT 'Bombeiros/UFSM - Faixa Nova' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM linha WHERE nome='Bombeiros/UFSM - Faixa Nova');

INSERT INTO linha (nome) SELECT 'UFSM/Bombeiros - Faixa Nova' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM linha WHERE nome='UFSM/Bombeiros - Faixa Nova');

INSERT INTO linha (nome) SELECT 'UFSM/Bombeiros - Faixa Velha' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM linha WHERE nome='UFSM/Bombeiros - Faixa Velha');

INSERT INTO linha (nome) SELECT 'UFSM/TNeves' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM linha WHERE nome='UFSM/TNeves');

INSERT INTO linha (nome) SELECT 'TNeves/UFSM' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM linha WHERE nome='TNeves/UFSM');

INSERT INTO linha (nome) SELECT 'Vale Machado/UFSM - Faixa Velha' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM linha WHERE nome='Vale Machado/UFSM - Faixa Velha');

INSERT INTO linha (nome) SELECT 'Vale Machado/UFSM - Faixa Nova' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM linha WHERE nome='Vale Machado/UFSM - Faixa Nova');

INSERT INTO linha (nome) SELECT 'UFSM/Vale Machado - Faixa Velha' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM linha WHERE nome='UFSM/Vale Machado - Faixa Velha');

INSERT INTO linha (nome) SELECT 'UFSM/Vale Machado - Faixa Nova' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM linha WHERE nome='UFSM/Vale Machado - Faixa Nova');
