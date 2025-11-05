#!/usr/bin/env python3
"""
Script para inicializar o banco de dados MySQL
"""
import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import re  # <-- adicionar

def load_env():
    # Novo: procurar .env na raiz e fallback para code/.env
    root_env = Path(__file__).resolve().parents[1] / ".env"
    code_env = Path(__file__).resolve().parents[1] / "code" / ".env"
    for candidate in (root_env, code_env):
        if candidate.exists() and load_dotenv(str(candidate), override=True):
            print(f"Usando .env: {candidate}")
            return candidate
    print("Aviso: .env não encontrado (raiz nem code/.env). Usando variáveis de ambiente do sistema (se houver).")
    return None

def get_conn(include_db=False):
    cfg = {
        "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "port": int(os.getenv("DB_PORT", "3306")),
    }
    if include_db:
        cfg["database"] = os.getenv("DB_NAME", "transit_db")
    # Log da conexão (sem senha)
    target_db = cfg.get("database", "(sem DB)")
    print(f"Conectando MySQL: {cfg['user']}@{cfg['host']}:{cfg['port']}/{target_db}")
    return mysql.connector.connect(**cfg)

def ensure_database(cursor, db_name):
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` DEFAULT CHARACTER SET utf8mb4")
    cursor.execute(f"USE `{db_name}`")

def _remove_db_directives(sql: str):
    lines = []
    for line in sql.splitlines():
        l = line.strip().rstrip(";")
        if l.upper().startswith("CREATE DATABASE") or l.upper().startswith("USE "):
            continue
        lines.append(line)
    return "\n".join(lines)

def exec_sql_file(cursor, sql_path: Path):
    with sql_path.open("r", encoding="utf-8") as f:
        raw = f.read()
    # remove CREATE DATABASE/USE
    raw = _remove_db_directives(raw)
    if not raw.strip():
        return
    # remover comentários de bloco /* ... */ e de linha -- ...
    no_block = re.sub(r"/\*.*?\*/", "", raw, flags=re.S)
    lines = []
    for line in no_block.splitlines():
        line = re.sub(r"--.*", "", line).strip()
        if line:
            lines.append(line)
    sql_clean = "\n".join(lines)
    # executar statements individualmente (sem multi=True)
    statements = [stmt.strip() for stmt in sql_clean.split(";") if stmt.strip()]
    for stmt in statements:
        cursor.execute(stmt)

def table_exists(cursor, db_name, table_name):
    cursor.execute(
        "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=%s AND table_name=%s",
        (db_name, table_name),
    )
    return cursor.fetchone()[0] == 1

def column_exists(cursor, db_name, table_name, column_name):
    cursor.execute(
        "SELECT COUNT(*) FROM information_schema.columns WHERE table_schema=%s AND table_name=%s AND column_name=%s",
        (db_name, table_name, column_name),
    )
    return cursor.fetchone()[0] == 1

def is_not_nullable(cursor, db_name, table_name, column_name):
    cursor.execute(
        """
        SELECT CASE WHEN is_nullable='NO' THEN 1 ELSE 0 END
        FROM information_schema.columns
        WHERE table_schema=%s AND table_name=%s AND column_name=%s
        """,
        (db_name, table_name, column_name),
    )
    row = cursor.fetchone()
    return bool(row and row[0] == 1)

def fk_exists(cursor, db_name, table_name, constraint_name):
    cursor.execute(
        """
        SELECT COUNT(*) 
        FROM information_schema.referential_constraints 
        WHERE constraint_schema=%s AND constraint_name=%s AND table_name=%s
        """,
        (db_name, constraint_name, table_name),
    )
    return cursor.fetchone()[0] == 1

def rename_table_if_needed(cursor, db_name, old, new):
    if table_exists(cursor, db_name, old) and not table_exists(cursor, db_name, new):
        cursor.execute(f"RENAME TABLE `{old}` TO `{new}`")

def add_column_if_missing(cursor, db_name, table, column_def):
    col_name = column_def.split()[0].strip("`")
    if not column_exists(cursor, db_name, table, col_name):
        cursor.execute(f"ALTER TABLE `{table}` ADD COLUMN {column_def}")

def add_fk_if_missing(cursor, db_name, table, constraint_name, col, ref_table, ref_col):
    if not fk_exists(cursor, db_name, table, constraint_name):
        cursor.execute(
            f"ALTER TABLE `{table}` ADD CONSTRAINT `{constraint_name}` FOREIGN KEY (`{col}`) "
            f"REFERENCES `{ref_table}`(`{ref_col}`)"
        )

def drop_fk_by_names(cursor, db_name: str, names: list[str]):
    if not names:
        return
    fmt = ",".join(["%s"] * len(names))
    cursor.execute(
        f"""
        SELECT table_name, constraint_name
        FROM information_schema.referential_constraints
        WHERE constraint_schema=%s AND constraint_name IN ({fmt})
        """,
        (db_name, *names),
    )
    rows = cursor.fetchall() or []
    for table_name, constraint_name in rows:
        try:
            cursor.execute(f"ALTER TABLE `{table_name}` DROP FOREIGN KEY `{constraint_name}`")
            # print(f"Dropped FK {constraint_name} on {table_name}")
        except Error:
            pass

# Novo: dropa todas as FKs das tabelas informadas (idempotente)
def drop_all_fks_for_tables(cursor, db_name: str, table_names: list[str]):
    if not table_names:
        return
    fmt = ",".join(["%s"] * len(table_names))
    cursor.execute(
        f"""
        SELECT table_name, constraint_name
        FROM information_schema.referential_constraints
        WHERE constraint_schema=%s AND table_name IN ({fmt})
        """,
        (db_name, *table_names),
    )
    rows = cursor.fetchall() or []
    for table_name, constraint_name in rows:
        try:
            cursor.execute(f"ALTER TABLE `{table_name}` DROP FOREIGN KEY `{constraint_name}`")
        except Error:
            pass

def align_schema_for_api(cursor, db_name):
    # Renomear tabelas CamelCase -> minúsculas (compatível com as queries da API)
    rename_table_if_needed(cursor, db_name, "Onibus", "onibus")
    rename_table_if_needed(cursor, db_name, "Linha", "linha")
    rename_table_if_needed(cursor, db_name, "Parada", "parada")
    rename_table_if_needed(cursor, db_name, "Viagem", "viagem")
    rename_table_if_needed(cursor, db_name, "RegistroLotacao", "registro_lotacao")
    rename_table_if_needed(cursor, db_name, "Rota", "rota")

    # Garantir colunas usadas pela API
    # viagem: data_hora_inicio, data_hora_fim, status
    if table_exists(cursor, db_name, "viagem"):
        add_column_if_missing(cursor, db_name, "viagem", "data_hora_inicio DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP")
        add_column_if_missing(cursor, db_name, "viagem", "data_hora_fim DATETIME NULL")
        add_column_if_missing(cursor, db_name, "viagem", "status VARCHAR(20) NOT NULL DEFAULT 'em_andamento'")

    # registro_lotacao: id_parada_origem, id_parada_destino
    if table_exists(cursor, db_name, "registro_lotacao"):
        add_column_if_missing(cursor, db_name, "registro_lotacao", "id_parada_origem INT NOT NULL")
        add_column_if_missing(cursor, db_name, "registro_lotacao", "id_parada_destino INT NULL")
        # Tornar coluna legada id_parada opcional, se existir e for NOT NULL
        if column_exists(cursor, db_name, "registro_lotacao", "id_parada"):
            try:
                if is_not_nullable(cursor, db_name, "registro_lotacao", "id_parada"):
                    cursor.execute("ALTER TABLE `registro_lotacao` MODIFY `id_parada` INT NULL")
            except Error:
                pass
        # Chaves estrangeiras (idempotentes)
        try:
            add_fk_if_missing(cursor, db_name, "registro_lotacao", "fk_rl_parada_origem", "id_parada_origem", "parada", "id_parada")
        except Error:
            pass
        try:
            add_fk_if_missing(cursor, db_name, "registro_lotacao", "fk_rl_parada_destino", "id_parada_destino", "parada", "id_parada")
        except Error:
            pass

    # Garantir coluna 'esta_ativa' em 'rota' (usada pelos scripts de rota *.sql)
    if table_exists(cursor, db_name, "rota"):
        add_column_if_missing(cursor, db_name, "rota", "esta_ativa TINYINT(1) NOT NULL DEFAULT 1")

def main():
    parser = argparse.ArgumentParser(description="Inicializa o banco MySQL com base no CreateDB.sql")
    parser.add_argument("--sql", default=str(Path(__file__).parents[1] / "DB" / "CreateDB.sql"), help="Caminho para o arquivo SQL")
    args = parser.parse_args()

    used_env = load_env()
    db_name = os.getenv("DB_NAME", "transit_db")

    sql_path = Path(args.sql)
    if not sql_path.exists():
        print(f"Arquivo SQL não encontrado: {sql_path}")
        sys.exit(1)

    try:
        # Conexão sem database para criar DB
        conn = get_conn(include_db=False)
        cur = conn.cursor()
        ensure_database(cur, db_name)
        conn.commit()

        # Reabrir conexão já usando o DB alvo
        cur.close()
        conn.close()
        conn = get_conn(include_db=True)
        cur = conn.cursor()

        # Evitar erro 1826 (FK duplicada) antes de executar o script SQL
        # 1) Drop por nome conhecido (compatível com auto-nomes do MySQL)
        drop_fk_by_names(cur, db_name, ["Viagem_ibfk_1", "Viagem_ibfk_2", "Rota_ibfk_1", "Rota_ibfk_2", "RegistroLotacao_ibfk_1", "RegistroLotacao_ibfk_2"])
        # 2) Drop genérico de todas as FKs das tabelas criadas pelo CreateDB.sql (CamelCase)
        drop_all_fks_for_tables(cur, db_name, ["Viagem", "RegistroLotacao", "Rota"])
        conn.commit()

        # Executar SQL (sem CREATE DATABASE/USE)
        exec_sql_file(cur, sql_path)
        conn.commit()

        # Ajustes para casar com a API
        cur.close()
        cur = conn.cursor()
        align_schema_for_api(cur, db_name)
        conn.commit()

        print(f"✅ Banco inicializado com sucesso no schema '{db_name}'.")
    except Error as e:
        # Mensagem amigável para erros de autenticação (1045/1698)
        if getattr(e, "errno", None) in (1045, 1698):
            user = os.getenv("DB_USER", "root")
            host = os.getenv("DB_HOST", "localhost")
            port = os.getenv("DB_PORT", "3306")
            print(f"❌ Acesso negado ({e.errno}): {e}")
            print(f"  - .env usado: {used_env or '[não carregado]'}")
            print("  - Verifique credenciais no .env (DB_USER/DB_PASSWORD/DB_NAME) e privilégios no MySQL:")
            print(f"      CREATE USER '{user}'@'localhost' IDENTIFIED BY 'SUA_SENHA';")
            print(f"      GRANT ALL PRIVILEGES ON {db_name}.* TO '{user}'@'localhost';")
            print("      FLUSH PRIVILEGES;")
            print(f"  - Conferir conexão: {user}@{host}:{port}/{db_name}")
        else:
            print(f"❌ Erro ao inicializar o banco: {e}")
        sys.exit(1)
    finally:
        try:
            cur.close()
            conn.close()
        except Exception:
            pass

if __name__ == "__main__":
    main()
