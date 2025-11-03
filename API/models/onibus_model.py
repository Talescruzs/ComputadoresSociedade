from API.models.db import get_db_connection

def list_all():
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM onibus ORDER BY id_onibus")
    data = cur.fetchall(); cur.close(); conn.close()
    return data

def get_by_id(id_):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM onibus WHERE id_onibus = %s", (id_,))
    data = cur.fetchone(); cur.close(); conn.close()
    return data

def create(payload):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            "INSERT INTO onibus (placa, capacidade, data_ultima_manutencao) VALUES (%s, %s, %s)",
            (payload["placa"], payload["capacidade"], payload.get("data_ultima_manutencao")),
        )
        new_id = cur.lastrowid; conn.commit()
        cur.execute("SELECT * FROM onibus WHERE id_onibus = %s", (new_id,))
        row = cur.fetchone(); return row
    finally:
        cur.close(); conn.close()

def update(id_, payload):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            "UPDATE onibus SET placa=%s, capacidade=%s, data_ultima_manutencao=%s WHERE id_onibus=%s",
            (payload["placa"], payload["capacidade"], payload.get("data_ultima_manutencao"), id_),
        )
        conn.commit()
        if cur.rowcount:
            cur.execute("SELECT * FROM onibus WHERE id_onibus = %s", (id_,))
            return cur.fetchone()
        return None
    finally:
        cur.close(); conn.close()

def delete(id_):
    conn = get_db_connection(); cur = conn.cursor()
    cur.execute("DELETE FROM onibus WHERE id_onibus = %s", (id_,))
    affected = cur.rowcount; conn.commit(); cur.close(); conn.close()
    return affected > 0
