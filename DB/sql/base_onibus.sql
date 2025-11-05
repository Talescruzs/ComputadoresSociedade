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
