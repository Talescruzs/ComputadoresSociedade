from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Configuração do banco de dados
DB_CONFIG = {
    'dbname': os.environ.get('DB_NAME', 'transit_db'),
    'user': os.environ.get('DB_USER', 'postgres'),
    'password': os.environ.get('DB_PASSWORD', 'postgres'),
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': os.environ.get('DB_PORT', '5432')
}

def get_db_connection():
    """Cria conexão com o banco de dados"""
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

# ==================== CRUD para ÔNIBUS ====================

@app.route('/api/onibus', methods=['GET'])
def get_onibus():
    """Lista todos os ônibus"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM onibus ORDER BY id_onibus')
    onibus = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(onibus)

@app.route('/api/onibus/<int:id>', methods=['GET'])
def get_onibus_by_id(id):
    """Busca um ônibus por ID"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM onibus WHERE id_onibus = %s', (id,))
    onibus = cur.fetchone()
    cur.close()
    conn.close()
    if onibus:
        return jsonify(onibus)
    return jsonify({'error': 'Ônibus não encontrado'}), 404

@app.route('/api/onibus', methods=['POST'])
def create_onibus():
    """Cria novo ônibus"""
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute(
            'INSERT INTO onibus (placa, capacidade, data_ultima_manutencao) VALUES (%s, %s, %s) RETURNING *',
            (data['placa'], data['capacidade'], data.get('data_ultima_manutencao'))
        )
        onibus = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(onibus), 201
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/onibus/<int:id>', methods=['PUT'])
def update_onibus(id):
    """Atualiza um ônibus"""
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute(
            'UPDATE onibus SET placa = %s, capacidade = %s, data_ultima_manutencao = %s WHERE id_onibus = %s RETURNING *',
            (data['placa'], data['capacidade'], data.get('data_ultima_manutencao'), id)
        )
        onibus = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        if onibus:
            return jsonify(onibus)
        return jsonify({'error': 'Ônibus não encontrado'}), 404
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/onibus/<int:id>', methods=['DELETE'])
def delete_onibus(id):
    """Deleta um ônibus"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM onibus WHERE id_onibus = %s', (id,))
    affected = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    if affected > 0:
        return jsonify({'message': 'Ônibus deletado com sucesso'}), 200
    return jsonify({'error': 'Ônibus não encontrado'}), 404

# ==================== CRUD para LINHA ====================

@app.route('/api/linhas', methods=['GET'])
def get_linhas():
    """Lista todas as linhas"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM linha ORDER BY id_linha')
    linhas = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(linhas)

@app.route('/api/linhas/<int:id>', methods=['GET'])
def get_linha_by_id(id):
    """Busca uma linha por ID"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM linha WHERE id_linha = %s', (id,))
    linha = cur.fetchone()
    cur.close()
    conn.close()
    if linha:
        return jsonify(linha)
    return jsonify({'error': 'Linha não encontrada'}), 404

@app.route('/api/linhas', methods=['POST'])
def create_linha():
    """Cria nova linha"""
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute('INSERT INTO linha (nome) VALUES (%s) RETURNING *', (data['nome'],))
        linha = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(linha), 201
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/linhas/<int:id>', methods=['PUT'])
def update_linha(id):
    """Atualiza uma linha"""
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute('UPDATE linha SET nome = %s WHERE id_linha = %s RETURNING *', (data['nome'], id))
        linha = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        if linha:
            return jsonify(linha)
        return jsonify({'error': 'Linha não encontrada'}), 404
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/linhas/<int:id>', methods=['DELETE'])
def delete_linha(id):
    """Deleta uma linha"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM linha WHERE id_linha = %s', (id,))
    affected = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    if affected > 0:
        return jsonify({'message': 'Linha deletada com sucesso'}), 200
    return jsonify({'error': 'Linha não encontrada'}), 404

# ==================== CRUD para PARADA ====================

@app.route('/api/paradas', methods=['GET'])
def get_paradas():
    """Lista todas as paradas"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM parada ORDER BY id_parada')
    paradas = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(paradas)

@app.route('/api/paradas/<int:id>', methods=['GET'])
def get_parada_by_id(id):
    """Busca uma parada por ID"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM parada WHERE id_parada = %s', (id,))
    parada = cur.fetchone()
    cur.close()
    conn.close()
    if parada:
        return jsonify(parada)
    return jsonify({'error': 'Parada não encontrada'}), 404

@app.route('/api/paradas', methods=['POST'])
def create_parada():
    """Cria nova parada"""
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute(
            'INSERT INTO parada (nome, localizacao) VALUES (%s, %s) RETURNING *',
            (data['nome'], data['localizacao'])
        )
        parada = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(parada), 201
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/paradas/<int:id>', methods=['PUT'])
def update_parada(id):
    """Atualiza uma parada"""
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute(
            'UPDATE parada SET nome = %s, localizacao = %s WHERE id_parada = %s RETURNING *',
            (data['nome'], data['localizacao'], id)
        )
        parada = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        if parada:
            return jsonify(parada)
        return jsonify({'error': 'Parada não encontrada'}), 404
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/paradas/<int:id>', methods=['DELETE'])
def delete_parada(id):
    """Deleta uma parada"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM parada WHERE id_parada = %s', (id,))
    affected = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    if affected > 0:
        return jsonify({'message': 'Parada deletada com sucesso'}), 200
    return jsonify({'error': 'Parada não encontrada'}), 404

# ==================== CRUD para VIAGEM ====================

@app.route('/api/viagens', methods=['GET'])
def get_viagens():
    """Lista todas as viagens"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        SELECT v.*, o.placa, l.nome as linha_nome 
        FROM viagem v
        JOIN onibus o ON v.id_onibus = o.id_onibus
        JOIN linha l ON v.id_linha = l.id_linha
        ORDER BY v.data_hora_inicio DESC
    ''')
    viagens = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(viagens)

@app.route('/api/viagens/<int:id>', methods=['GET'])
def get_viagem_by_id(id):
    """Busca uma viagem por ID"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        SELECT v.*, o.placa, l.nome as linha_nome 
        FROM viagem v
        JOIN onibus o ON v.id_onibus = o.id_onibus
        JOIN linha l ON v.id_linha = l.id_linha
        WHERE v.id_viagem = %s
    ''', (id,))
    viagem = cur.fetchone()
    cur.close()
    conn.close()
    if viagem:
        return jsonify(viagem)
    return jsonify({'error': 'Viagem não encontrada'}), 404

@app.route('/api/viagens', methods=['POST'])
def create_viagem():
    """Cria nova viagem"""
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute(
            '''INSERT INTO viagem (id_onibus, id_linha, data_hora_inicio, data_hora_fim, status) 
               VALUES (%s, %s, %s, %s, %s) RETURNING *''',
            (data['id_onibus'], data['id_linha'], data.get('data_hora_inicio', datetime.now()),
             data.get('data_hora_fim'), data.get('status', 'em_andamento'))
        )
        viagem = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(viagem), 201
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/viagens/<int:id>', methods=['PUT'])
def update_viagem(id):
    """Atualiza uma viagem"""
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute(
            '''UPDATE viagem SET id_onibus = %s, id_linha = %s, data_hora_inicio = %s, 
               data_hora_fim = %s, status = %s WHERE id_viagem = %s RETURNING *''',
            (data['id_onibus'], data['id_linha'], data['data_hora_inicio'],
             data.get('data_hora_fim'), data['status'], id)
        )
        viagem = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        if viagem:
            return jsonify(viagem)
        return jsonify({'error': 'Viagem não encontrada'}), 404
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/viagens/<int:id>', methods=['DELETE'])
def delete_viagem(id):
    """Deleta uma viagem"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM viagem WHERE id_viagem = %s', (id,))
    affected = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    if affected > 0:
        return jsonify({'message': 'Viagem deletada com sucesso'}), 200
    return jsonify({'error': 'Viagem não encontrada'}), 404

# ==================== CRUD para REGISTRO DE LOTAÇÃO ====================

@app.route('/api/lotacao', methods=['GET'])
def get_lotacoes():
    """Lista todos os registros de lotação"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
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
    ''')
    lotacoes = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(lotacoes)

@app.route('/api/lotacao/<int:id>', methods=['GET'])
def get_lotacao_by_id(id):
    """Busca um registro de lotação por ID"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        SELECT rl.*, 
               po.nome as parada_origem_nome,
               pd.nome as parada_destino_nome
        FROM registro_lotacao rl
        JOIN parada po ON rl.id_parada_origem = po.id_parada
        LEFT JOIN parada pd ON rl.id_parada_destino = pd.id_parada
        WHERE rl.id_lotacao = %s
    ''', (id,))
    lotacao = cur.fetchone()
    cur.close()
    conn.close()
    if lotacao:
        return jsonify(lotacao)
    return jsonify({'error': 'Registro não encontrado'}), 404

@app.route('/api/lotacao', methods=['POST'])
def create_lotacao():
    """Cria novo registro de lotação"""
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute(
            '''INSERT INTO registro_lotacao (id_viagem, id_parada_origem, id_parada_destino, data_hora, qtd_pessoas) 
               VALUES (%s, %s, %s, %s, %s) RETURNING *''',
            (data['id_viagem'], data['id_parada_origem'], data.get('id_parada_destino'),
             data.get('data_hora', datetime.now()), data['qtd_pessoas'])
        )
        lotacao = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(lotacao), 201
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/lotacao/<int:id>', methods=['PUT'])
def update_lotacao(id):
    """Atualiza um registro de lotação"""
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute(
            '''UPDATE registro_lotacao SET id_viagem = %s, id_parada_origem = %s, 
               id_parada_destino = %s, data_hora = %s, qtd_pessoas = %s 
               WHERE id_lotacao = %s RETURNING *''',
            (data['id_viagem'], data['id_parada_origem'], data.get('id_parada_destino'),
             data['data_hora'], data['qtd_pessoas'], id)
        )
        lotacao = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        if lotacao:
            return jsonify(lotacao)
        return jsonify({'error': 'Registro não encontrado'}), 404
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/lotacao/<int:id>', methods=['DELETE'])
def delete_lotacao(id):
    """Deleta um registro de lotação"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM registro_lotacao WHERE id_lotacao = %s', (id,))
    affected = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    if affected > 0:
        return jsonify({'message': 'Registro deletado com sucesso'}), 200
    return jsonify({'error': 'Registro não encontrado'}), 404

# ==================== ENDPOINTS DE ANÁLISE ====================

@app.route('/api/analytics/lotacao-por-linha', methods=['GET'])
def lotacao_por_linha():
    """Retorna dados de lotação agregados por linha"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        SELECT 
            l.id_linha,
            l.nome as linha_nome,
            AVG(rl.qtd_pessoas) as media_pessoas,
            MAX(rl.qtd_pessoas) as max_pessoas,
            MIN(rl.qtd_pessoas) as min_pessoas,
            COUNT(rl.id_lotacao) as total_registros
        FROM registro_lotacao rl
        JOIN viagem v ON rl.id_viagem = v.id_viagem
        JOIN linha l ON v.id_linha = l.id_linha
        GROUP BY l.id_linha, l.nome
        ORDER BY media_pessoas DESC
    ''')
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

@app.route('/api/analytics/lotacao-por-trecho', methods=['GET'])
def lotacao_por_trecho():
    """Retorna dados de lotação por trecho (origem-destino)"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
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
        WHERE rl.id_parada_destino IS NOT NULL
        GROUP BY l.nome, po.nome, pd.nome
        ORDER BY media_pessoas DESC
        LIMIT 20
    ''')
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

@app.route('/api/analytics/lotacao-horaria', methods=['GET'])
def lotacao_horaria():
    """Retorna dados de lotação por horário do dia"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        SELECT 
            EXTRACT(HOUR FROM rl.data_hora) as hora,
            AVG(rl.qtd_pessoas) as media_pessoas,
            COUNT(rl.id_lotacao) as total_registros
        FROM registro_lotacao rl
        GROUP BY EXTRACT(HOUR FROM rl.data_hora)
        ORDER BY hora
    ''')
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

# ==================== DASHBOARD ====================

@app.route('/')
def dashboard():
    """Renderiza o dashboard principal"""
    return render_template('dashboard.html')

@app.route('/health')
def health():
    """Verifica saúde da aplicação"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
