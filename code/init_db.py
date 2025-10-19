#!/usr/bin/env python3
"""
Script para inicializar o banco de dados SQLite
"""
import sqlite3
import os

DB_PATH = 'transit.db'

def init_database():
    """Cria e inicializa o banco de dados"""
    
    print("═══════════════════════════════════════════════════════════")
    print("  🗄️  Inicializando banco de dados SQLite")
    print("═══════════════════════════════════════════════════════════")
    print()
    
    # Verificar se já existe
    if os.path.exists(DB_PATH):
        print("⚠️  Banco de dados existente encontrado")
        response = input("Deseja apagar e criar um novo? (s/N): ")
        if response.lower() != 's':
            print("Mantendo banco existente")
            return
        os.remove(DB_PATH)
        print("✓ Banco antigo removido")
    
    # Criar conexão
    print("Criando banco de dados...")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Criar tabelas
    cur.executescript('''
        -- Tabela de Ônibus
        CREATE TABLE IF NOT EXISTS onibus (
            id_onibus INTEGER PRIMARY KEY AUTOINCREMENT,
            placa VARCHAR(10) UNIQUE NOT NULL,
            capacidade INTEGER NOT NULL,
            data_ultima_manutencao TIMESTAMP
        );

        -- Tabela de Linhas
        CREATE TABLE IF NOT EXISTS linha (
            id_linha INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(100) NOT NULL
        );

        -- Tabela de Paradas
        CREATE TABLE IF NOT EXISTS parada (
            id_parada INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(100) NOT NULL,
            localizacao VARCHAR(255) NOT NULL
        );

        -- Tabela de Rotas
        CREATE TABLE IF NOT EXISTS rota (
            id_rota INTEGER PRIMARY KEY AUTOINCREMENT,
            id_linha INTEGER NOT NULL,
            id_parada INTEGER NOT NULL,
            ordem INTEGER NOT NULL,
            esta_ativa BOOLEAN DEFAULT 1,
            FOREIGN KEY (id_linha) REFERENCES linha(id_linha) ON DELETE CASCADE,
            FOREIGN KEY (id_parada) REFERENCES parada(id_parada) ON DELETE CASCADE,
            UNIQUE(id_linha, id_parada, ordem)
        );

        -- Tabela de Viagens
        CREATE TABLE IF NOT EXISTS viagem (
            id_viagem INTEGER PRIMARY KEY AUTOINCREMENT,
            id_onibus INTEGER NOT NULL,
            id_linha INTEGER NOT NULL,
            data_hora_inicio TIMESTAMP NOT NULL,
            data_hora_fim TIMESTAMP,
            status VARCHAR(20) DEFAULT 'em_andamento',
            FOREIGN KEY (id_onibus) REFERENCES onibus(id_onibus) ON DELETE CASCADE,
            FOREIGN KEY (id_linha) REFERENCES linha(id_linha) ON DELETE CASCADE
        );

        -- Tabela de Registro de Lotação
        CREATE TABLE IF NOT EXISTS registro_lotacao (
            id_lotacao INTEGER PRIMARY KEY AUTOINCREMENT,
            id_viagem INTEGER NOT NULL,
            id_parada_origem INTEGER NOT NULL,
            id_parada_destino INTEGER,
            data_hora TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            qtd_pessoas INTEGER NOT NULL,
            FOREIGN KEY (id_viagem) REFERENCES viagem(id_viagem) ON DELETE CASCADE,
            FOREIGN KEY (id_parada_origem) REFERENCES parada(id_parada) ON DELETE CASCADE,
            FOREIGN KEY (id_parada_destino) REFERENCES parada(id_parada) ON DELETE CASCADE
        );

        -- Índices
        CREATE INDEX IF NOT EXISTS idx_viagem_onibus ON viagem(id_onibus);
        CREATE INDEX IF NOT EXISTS idx_viagem_linha ON viagem(id_linha);
        CREATE INDEX IF NOT EXISTS idx_rota_linha ON rota(id_linha);
        CREATE INDEX IF NOT EXISTS idx_registro_viagem ON registro_lotacao(id_viagem);
        CREATE INDEX IF NOT EXISTS idx_registro_data ON registro_lotacao(data_hora);
    ''')
    
    print("✓ Tabelas criadas")
    
    # Inserir dados de exemplo
    print("Inserindo dados de exemplo...")
    
    cur.executescript('''
        -- Ônibus
        INSERT INTO onibus (placa, capacidade, data_ultima_manutencao) VALUES
            ('ABC-1234', 50, '2024-09-15 10:00:00'),
            ('DEF-5678', 45, '2024-09-20 14:30:00'),
            ('GHI-9012', 60, '2024-10-01 09:00:00');

        -- Linhas
        INSERT INTO linha (nome) VALUES
            ('Linha 100 - Centro/Terminal'),
            ('Linha 200 - Aeroporto/Rodoviária'),
            ('Linha 300 - Shopping/Hospital');

        -- Paradas
        INSERT INTO parada (nome, localizacao) VALUES
            ('Terminal Central', 'Av. Principal, 100'),
            ('Praça da Matriz', 'Centro, Praça 1'),
            ('Shopping Center', 'Av. Comercial, 500'),
            ('Hospital Regional', 'Rua da Saúde, 200'),
            ('Aeroporto', 'Rod. BR-101, km 45'),
            ('Rodoviária', 'Av. dos Estados, 300');

        -- Rotas
        INSERT INTO rota (id_linha, id_parada, ordem, esta_ativa) VALUES
            (1, 1, 1, 1),
            (1, 2, 2, 1),
            (1, 3, 3, 1),
            (2, 5, 1, 1),
            (2, 1, 2, 1),
            (2, 6, 3, 1),
            (3, 3, 1, 1),
            (3, 4, 2, 1),
            (3, 1, 3, 1);
    ''')
    
    conn.commit()
    print("✓ Dados inseridos")
    
    conn.close()
    
    print()
    print("═══════════════════════════════════════════════════════════")
    print("  ✅ Banco de dados criado com sucesso!")
    print("═══════════════════════════════════════════════════════════")
    print()
    print("📊 Dados incluídos:")
    print("  • 3 ônibus")
    print("  • 3 linhas")
    print("  • 6 paradas")
    print("  • 9 rotas")
    print()
    print("🚀 Próximo passo:")
    print("  Execute: ./start_sqlite.sh")
    print("  Ou: python app_sqlite.py")
    print()

if __name__ == '__main__':
    try:
        init_database()
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        exit(1)
