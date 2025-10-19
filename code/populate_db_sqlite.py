"""
Script para popular o banco de dados SQLite com dados de exemplo
"""
import sqlite3
from datetime import datetime, timedelta
import random

DB_PATH = 'transit.db'

def populate_database():
    """Popula o banco com dados de exemplo"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    print("Criando viagens de exemplo...")
    
    # Criar algumas viagens
    now = datetime.now()
    viagens_ids = []
    
    for i in range(10):
        data_inicio = now - timedelta(days=random.randint(0, 7), hours=random.randint(6, 20))
        cur.execute(
            """INSERT INTO viagem (id_onibus, id_linha, data_hora_inicio, status) 
               VALUES (?, ?, ?, ?)""",
            (random.randint(1, 3), random.randint(1, 3), data_inicio.isoformat(), 'em_andamento')
        )
        viagem_id = cur.lastrowid
        viagens_ids.append((viagem_id, data_inicio))
        print(f"  Viagem {viagem_id} criada")
    
    print("\nCriando registros de lotação...")
    
    # Criar registros de lotação para cada viagem
    for viagem_id, data_inicio in viagens_ids:
        # Simular registros em diferentes trechos
        num_registros = random.randint(3, 8)
        
        for i in range(num_registros):
            origem = random.randint(1, 6)
            destino = random.randint(1, 6)
            if destino == origem:
                destino = (destino % 6) + 1
            
            # Simular variação de lotação ao longo do dia
            hora = data_inicio.hour
            if 7 <= hora <= 9 or 17 <= hora <= 19:  # Horários de pico
                qtd_pessoas = random.randint(30, 60)
            else:
                qtd_pessoas = random.randint(10, 35)
            
            data_registro = data_inicio + timedelta(minutes=i * 15)
            
            cur.execute(
                """INSERT INTO registro_lotacao 
                   (id_viagem, id_parada_origem, id_parada_destino, data_hora, qtd_pessoas) 
                   VALUES (?, ?, ?, ?, ?)""",
                (viagem_id, origem, destino, data_registro.isoformat(), qtd_pessoas)
            )
            print(f"  Registro de lotação criado para viagem {viagem_id}: {qtd_pessoas} pessoas")
    
    conn.commit()
    cur.close()
    conn.close()
    
    print("\n✓ Banco de dados populado com sucesso!")
    print(f"  - {len(viagens_ids)} viagens criadas")
    print(f"  - Aproximadamente {len(viagens_ids) * 5} registros de lotação criados")

if __name__ == '__main__':
    try:
        populate_database()
    except Exception as e:
        print(f"Erro ao popular banco de dados: {e}")
        print("\nCertifique-se de que:")
        print("  1. O banco 'transit.db' existe")
        print("  2. Execute './init_db.sh' primeiro")
