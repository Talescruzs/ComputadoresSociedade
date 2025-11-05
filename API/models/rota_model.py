from pathlib import Path
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# Carregar .env (raiz do projeto -> fallback para API/.env)
BASE_DIR = Path(__file__).resolve().parents[2]
for env_path in (BASE_DIR / ".env", Path(__file__).resolve().parents[1] / ".env"):
    if env_path.exists() and load_dotenv(str(env_path), override=True):
        break

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "transit_db"),
    "port": int(os.getenv("DB_PORT", "3306")),
}

def get_conn():
    return mysql.connector.connect(**DB_CONFIG)

def rota_por_linha(id_linha: int):
    """
    Retorna a rota (paradas em ordem) da linha.
    Campos: id_parada, parada_nome, localizacao, ordem
    """
    sql = """
        SELECT
            p.id_parada,
            p.nome AS parada_nome,
            p.localizacao,
            r.ordem
        FROM rota r
        JOIN parada p ON p.id_parada = r.id_parada
        WHERE r.id_linha = %s
        ORDER BY r.ordem ASC, p.id_parada ASC
    """
    conn = get_conn(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute(sql, (id_linha,))
        return cur.fetchall()
    finally:
        cur.close(); conn.close()

def linhas_por_parada(id_parada: int):
    """
    Retorna as linhas às quais a parada pertence (com ordem na rota).
    Campos: id_linha, linha_nome, ordem
    """
    sql = """
        SELECT
            l.id_linha,
            l.nome AS linha_nome,
            r.ordem
        FROM rota r
        JOIN linha l ON l.id_linha = r.id_linha
        WHERE r.id_parada = %s
        ORDER BY l.nome ASC, r.ordem ASC
    """
    conn = get_conn(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute(sql, (id_parada,))
        return cur.fetchall()
    finally:
        cur.close(); conn.close()
