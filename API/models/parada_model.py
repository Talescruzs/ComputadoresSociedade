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

def pessoas_total_por_parada():
    """
    Retorna total de embarques por parada (quantidade de pessoas que subiram).
    Lógica: para cada registro de lotação considera diferença positiva entre
    ocupação atual e ocupação imediatamente anterior na mesma viagem.
    """
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute("""
            SELECT 
              p.id_parada,
              p.nome AS parada_nome,
              COALESCE(SUM(t.embarques),0) AS pessoas_total
            FROM parada p
            LEFT JOIN (
              SELECT 
                rl.id_parada_origem AS id_parada_origem,
                GREATEST(
                  rl.qtd_pessoas - COALESCE((
                    SELECT rl2.qtd_pessoas
                    FROM registro_lotacao rl2
                    WHERE rl2.id_viagem = rl.id_viagem
                      AND rl2.data_hora < rl.data_hora
                    ORDER BY rl2.data_hora DESC, rl2.id_lotacao DESC
                    LIMIT 1
                  ),0),
                0) AS embarques
              FROM registro_lotacao rl
            ) t ON t.id_parada_origem = p.id_parada
            GROUP BY p.id_parada, p.nome
            ORDER BY p.nome
        """)
        return cur.fetchall()
    finally:
        cur.close(); conn.close()

def pessoas_por_hora_parada(id_parada: int):
    """
    Embarques por hora na parada (0..23).
    Embarques = max(qtd_atual - qtd_anterior_mesma_viagem, 0)
    """
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute("""
            SELECT
              h.hora,
              COALESCE(SUM(h.embarques),0) AS embarques
            FROM (
              SELECT
                HOUR(rl.data_hora) AS hora,
                GREATEST(
                  rl.qtd_pessoas - COALESCE((
                    SELECT rl2.qtd_pessoas
                    FROM registro_lotacao rl2
                    WHERE rl2.id_viagem = rl.id_viagem
                      AND rl2.data_hora < rl.data_hora
                    ORDER BY rl2.data_hora DESC, rl2.id_lotacao DESC
                    LIMIT 1
                  ),0),
                0) AS embarques
              FROM registro_lotacao rl
              WHERE rl.id_parada_origem = %s
            ) AS h
            GROUP BY h.hora
            ORDER BY h.hora
        """, (id_parada,))
        return cur.fetchall()
    finally:
        cur.close(); conn.close()
