from API.models.db import get_db_connection

def list_all():
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM parada ORDER BY id_parada")
    data = cur.fetchall(); cur.close(); conn.close()
    return data

def get_by_id(id_):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM parada WHERE id_parada = %s", (id_,))
    row = cur.fetchone(); cur.close(); conn.close()
    return row

def create(payload):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute("INSERT INTO parada (nome, localizacao) VALUES (%s, %s)", (payload["nome"], payload["localizacao"]))
        new_id = cur.lastrowid; conn.commit()
        cur.execute("SELECT * FROM parada WHERE id_parada = %s", (new_id,))
        return cur.fetchone()
    finally:
        cur.close(); conn.close()

def update(id_, payload):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute("UPDATE parada SET nome=%s, localizacao=%s WHERE id_parada=%s", (payload["nome"], payload["localizacao"], id_))
        conn.commit()
        if cur.rowcount:
            cur.execute("SELECT * FROM parada WHERE id_parada = %s", (id_,))
            return cur.fetchone()
        return None
    finally:
        cur.close(); conn.close()

def delete(id_):
    conn = get_db_connection(); cur = conn.cursor()
    cur.execute("DELETE FROM parada WHERE id_parada = %s", (id_,))
    affected = cur.rowcount; conn.commit(); cur.close(); conn.close()
    return affected > 0
