#!/usr/bin/env python3
"""
Drop (remover) um schema MySQL de forma segura.

Uso:
  python DB/drop_db.py                 # dropar 'transporte' (padrão) com confirmação
  python DB/drop_db.py --db transporte --yes
  python DB/drop_db.py --db banco_atu  # outro nome
"""
import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

CRITICAL_SCHEMAS = {"mysql", "information_schema", "performance_schema", "sys"}

def load_env():
    root_env = Path(__file__).resolve().parents[1] / ".env"
    code_env = Path(__file__).resolve().parents[1] / "code" / ".env"
    for candidate in (root_env, code_env):
        if candidate.exists() and load_dotenv(str(candidate), override=True):
            print(f"Usando .env: {candidate}")
            return candidate
    print("Aviso: .env não encontrado (raiz nem code/.env). Usando variáveis de ambiente do sistema (se houver).")
    return None

def get_conn():
    cfg = {
        "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "port": int(os.getenv("DB_PORT", "3306")),
    }
    print(f"Conectando MySQL (sem DB): {cfg['user']}@{cfg['host']}:{cfg['port']}/(sem DB)")
    return mysql.connector.connect(**cfg)

def drop_database(cursor, db_name: str):
    cursor.execute(f"DROP DATABASE IF EXISTS `{db_name}`")

def main():
    parser = argparse.ArgumentParser(description="Drop (remover) um schema MySQL.")
    parser.add_argument("--db", default="transporte", help="Nome do banco a remover (padrão: transporte)")
    parser.add_argument("--yes", action="store_true", help="Não perguntar confirmação")
    args = parser.parse_args()

    load_env()
    db_name = args.db.strip()

    if not db_name:
        print("❌ Nome de banco inválido.")
        sys.exit(1)
    if db_name in CRITICAL_SCHEMAS:
        print(f"❌ Operação bloqueada para schema crítico: '{db_name}'.")
        sys.exit(1)

    if not args.yes:
        print(f"Atenção: o schema '{db_name}' será removido (DROP DATABASE IF EXISTS).")
        resp = input("Confirme digitando 'SIM': ").strip()
        if resp != "SIM":
            print("Operação cancelada.")
            return

    try:
        conn = get_conn()
        cur = conn.cursor()
        drop_database(cur, db_name)
        conn.commit()
        print(f"✅ Schema '{db_name}' removido (ou já não existia).")
    except Error as e:
        print(f"❌ Erro ao dropar schema '{db_name}': {e}")
        if getattr(e, "errno", None) in (1045, 1698):
            user = os.getenv("DB_USER", "root")
            host = os.getenv("DB_HOST", "localhost")
            port = os.getenv("DB_PORT", "3306")
            print("  - Verifique credenciais e privilégios para DROP DATABASE:")
            print(f"      GRANT DROP ON *.* TO '{user}'@'{host}'; FLUSH PRIVILEGES;")
            print(f"  - Conexão: {user}@{host}:{port}")
        sys.exit(1)
    finally:
        try:
            cur.close()
            conn.close()
        except Exception:
            pass

if __name__ == "__main__":
    main()
