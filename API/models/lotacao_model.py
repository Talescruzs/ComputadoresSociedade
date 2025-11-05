from API.models.db import get_db_connection
from datetime import datetime

def list_all():
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT rl.*, 
               po.nome as parada_origem_nome,
               pd.nome as parada_destino_nome,
               v.id_linha,
               l.nome as linha_nome
        FROM registro_lotacao rl
        JOIN parada po ON rl.id_parada_origem = po.id_parada
        LEFT JOIN parada pd ON rl.id_parada_destino = pd.id_parada
        JOIN viagem v ON rl.id_viagem = v.id_viagem
        JOIN linha l ON v.id_linha = l.id_linha
        ORDER BY rl.data_hora DESC
    """)
    rows = cur.fetchall(); cur.close(); conn.close()
    return rows

def get_by_id(id_):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT rl.*, 
               po.nome as parada_origem_nome,
               pd.nome as parada_destino_nome
        FROM registro_lotacao rl
        JOIN parada po ON rl.id_parada_origem = po.id_parada
        LEFT JOIN parada pd ON rl.id_parada_destino = pd.id_parada
        WHERE rl.id_lotacao = %s
    """, (id_,))
    row = cur.fetchone(); cur.close(); conn.close()
    return row

def create(payload):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute("""
            INSERT INTO registro_lotacao (id_viagem, id_parada_origem, id_parada_destino, data_hora, qtd_pessoas)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            payload["id_viagem"], payload["id_parada_origem"], payload.get("id_parada_destino"),
            payload.get("data_hora", datetime.now()), payload["qtd_pessoas"]
        ))
        new_id = cur.lastrowid; conn.commit()
        cur.execute("""
            SELECT rl.*, 
                   po.nome as parada_origem_nome,
                   pd.nome as parada_destino_nome,
                   v.id_linha,
                   l.nome as linha_nome
            FROM registro_lotacao rl
            JOIN parada po ON rl.id_parada_origem = po.id_parada
            LEFT JOIN parada pd ON rl.id_parada_destino = pd.id_parada
            JOIN viagem v ON rl.id_viagem = v.id_viagem
            JOIN linha l ON v.id_linha = l.id_linha
            WHERE rl.id_lotacao = %s
        """, (new_id,))
        return cur.fetchone()
    finally:
        cur.close(); conn.close()

def update(id_, payload):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute("""
            UPDATE registro_lotacao SET id_viagem=%s, id_parada_origem=%s, id_parada_destino=%s,
                   data_hora=%s, qtd_pessoas=%s
            WHERE id_lotacao=%s
        """, (
            payload["id_viagem"], payload["id_parada_origem"], payload.get("id_parada_destino"),
            payload["data_hora"], payload["qtd_pessoas"], id_
        ))
        conn.commit()
        if cur.rowcount:
            return get_by_id(id_)
        return None
    finally:
        cur.close(); conn.close()

def delete(id_):
    conn = get_db_connection(); cur = conn.cursor()
    cur.execute("DELETE FROM registro_lotacao WHERE id_lotacao = %s", (id_,))
    affected = cur.rowcount; conn.commit(); cur.close(); conn.close()
    return affected > 0

def analytics_lotacao_por_linha():
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT l.id_linha, l.nome as linha_nome,
               AVG(rl.qtd_pessoas) as media_pessoas,
               MAX(rl.qtd_pessoas) as max_pessoas,
               MIN(rl.qtd_pessoas) as min_pessoas,
               COUNT(rl.id_lotacao) as total_registros
        FROM registro_lotacao rl
        JOIN viagem v ON rl.id_viagem = v.id_viagem
        JOIN linha l ON v.id_linha = l.id_linha
        GROUP BY l.id_linha, l.nome
        ORDER BY media_pessoas DESC
    """)
    data = cur.fetchall(); cur.close(); conn.close()
    return data

def analytics_lotacao_por_trecho():
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT l.nome as linha_nome, po.nome as parada_origem, pd.nome as parada_destino,
               AVG(rl.qtd_pessoas) as media_pessoas, MAX(rl.qtd_pessoas) as max_pessoas,
               COUNT(rl.id_lotacao) as total_registros
        FROM registro_lotacao rl
        JOIN viagem v ON rl.id_viagem = v.id_viagem
        JOIN linha l ON v.id_linha = l.id_linha
        JOIN parada po ON rl.id_parada_origem = po.id_parada
        LEFT JOIN parada pd ON rl.id_parada_destino = pd.id_parada
        WHERE rl.id_parada_destino IS NOT NULL
        GROUP BY l.nome, po.nome, pd.nome
        ORDER BY media_pessoas DESC
        LIMIT 20
    """)
    data = cur.fetchall(); cur.close(); conn.close()
    return data

def analytics_lotacao_horaria():
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT EXTRACT(HOUR FROM rl.data_hora) as hora,
               AVG(rl.qtd_pessoas) as media_pessoas,
               COUNT(rl.id_lotacao) as total_registros
        FROM registro_lotacao rl
        GROUP BY EXTRACT(HOUR FROM rl.data_hora)
        ORDER BY hora
    """)
    data = cur.fetchall(); cur.close(); conn.close()
    return data

def analytics_lotacao_horaria_por_linha(id_linha: int):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT 
            EXTRACT(HOUR FROM rl.data_hora) as hora,
            AVG(rl.qtd_pessoas) as media_pessoas,
            COUNT(rl.id_lotacao) as total_registros
        FROM registro_lotacao rl
        JOIN viagem v ON rl.id_viagem = v.id_viagem
        WHERE v.id_linha = %s
        GROUP BY EXTRACT(HOUR FROM rl.data_hora)
        ORDER BY hora
    """, (id_linha,))
    data = cur.fetchall(); cur.close(); conn.close()
    return data

def analytics_trechos_por_linha(id_linha: int, limit: int = 20):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT 
            l.nome as linha_nome,
            po.nome as parada_origem,
            pd.nome as parada_destino,
            AVG(rl.qtd_pessoas) as media_pessoas,
            MAX(rl.qtd_pessoas) as max_pessoas,
            COUNT(rl.id_lotacao) as total_registros
        FROM registro_lotacao rl
        JOIN viagem v ON rl.id_viagem = v.id_viagem
        JOIN linha l ON v.id_linha = l.id_linha
        JOIN parada po ON rl.id_parada_origem = po.id_parada
        LEFT JOIN parada pd ON rl.id_parada_destino = pd.id_parada
        WHERE v.id_linha = %s AND rl.id_parada_destino IS NOT NULL
        GROUP BY l.nome, po.nome, pd.nome
        ORDER BY media_pessoas DESC
        LIMIT %s
    """, (id_linha, limit))
    data = cur.fetchall(); cur.close(); conn.close()
    return data
