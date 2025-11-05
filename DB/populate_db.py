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
import re

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

def table_exists(cur, table, schema):
    cur.execute(
        """
        SELECT COUNT(*) FROM information_schema.tables
        WHERE table_schema=%s AND table_name=%s
        """,
        (schema, table),
    )
    return cur.fetchone()[0] == 1

def get_linha_id_by_name(cur, nome):
    cur.execute("SELECT id_linha FROM linha WHERE nome = %s", (nome,))
    row = cur.fetchone()
    return row[0] if row else None

# NOVO: obter paradas (em ordem, se houver) pertencentes à rota da linha
def get_route_stops(cur, id_linha, schema):
    """Retorna a lista de ids de paradas associadas à linha na tabela 'rota' (em ordem se existir)."""
    if not table_exists(cur, "rota", schema):
        return []
    has_ordem = has_column(cur, "rota", "ordem", schema)
    order_by = "r.ordem ASC" if has_ordem else "r.id_parada ASC"
    cur.execute(f"SELECT r.id_parada FROM rota r WHERE r.id_linha = %s ORDER BY {order_by}", (id_linha,))
    return [row[0] for row in cur.fetchall()]

def get_parada_id_by_name(cur, nome):
    cur.execute("SELECT id_parada FROM parada WHERE nome = %s", (nome,))
    row = cur.fetchone()
    return row[0] if row else None

def get_or_create_parada(cur, nome, localizacao=None):
    pid = get_parada_id_by_name(cur, nome)
    if pid:
        return pid
    cur.execute(
        "INSERT INTO parada (nome, localizacao) VALUES (%s, %s)",
        (nome, localizacao or nome),
    )
    return cur.lastrowid

def rota_entry_exists(cur, id_linha, id_parada):
    cur.execute(
        "SELECT COUNT(*) FROM rota WHERE id_linha = %s AND id_parada = %s",
        (id_linha, id_parada),
    )
    return cur.fetchone()[0] > 0

def exec_sql_file(cur, sql_path: Path):
    with sql_path.open("r", encoding="utf-8") as f:
        raw = f.read()

    # Remove comentários de bloco /* ... */ e de linha -- ...
    sql = re.sub(r"/\*.*?\*/", "", raw, flags=re.S)
    lines = []
    for line in sql.splitlines():
        # remove comentários de linha (tudo após --)
        cleaned = re.sub(r"--.*", "", line).strip()
        if cleaned:
            lines.append(cleaned)
    sql_clean = "\n".join(lines)

    # Executa statements individualmente (sem usar multi=True)
    statements = [stmt.strip() for stmt in sql_clean.split(";") if stmt.strip()]
    for stmt in statements:
        cur.execute(stmt)

def ensure_bombeiros_ufsm_faixa_velha_route(cur, conn):
    """
    Garante a rota 'Bombeiros/UFSM - Faixa Velha' executando SQL idempotente.
    """
    sql_path = Path(__file__).parent / "sql" / "rota_bombeiros_ufsm_faixa_velha.sql"
    exec_sql_file(cur, sql_path)
    conn.commit()
    print("✓ SQL executado: rota Bombeiros/UFSM - Faixa Velha")

def ensure_bombeiros_ufsm_faixa_nova_route(cur, conn):
    """
    Garante a rota 'Bombeiros/UFSM - Faixa Nova' executando SQL idempotente.
    """
    sql_path = Path(__file__).parent / "sql" / "rota_bombeiros_ufsm_faixa_nova.sql"
    exec_sql_file(cur, sql_path)
    conn.commit()
    print("✓ SQL executado: rota Bombeiros/UFSM - Faixa Nova")

def ensure_ufsm_bombeiros_faixa_velha_route(cur, conn):
    """
    Garante a rota 'UFSM/Bombeiros - Faixa Velha' executando SQL idempotente.
    """
    sql_path = Path(__file__).parent / "sql" / "rota_ufsm_bombeiros_faixa_velha.sql"
    exec_sql_file(cur, sql_path)
    conn.commit()
    print("✓ SQL executado: rota UFSM/Bombeiros - Faixa Velha")

def ensure_ufsm_bombeiros_faixa_nova_route(cur, conn):
    """
    Garante a rota 'UFSM/Bombeiros - Faixa Nova' executando SQL idempotente.
    """
    sql_path = Path(__file__).parent / "sql" / "rota_ufsm_bombeiros_faixa_nova.sql"
    exec_sql_file(cur, sql_path)
    conn.commit()
    print("✓ SQL executado: rota UFSM/Bombeiros - Faixa Nova")

def ensure_vale_machado_ufsm_faixa_velha_route(cur, conn):
    # Executa SQL da rota Vale Machado/UFSM - Faixa Velha
    sql_path = Path(__file__).parent / "sql" / "rota_vale_machado_ufsm_faixa_velha.sql"
    exec_sql_file(cur, sql_path)
    conn.commit()
    print("✓ SQL executado: rota Vale Machado/UFSM - Faixa Velha")


def ensure_vale_machado_ufsm_faixa_nova_route(cur, conn):
    # Executa SQL da rota Vale Machado/UFSM - Faixa Nova
    sql_path = Path(__file__).parent / "sql" / "rota_vale_machado_ufsm_faixa_nova.sql"
    exec_sql_file(cur, sql_path)
    conn.commit()
    print("✓ SQL executado: rota Vale Machado/UFSM - Faixa Nova")

def ensure_ufsm_vale_machado_faixa_nova_route(cur, conn):
    # Executa SQL da rota UFSM/Vale Machado - Faixa Nova
    sql_path = Path(__file__).parent / "sql" / "rota_ufsm_vale_machado_faixa_nova.sql"
    exec_sql_file(cur, sql_path)
    conn.commit()
    print("✓ SQL executado: rota UFSM/Vale Machado - Faixa Nova")

def ensure_ufsm_vale_machado_faixa_velha_route(cur, conn):
    # Executa SQL da rota UFSM/Vale Machado - Faixa Velha
    sql_path = Path(__file__).parent / "sql" / "rota_ufsm_vale_machado_faixa_velha.sql"
    exec_sql_file(cur, sql_path)
    conn.commit()
    print("✓ SQL executado: rota UFSM/Vale Machado - Faixa Velha")

def ensure_base_data(cur, conn):
    """Garante dados-base mínimos (somente se vazias) via SQL idempotente."""
    inserted = False

    # Substitui inserts Python por SQL
    sql_dir = Path(__file__).parent / "sql"
    exec_sql_file(cur, sql_dir / "base_onibus.sql")
    exec_sql_file(cur, sql_dir / "base_linhas.sql")
    conn.commit()
    inserted = True  # Considera que o SQL já cuidou da idempotência
    if inserted:
        print("✓ Dados-base garantidos via SQL.")

    # Garante que a tabela 'rota' tenha a coluna 'esta_ativa'
    schema = DB_CONFIG["database"]
    if table_exists(cur, "rota", schema) and not has_column(cur, "rota", "esta_ativa", schema):
        cur.execute("ALTER TABLE `rota` ADD COLUMN `esta_ativa` TINYINT(1) NOT NULL DEFAULT 1")
        conn.commit()
        print("✓ Tabela 'rota' atualizada: adicionada coluna 'esta_ativa'.")

    # Após garantir base e schema, adiciona as rotas solicitadas (via SQL)
    ensure_bombeiros_ufsm_faixa_velha_route(cur, conn)
    ensure_bombeiros_ufsm_faixa_nova_route(cur, conn)
    ensure_ufsm_bombeiros_faixa_velha_route(cur, conn)
    ensure_ufsm_bombeiros_faixa_nova_route(cur, conn)  
    ensure_vale_machado_ufsm_faixa_velha_route(cur, conn)
    ensure_vale_machado_ufsm_faixa_nova_route(cur, conn)  
    ensure_ufsm_vale_machado_faixa_nova_route(cur, conn)
    ensure_ufsm_vale_machado_faixa_velha_route(cur, conn) 

    # Cria viagens aleatórias para até 3 ônibus em linhas com rota (>= 2 paradas)
    exec_sql_file(cur, sql_dir / "seed_viagens_random.sql")
    conn.commit()
    print("✓ Viagens iniciais criadas via SQL.")

    # Cria registros de lotação seguindo a ordem da rota
    exec_sql_file(cur, sql_dir / "seed_registro_lotacao.sql")
    conn.commit()
    print("✓ Registros de lotação criados via SQL.")

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
        # Apenas garantir ônibus, linhas e rotas via SQL
        ensure_base_data(cur, conn)

        # Finaliza sem criar viagens ou registros de lotação
        conn.commit()
        print("\n✓ População concluída (somente ônibus, linhas e rotas via SQL).")
    except Exception as e:
        conn.rollback()
        print(f"Erro ao popular banco de dados: {e}")
        print("\nVerifique:")
        print("  - Se a tabela 'rota' existe e as linhas possuem suas paradas associadas (>= 2)")
        print("  - Se o schema está alinhado com a API (rode o init_db.py, se necessário)")
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    populate_database()
