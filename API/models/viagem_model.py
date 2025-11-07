from API.models.db import get_db_connection
from datetime import datetime

def list_all():
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT 
            v.id_viagem,
            v.id_onibus,
            v.id_linha,
            v.data_hora_inicio,
            v.data_hora_fim,
            CASE WHEN v.status='em_andamento' THEN 'Ativo' ELSE v.status END AS status,
            o.placa,
            l.nome AS linha_nome
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
        SELECT 
            v.id_viagem,
            v.id_onibus,
            v.id_linha,
            v.data_hora_inicio,
            v.data_hora_fim,
            CASE WHEN v.status='em_andamento' THEN 'Ativo' ELSE v.status END AS status,
            o.placa,
            l.nome AS linha_nome
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
            payload["id_onibus"],
            payload["id_linha"],
            payload.get("data_hora_inicio", datetime.now()),
            payload.get("data_hora_fim"),
            payload.get("status", "Ativo")  # alterado de 'Ativa' / 'em_andamento' para 'Ativo'
        ))
        new_id = cur.lastrowid; conn.commit()
        return get_by_id(new_id)
    finally:
        cur.close(); conn.close()

def update(id_, payload):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute("""
            UPDATE viagem 
               SET id_onibus=%s,
                   id_linha=%s,
                   data_hora_inicio=%s,
                   data_hora_fim=%s,
                   status=%s
             WHERE id_viagem=%s
        """, (
            payload["id_onibus"],
            payload["id_linha"],
            payload["data_hora_inicio"],
            payload.get("data_hora_fim"),
            "Ativo" if payload.get("status") == "em_andamento" else payload.get("status", "Ativo"),
            id_
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

def list_trechos(id_viagem: int):
    """
    Retorna os trechos (registros de lotação) da viagem com capacidade do ônibus.
    """
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute("""
            SELECT
              rl.id_lotacao,
              rl.id_viagem,
              rl.data_hora,
              rl.qtd_pessoas,
              po.id_parada AS parada_origem_id,
              po.nome AS parada_origem_nome,
              pd.id_parada AS parada_destino_id,
              pd.nome AS parada_destino_nome,
              o.capacidade
            FROM registro_lotacao rl
            JOIN parada po ON po.id_parada = rl.id_parada_origem
            LEFT JOIN parada pd ON pd.id_parada = rl.id_parada_destino
            JOIN viagem v ON v.id_viagem = rl.id_viagem
            JOIN onibus o ON o.id_onibus = v.id_onibus
            WHERE rl.id_viagem = %s
            ORDER BY rl.data_hora ASC, rl.id_lotacao ASC
        """, (id_viagem,))
        return cur.fetchall()
    finally:
        cur.close(); conn.close()
