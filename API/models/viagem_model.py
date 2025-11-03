from API.models.db import get_db_connection
from datetime import datetime

def list_all():
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT v.*, o.placa, l.nome as linha_nome
        FROM viagem v
        JOIN onibus o ON v.id_onibus = o.id_onibus
        JOIN linha l ON v.id_linha = l.id_linha
        ORDER BY v.data_hora_inicio DESC
    """)
    data = cur.fetchall(); cur.close(); conn.close()
    return data

def get_by_id(id_):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT v.*, o.placa, l.nome as linha_nome
        FROM viagem v
        JOIN onibus o ON v.id_onibus = o.id_onibus
        JOIN linha l ON v.id_linha = l.id_linha
        WHERE v.id_viagem = %s
    """, (id_,))
    row = cur.fetchone(); cur.close(); conn.close()
    return row

def create(payload):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute("""
            INSERT INTO viagem (id_onibus, id_linha, data_hora_inicio, data_hora_fim, status)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            payload["id_onibus"], payload["id_linha"], payload.get("data_hora_inicio", datetime.now()),
            payload.get("data_hora_fim"), payload.get("status", "em_andamento")
        ))
        new_id = cur.lastrowid; conn.commit()
        cur.execute("""
            SELECT v.*, o.placa, l.nome as linha_nome
            FROM viagem v
            JOIN onibus o ON v.id_onibus = o.id_onibus
            JOIN linha l ON v.id_linha = l.id_linha
            WHERE v.id_viagem = %s
        """, (new_id,))
        return cur.fetchone()
    finally:
        cur.close(); conn.close()

def update(id_, payload):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute("""
            UPDATE viagem SET id_onibus=%s, id_linha=%s, data_hora_inicio=%s, data_hora_fim=%s, status=%s
            WHERE id_viagem=%s
        """, (
            payload["id_onibus"], payload["id_linha"], payload["data_hora_inicio"],
            payload.get("data_hora_fim"), payload["status"], id_
        ))
        conn.commit()
        if cur.rowcount:
            return get_by_id(id_)
        return None
    finally:
        cur.close(); conn.close()

def delete(id_):
    conn = get_db_connection(); cur = conn.cursor()
    cur.execute("DELETE FROM viagem WHERE id_viagem = %s", (id_,))
    affected = cur.rowcount; conn.commit(); cur.close(); conn.close()
    return affected > 0
