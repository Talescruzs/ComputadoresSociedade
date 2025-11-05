CREATE DATABASE IF NOT EXISTS banco_atu;
USE banco_atu;

-- ==============================
-- Tabela: Onibus
-- ==============================
CREATE TABLE IF NOT EXISTS Onibus (
    id_onibus INT AUTO_INCREMENT PRIMARY KEY,
    placa VARCHAR(10) NOT NULL UNIQUE,
    capacidade INT NOT NULL,
    data_ultima_manutencao DATE
);

-- ==============================
-- Tabela: Linha
-- ==============================
CREATE TABLE IF NOT EXISTS Linha (
    id_linha INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

-- ==============================
-- Tabela: Parada
-- ==============================
CREATE TABLE IF NOT EXISTS Parada (
    id_parada INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    localizacao VARCHAR(255) NOT NULL
);

-- ==============================
-- Tabela: Viagem
-- ==============================
CREATE TABLE IF NOT EXISTS Viagem (
    id_viagem INT AUTO_INCREMENT PRIMARY KEY,
    id_onibus INT NOT NULL,
    id_linha INT NOT NULL,
    FOREIGN KEY (id_onibus) REFERENCES Onibus(id_onibus),
    FOREIGN KEY (id_linha) REFERENCES Linha(id_linha)
);

-- ==============================
-- Tabela: RegistroLotacao
-- ==============================
CREATE TABLE IF NOT EXISTS RegistroLotacao (
    id_lotacao INT AUTO_INCREMENT PRIMARY KEY,
    qtd_pessoas INT NOT NULL,
    id_viagem INT NOT NULL,
    id_parada INT NOT NULL,
    data_hora DATETIME NOT NULL,
    FOREIGN KEY (id_viagem) REFERENCES Viagem(id_viagem),
    FOREIGN KEY (id_parada) REFERENCES Parada(id_parada)
);

-- ==============================
-- Relação: Linha ↔ Parada (Rota)
-- ==============================
CREATE TABLE IF NOT EXISTS Rota (
    id_rota INT AUTO_INCREMENT PRIMARY KEY,
    id_linha INT NOT NULL,
    id_parada INT NOT NULL,
    ordem INT,
    FOREIGN KEY (id_linha) REFERENCES Linha(id_linha),
    FOREIGN KEY (id_parada) REFERENCES Parada(id_parada)
);
