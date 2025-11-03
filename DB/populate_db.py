"""
Script para popular o banco de dados MySQL com dados de exemplo
Usa credenciais do arquivo .env no raiz do projeto (fallback: code/.env)
"""
import os
import random
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# Carregar .env (raiz do projeto -> fallback para code/.env)
ROOT_ENV = Path(__file__).resolve().parents[1] / ".env"
CODE_ENV = Path(__file__).resolve().parents[1] / "code" / ".env"
loaded_env = None
for candidate in (ROOT_ENV, CODE_ENV):
    if candidate.exists() and load_dotenv(str(candidate), override=True):
        loaded_env = candidate
        print(f"Usando .env: {candidate}")
        break
if not loaded_env:
    print("Aviso: .env não encontrado no projeto. Usando variáveis de ambiente do sistema (se houver).")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "transit_db"),
    "port": int(os.getenv("DB_PORT", "3306")),
}

def get_conn():
    print(f"Conectando MySQL: {DB_CONFIG['user']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")
    return mysql.connector.connect(**DB_CONFIG)

def fetch_ids(cur, table, id_col):
    cur.execute(f"SELECT {id_col} FROM {table}")
    return [row[0] for row in cur.fetchall()]

def get_count(cur, table):
    cur.execute(f"SELECT COUNT(*) FROM {table}")
    return cur.fetchone()[0]

def has_column(cur, table, column, schema):
    cur.execute(
        """
        SELECT COUNT(*) FROM information_schema.columns
        WHERE table_schema=%s AND table_name=%s AND column_name=%s
        """,
        (schema, table, column),
    )
    return cur.fetchone()[0] == 1

def ensure_base_data(cur, conn):
    """Garante dados-base mínimos em onibus, linha e parada (somente se vazias)."""
    inserted = False

    if get_count(cur, "onibus") == 0:
        buses = [
            ("ABC-1234", 50, "2024-09-15 10:00:00"),
            ("DEF-5678", 45, "2024-09-20 14:30:00"),
            ("GHI-9012", 60, "2024-10-01 09:00:00"),
        ]
        cur.executemany(
            "INSERT INTO onibus (placa, capacidade, data_ultima_manutencao) VALUES (%s, %s, %s)",
            buses,
        )
        print(f"  -> Inseridos {len(buses)} ônibus de exemplo")
        inserted = True

    if get_count(cur, "linha") == 0:
        linhas = [
            ("Linha 100 - Centro/Terminal",),
            ("Linha 200 - Aeroporto/Rodoviária",),
            ("Linha 300 - Shopping/Hospital",),
        ]
        cur.executemany("INSERT INTO linha (nome) VALUES (%s)", linhas)
        print(f"  -> Inseridas {len(linhas)} linhas de exemplo")
        inserted = True

    if get_count(cur, "parada") == 0:
        paradas = [
            ("Terminal Central", "Av. Principal, 100"),
            ("Praça da Matriz", "Centro, Praça 1"),
            ("Shopping Center", "Av. Comercial, 500"),
            ("Hospital Regional", "Rua da Saúde, 200"),
            ("Aeroporto", "Rod. BR-101, km 45"),
            ("Rodoviária", "Av. dos Estados, 300"),
        ]
        cur.executemany(
            "INSERT INTO parada (nome, localizacao) VALUES (%s, %s)",
            paradas,
        )
        print(f"  -> Inseridas {len(paradas)} paradas de exemplo")
        inserted = True

    if inserted:
        conn.commit()
        print("✓ Dados-base criados.")

def populate_database():
    try:
        conn = get_conn()
    except Error as e:
        # Erros comuns de autenticação 1045/1698
        if getattr(e, "errno", None) in (1045, 1698):
            print(f"\n❌ Falha de autenticação no MySQL ({e.errno}): {e}")
            print("Verifique:")
            print(f"  - Seu arquivo .env (DB_USER/DB_PASSWORD/DB_NAME corretos): {loaded_env or '[não carregado]'}")
            print("  - Permissões do usuário no MySQL, por exemplo:")
            print(f"      CREATE USER '{DB_CONFIG['user']}'@'localhost' IDENTIFIED BY 'SUA_SENHA';")
            print(f"      GRANT ALL PRIVILEGES ON {DB_CONFIG['database']}.* TO '{DB_CONFIG['user']}'@'localhost';")
            print("      FLUSH PRIVILEGES;")
        else:
            print(f"\n❌ Erro ao conectar no MySQL: {e}")
        return

    cur = conn.cursor()
    try:
        # Garante dados-base mínimos para prosseguir
        ensure_base_data(cur, conn)

        # Verificar dados-base
        bus_ids = fetch_ids(cur, "onibus", "id_onibus")
        line_ids = fetch_ids(cur, "linha", "id_linha")
        stop_ids = fetch_ids(cur, "parada", "id_parada")

        if not bus_ids or not line_ids or not stop_ids:
            raise RuntimeError(
                "Tabelas base vazias. Cadastre dados em onibus, linha e parada "
                "antes de popular viagens/lotações (ou rode seu script de seed)."
            )

        print("Criando viagens de exemplo...")
        now = datetime.now()
        viagens_ids = []

        for _ in range(10):
            data_inicio = now - timedelta(days=random.randint(0, 7), hours=random.randint(6, 20))
            id_onibus = random.choice(bus_ids)
            id_linha = random.choice(line_ids)

            cur.execute(
                """INSERT INTO viagem (id_onibus, id_linha, data_hora_inicio, status)
                   VALUES (%s, %s, %s, %s)""",
                (id_onibus, id_linha, data_inicio, "em_andamento"),
            )
            viagem_id = cur.lastrowid
            viagens_ids.append((viagem_id, data_inicio))
            print(f"  Viagem {viagem_id} criada")

        print("\nCriando registros de lotação...")
        # Detecta coluna legada 'id_parada'
        schema_name = DB_CONFIG["database"]
        include_legacy_id_parada = has_column(cur, "registro_lotacao", "id_parada", schema_name)

        for viagem_id, data_inicio in viagens_ids:
            num_registros = random.randint(3, 8)
            for i in range(num_registros):
                origem = random.choice(stop_ids)
                destino = random.choice(stop_ids)
                while destino == origem:
                    destino = random.choice(stop_ids)
                hora = data_inicio.hour
                qtd_pessoas = random.randint(30, 60) if (7 <= hora <= 9 or 17 <= hora <= 19) else random.randint(10, 35)
                data_registro = data_inicio + timedelta(minutes=i * 15)

                if include_legacy_id_parada:
                    # Preenche coluna legada com o destino (ou origem)
                    cur.execute(
                        """INSERT INTO registro_lotacao
                           (id_viagem, id_parada_origem, id_parada_destino, id_parada, data_hora, qtd_pessoas)
                           VALUES (%s, %s, %s, %s, %s, %s)""",
                        (viagem_id, origem, destino, destino or origem, data_registro, qtd_pessoas),
                    )
                else:
                    cur.execute(
                        """INSERT INTO registro_lotacao
                           (id_viagem, id_parada_origem, id_parada_destino, data_hora, qtd_pessoas)
                           VALUES (%s, %s, %s, %s, %s)""",
                        (viagem_id, origem, destino, data_registro, qtd_pessoas),
                    )
                print(f"  Registro de lotação criado para viagem {viagem_id}: {qtd_pessoas} pessoas")

        conn.commit()
        print("\n✓ Banco de dados populado com sucesso!")
        print(f"  - {len(viagens_ids)} viagens criadas")
        print(f"  - Aproximadamente {len(viagens_ids) * 5} registros de lotação criados")
    except Exception as e:
        conn.rollback()
        print(f"Erro ao popular banco de dados: {e}")
        print("\nVerifique:")
        print(f"  - Conexão MySQL ({DB_CONFIG['user']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']})")
        print("  - Se .env está correto")
        print("  - Se as tabelas onibus, linha e parada possuem registros")
        print("  - Se o schema está alinhado com a API (rode o init_db.py, se necessário)")
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    populate_database()
