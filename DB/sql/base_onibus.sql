INSERT INTO onibus (placa, capacidade, data_ultima_manutencao)
SELECT 'ABC-1234', 50, '2024-09-15 10:00:00' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM onibus WHERE placa = 'ABC-1234');

INSERT INTO onibus (placa, capacidade, data_ultima_manutencao)
SELECT 'DEF-5678', 45, '2024-09-20 14:30:00' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM onibus WHERE placa = 'DEF-5678');

INSERT INTO onibus (placa, capacidade, data_ultima_manutencao)
SELECT 'GHI-9012', 60, '2024-10-01 09:00:00' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM onibus WHERE placa = 'GHI-9012');

INSERT INTO onibus (placa, capacidade, data_ultima_manutencao)
SELECT 'JKL-3456', 55, '2024-10-05 08:15:00' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM onibus WHERE placa = 'JKL-3456');

INSERT INTO onibus (placa, capacidade, data_ultima_manutencao)
SELECT 'MNO-7890', 52, '2024-10-08 11:40:00' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM onibus WHERE placa = 'MNO-7890');

INSERT INTO onibus (placa, capacidade, data_ultima_manutencao)
SELECT 'PQR-1122', 48, '2024-09-28 16:20:00' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM onibus WHERE placa = 'PQR-1122');

INSERT INTO onibus (placa, capacidade, data_ultima_manutencao)
SELECT 'STU-3344', 62, '2024-10-12 07:50:00' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM onibus WHERE placa = 'STU-3344');

INSERT INTO onibus (placa, capacidade, data_ultima_manutencao)
SELECT 'VWX-5566', 58, '2024-09-30 13:05:00' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM onibus WHERE placa = 'VWX-5566');

INSERT INTO onibus (placa, capacidade, data_ultima_manutencao)
SELECT 'YZA-7788', 47, '2024-10-03 10:10:00' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM onibus WHERE placa = 'YZA-7788');

INSERT INTO onibus (placa, capacidade, data_ultima_manutencao)
SELECT 'BCD-9900', 65, '2024-10-09 15:45:00' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM onibus WHERE placa = 'BCD-9900');

INSERT INTO onibus (placa, capacidade, data_ultima_manutencao)
SELECT 'EFG-1111', 50, '2024-10-10 08:00:00' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM onibus WHERE placa = 'EFG-1111');

INSERT INTO onibus (placa, capacidade, data_ultima_manutencao)
SELECT 'HIJ-2222', 55, '2024-10-11 09:15:00' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM onibus WHERE placa = 'HIJ-2222');

INSERT INTO onibus (placa, capacidade, data_ultima_manutencao)
SELECT 'KLM-3333', 60, '2024-10-12 10:30:00' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM onibus WHERE placa = 'KLM-3333');

INSERT INTO onibus (placa, capacidade, data_ultima_manutencao)
SELECT 'NOP-4444', 48, '2024-10-13 11:45:00' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM onibus WHERE placa = 'NOP-4444');

INSERT INTO onibus (placa, capacidade, data_ultima_manutencao)
SELECT 'QRS-5555', 52, '2024-10-14 13:10:00' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM onibus WHERE placa = 'QRS-5555');

INSERT INTO onibus (placa, capacidade, data_ultima_manutencao)
SELECT 'TUV-6666', 58, '2024-10-15 14:25:00' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM onibus WHERE placa = 'TUV-6666');

INSERT INTO onibus (placa, capacidade, data_ultima_manutencao)
SELECT 'WXY-7777', 47, '2024-10-16 15:40:00' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM onibus WHERE placa = 'WXY-7777');

INSERT INTO onibus (placa, capacidade, data_ultima_manutencao)
SELECT 'ZAB-8888', 62, '2024-10-17 16:55:00' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM onibus WHERE placa = 'ZAB-8888');

INSERT INTO onibus (placa, capacidade, data_ultima_manutencao)
SELECT 'CDE-9999', 53, '2024-10-18 18:05:00' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM onibus WHERE placa = 'CDE-9999');

INSERT INTO onibus (placa, capacidade, data_ultima_manutencao)
SELECT 'FGH-0001', 65, '2024-10-19 19:20:00' FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM onibus WHERE placa = 'FGH-0001');
