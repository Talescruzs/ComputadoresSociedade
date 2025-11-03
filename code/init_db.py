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

def load_env():
    env_path = Path(__file__).parent / ".env"
    load_dotenv(env_path)

def get_conn(include_db=False):
    cfg = {
        "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "port": int(os.getenv("DB_PORT", "3306")),
    }
    if include_db:
        cfg["database"] = os.getenv("DB_NAME", "transit_db")
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
        sql = f.read()
    sql = _remove_db_directives(sql)
    if not sql.strip():
        return
    for _ in cursor.execute(sql, multi=True):
        pass

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
        # Chaves estrangeiras (idempotentes)
        try:
            add_fk_if_missing(cursor, db_name, "registro_lotacao", "fk_rl_parada_origem", "id_parada_origem", "parada", "id_parada")
        except Error:
            pass
        try:
            add_fk_if_missing(cursor, db_name, "registro_lotacao", "fk_rl_parada_destino", "id_parada_destino", "parada", "id_parada")
        except Error:
            pass

def main():
    parser = argparse.ArgumentParser(description="Inicializa o banco MySQL com base no CreateDB.sql")
    parser.add_argument("--sql", default=str(Path(__file__).parents[1] / "DB" / "CreateDB.sql"), help="Caminho para o arquivo SQL")
    args = parser.parse_args()

    load_env()
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
