from API.models.db import get_db_connection

def list_all():
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM linha ORDER BY id_linha")
    data = cur.fetchall(); cur.close(); conn.close()
    return data

def get_by_id(id_):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM linha WHERE id_linha = %s", (id_,))
    row = cur.fetchone(); cur.close(); conn.close()
    return row

def create(payload):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute("INSERT INTO linha (nome) VALUES (%s)", (payload["nome"],))
        new_id = cur.lastrowid; conn.commit()
        cur.execute("SELECT * FROM linha WHERE id_linha = %s", (new_id,))
        return cur.fetchone()
    finally:
        cur.close(); conn.close()

def update(id_, payload):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute("UPDATE linha SET nome=%s WHERE id_linha=%s", (payload["nome"], id_))
        conn.commit()
        if cur.rowcount:
            cur.execute("SELECT * FROM linha WHERE id_linha = %s", (id_,))
            return cur.fetchone()
        return None
    finally:
        cur.close(); conn.close()

def delete(id_):
    conn = get_db_connection(); cur = conn.cursor()
    cur.execute("DELETE FROM linha WHERE id_linha = %s", (id_,))
    affected = cur.rowcount; conn.commit(); cur.close(); conn.close()
    return affected > 0
