#!/usr/bin/env python3
"""
Zera registros do banco MySQL (safe: dados dinâmicos; all: todas as tabelas)
Uso:
  python DB/db_data.py                  # modo seguro (registro_lotacao, viagem)
  python DB/db_data.py --scope all      # zera tudo
  python DB/db_data.py --scope all --yes
"""
import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

def load_env():
    root_env = Path(__file__).resolve().parents[1] / ".env"
    code_env = Path(__file__).resolve().parents[1] / "code" / ".env"
    for candidate in (root_env, code_env):
        if candidate.exists() and load_dotenv(str(candidate), override=True):
            print(f"Usando .env: {candidate}")
            return
    print("Aviso: .env não encontrado (raiz nem code/.env). Usando variáveis de ambiente do sistema (se houver).")

def get_conn():
    cfg = {
        "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "transit_db"),
        "port": int(os.getenv("DB_PORT", "3306")),
    }
    print(f"Conectando MySQL: {cfg['user']}@{cfg['host']}:{cfg['port']}/{cfg['database']}")
    return mysql.connector.connect(**cfg)

SAFE_TABLES = ["registro_lotacao", "viagem"]
ALL_TABLES = ["registro_lotacao", "rota", "viagem", "parada", "linha", "onibus"]

def truncate_tables(cur, tables):
    # Desabilitar checagens de FK para truncar em qualquer ordem
    cur.execute("SET FOREIGN_KEY_CHECKS=0")
    for t in tables:
        try:
            cur.execute(f"TRUNCATE TABLE `{t}`")
            print(f"TRUNCATE `{t}`: OK")
        except Error as e:
            print(f"TRUNCATE `{t}`: ignorado ({e})")
    cur.execute("SET FOREIGN_KEY_CHECKS=1")

def main():
    parser = argparse.ArgumentParser(description="Zera registros do banco MySQL")
    parser.add_argument("--scope", choices=["safe", "all"], default="safe",
                        help="safe: zera somente dados dinâmicos (registro_lotacao, viagem). all: zera tudo.")
    parser.add_argument("--yes", action="store_true", help="Não perguntar confirmação")
    args = parser.parse_args()

    load_env()
    tables = SAFE_TABLES if args.scope == "safe" else ALL_TABLES

    if not args.yes:
        print(f"Atenção: as tabelas serão truncadas (AUTO_INCREMENT reiniciado). Escopo: {args.scope}")
        print("Tabela(s): " + ", ".join(tables))
        resp = input("Confirmar? (digite 'SIM' para prosseguir): ").strip()
        if resp != "SIM":
            print("Operação cancelada.")
            return

    try:
        conn = get_conn()
        cur = conn.cursor()
        truncate_tables(cur, tables)
        conn.commit()
        print("✅ Dados zerados com sucesso.")
    except Error as e:
        print(f"❌ Erro ao zerar dados: {e}")
        sys.exit(1)
    finally:
        try:
            cur.close()
            conn.close()
        except Exception:
            pass

if __name__ == "__main__":
    main()
