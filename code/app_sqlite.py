from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Configuração do banco de dados SQLite
DB_PATH = os.path.join(os.path.dirname(__file__), 'transit.db')

def get_db_connection():
    """Cria conexão com o banco de dados SQLite"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Para retornar dicionários
    return conn

def dict_from_row(row):
    """Converte Row do SQLite em dicionário"""
    return dict(zip(row.keys(), row))

# ==================== CRUD para ÔNIBUS ====================

@app.route('/api/onibus', methods=['GET'])
def get_onibus():
    """Lista todos os ônibus"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM onibus ORDER BY id_onibus')
    onibus = [dict_from_row(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(onibus)

@app.route('/api/onibus/<int:id>', methods=['GET'])
def get_onibus_by_id(id):
    """Busca um ônibus por ID"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM onibus WHERE id_onibus = ?', (id,))
    onibus = cur.fetchone()
    conn.close()
    if onibus:
        return jsonify(dict_from_row(onibus))
    return jsonify({'error': 'Ônibus não encontrado'}), 404

@app.route('/api/onibus', methods=['POST'])
def create_onibus():
    """Cria novo ônibus"""
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            'INSERT INTO onibus (placa, capacidade, data_ultima_manutencao) VALUES (?, ?, ?)',
            (data['placa'], data['capacidade'], data.get('data_ultima_manutencao'))
        )
        conn.commit()
        onibus_id = cur.lastrowid
        cur.execute('SELECT * FROM onibus WHERE id_onibus = ?', (onibus_id,))
        onibus = dict_from_row(cur.fetchone())
        conn.close()
        return jsonify(onibus), 201
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/onibus/<int:id>', methods=['PUT'])
def update_onibus(id):
    """Atualiza um ônibus"""
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            'UPDATE onibus SET placa = ?, capacidade = ?, data_ultima_manutencao = ? WHERE id_onibus = ?',
            (data['placa'], data['capacidade'], data.get('data_ultima_manutencao'), id)
        )
        conn.commit()
        if cur.rowcount > 0:
            cur.execute('SELECT * FROM onibus WHERE id_onibus = ?', (id,))
            onibus = dict_from_row(cur.fetchone())
            conn.close()
            return jsonify(onibus)
        conn.close()
        return jsonify({'error': 'Ônibus não encontrado'}), 404
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/onibus/<int:id>', methods=['DELETE'])
def delete_onibus(id):
    """Deleta um ônibus"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM onibus WHERE id_onibus = ?', (id,))
    affected = cur.rowcount
    conn.commit()
    conn.close()
    if affected > 0:
        return jsonify({'message': 'Ônibus deletado com sucesso'}), 200
    return jsonify({'error': 'Ônibus não encontrado'}), 404

# ==================== CRUD para LINHA ====================

@app.route('/api/linhas', methods=['GET'])
def get_linhas():
    """Lista todas as linhas"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM linha ORDER BY id_linha')
    linhas = [dict_from_row(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(linhas)

@app.route('/api/linhas/<int:id>', methods=['GET'])
def get_linha_by_id(id):
    """Busca uma linha por ID"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM linha WHERE id_linha = ?', (id,))
    linha = cur.fetchone()
    conn.close()
    if linha:
        return jsonify(dict_from_row(linha))
    return jsonify({'error': 'Linha não encontrada'}), 404

@app.route('/api/linhas', methods=['POST'])
def create_linha():
    """Cria nova linha"""
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO linha (nome) VALUES (?)', (data['nome'],))
        conn.commit()
        linha_id = cur.lastrowid
        cur.execute('SELECT * FROM linha WHERE id_linha = ?', (linha_id,))
        linha = dict_from_row(cur.fetchone())
        conn.close()
        return jsonify(linha), 201
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/linhas/<int:id>', methods=['PUT'])
def update_linha(id):
    """Atualiza uma linha"""
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('UPDATE linha SET nome = ? WHERE id_linha = ?', (data['nome'], id))
        conn.commit()
        if cur.rowcount > 0:
            cur.execute('SELECT * FROM linha WHERE id_linha = ?', (id,))
            linha = dict_from_row(cur.fetchone())
            conn.close()
            return jsonify(linha)
        conn.close()
        return jsonify({'error': 'Linha não encontrada'}), 404
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/linhas/<int:id>', methods=['DELETE'])
def delete_linha(id):
    """Deleta uma linha"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM linha WHERE id_linha = ?', (id,))
    affected = cur.rowcount
    conn.commit()
    conn.close()
    if affected > 0:
        return jsonify({'message': 'Linha deletada com sucesso'}), 200
    return jsonify({'error': 'Linha não encontrada'}), 404

# ==================== CRUD para PARADA ====================

@app.route('/api/paradas', methods=['GET'])
def get_paradas():
    """Lista todas as paradas"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM parada ORDER BY id_parada')
    paradas = [dict_from_row(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(paradas)

@app.route('/api/paradas/<int:id>', methods=['GET'])
def get_parada_by_id(id):
    """Busca uma parada por ID"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM parada WHERE id_parada = ?', (id,))
    parada = cur.fetchone()
    conn.close()
    if parada:
        return jsonify(dict_from_row(parada))
    return jsonify({'error': 'Parada não encontrada'}), 404

@app.route('/api/paradas', methods=['POST'])
def create_parada():
    """Cria nova parada"""
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            'INSERT INTO parada (nome, localizacao) VALUES (?, ?)',
            (data['nome'], data['localizacao'])
        )
        conn.commit()
        parada_id = cur.lastrowid
        cur.execute('SELECT * FROM parada WHERE id_parada = ?', (parada_id,))
        parada = dict_from_row(cur.fetchone())
        conn.close()
        return jsonify(parada), 201
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/paradas/<int:id>', methods=['PUT'])
def update_parada(id):
    """Atualiza uma parada"""
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            'UPDATE parada SET nome = ?, localizacao = ? WHERE id_parada = ?',
            (data['nome'], data['localizacao'], id)
        )
        conn.commit()
        if cur.rowcount > 0:
            cur.execute('SELECT * FROM parada WHERE id_parada = ?', (id,))
            parada = dict_from_row(cur.fetchone())
            conn.close()
            return jsonify(parada)
        conn.close()
        return jsonify({'error': 'Parada não encontrada'}), 404
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/paradas/<int:id>', methods=['DELETE'])
def delete_parada(id):
    """Deleta uma parada"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM parada WHERE id_parada = ?', (id,))
    affected = cur.rowcount
    conn.commit()
    conn.close()
    if affected > 0:
        return jsonify({'message': 'Parada deletada com sucesso'}), 200
    return jsonify({'error': 'Parada não encontrada'}), 404

# ==================== CRUD para VIAGEM ====================

@app.route('/api/viagens', methods=['GET'])
def get_viagens():
    """Lista todas as viagens"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT v.*, o.placa, l.nome as linha_nome 
        FROM viagem v
        JOIN onibus o ON v.id_onibus = o.id_onibus
        JOIN linha l ON v.id_linha = l.id_linha
        ORDER BY v.data_hora_inicio DESC
    ''')
    viagens = [dict_from_row(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(viagens)

@app.route('/api/viagens/<int:id>', methods=['GET'])
def get_viagem_by_id(id):
    """Busca uma viagem por ID"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT v.*, o.placa, l.nome as linha_nome 
        FROM viagem v
        JOIN onibus o ON v.id_onibus = o.id_onibus
        JOIN linha l ON v.id_linha = l.id_linha
        WHERE v.id_viagem = ?
    ''', (id,))
    viagem = cur.fetchone()
    conn.close()
    if viagem:
        return jsonify(dict_from_row(viagem))
    return jsonify({'error': 'Viagem não encontrada'}), 404

@app.route('/api/viagens', methods=['POST'])
def create_viagem():
    """Cria nova viagem"""
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            '''INSERT INTO viagem (id_onibus, id_linha, data_hora_inicio, data_hora_fim, status) 
               VALUES (?, ?, ?, ?, ?)''',
            (data['id_onibus'], data['id_linha'], data.get('data_hora_inicio', datetime.now().isoformat()),
             data.get('data_hora_fim'), data.get('status', 'em_andamento'))
        )
        conn.commit()
        viagem_id = cur.lastrowid
        cur.execute('SELECT * FROM viagem WHERE id_viagem = ?', (viagem_id,))
        viagem = dict_from_row(cur.fetchone())
        conn.close()
        return jsonify(viagem), 201
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/viagens/<int:id>', methods=['PUT'])
def update_viagem(id):
    """Atualiza uma viagem"""
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            '''UPDATE viagem SET id_onibus = ?, id_linha = ?, data_hora_inicio = ?, 
               data_hora_fim = ?, status = ? WHERE id_viagem = ?''',
            (data['id_onibus'], data['id_linha'], data['data_hora_inicio'],
             data.get('data_hora_fim'), data['status'], id)
        )
        conn.commit()
        if cur.rowcount > 0:
            cur.execute('SELECT * FROM viagem WHERE id_viagem = ?', (id,))
            viagem = dict_from_row(cur.fetchone())
            conn.close()
            return jsonify(viagem)
        conn.close()
        return jsonify({'error': 'Viagem não encontrada'}), 404
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/viagens/<int:id>', methods=['DELETE'])
def delete_viagem(id):
    """Deleta uma viagem"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM viagem WHERE id_viagem = ?', (id,))
    affected = cur.rowcount
    conn.commit()
    conn.close()
    if affected > 0:
        return jsonify({'message': 'Viagem deletada com sucesso'}), 200
    return jsonify({'error': 'Viagem não encontrada'}), 404

# ==================== CRUD para REGISTRO DE LOTAÇÃO ====================

@app.route('/api/lotacao', methods=['GET'])
def get_lotacoes():
    """Lista todos os registros de lotação"""
    conn = get_db_connection()
    cur = conn.cursor()
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
    lotacoes = [dict_from_row(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(lotacoes)

@app.route('/api/lotacao/<int:id>', methods=['GET'])
def get_lotacao_by_id(id):
    """Busca um registro de lotação por ID"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT rl.*, 
               po.nome as parada_origem_nome,
               pd.nome as parada_destino_nome
        FROM registro_lotacao rl
        JOIN parada po ON rl.id_parada_origem = po.id_parada
        LEFT JOIN parada pd ON rl.id_parada_destino = pd.id_parada
        WHERE rl.id_lotacao = ?
    ''', (id,))
    lotacao = cur.fetchone()
    conn.close()
    if lotacao:
        return jsonify(dict_from_row(lotacao))
    return jsonify({'error': 'Registro não encontrado'}), 404

@app.route('/api/lotacao', methods=['POST'])
def create_lotacao():
    """Cria novo registro de lotação"""
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            '''INSERT INTO registro_lotacao (id_viagem, id_parada_origem, id_parada_destino, data_hora, qtd_pessoas) 
               VALUES (?, ?, ?, ?, ?)''',
            (data['id_viagem'], data['id_parada_origem'], data.get('id_parada_destino'),
             data.get('data_hora', datetime.now().isoformat()), data['qtd_pessoas'])
        )
        conn.commit()
        lotacao_id = cur.lastrowid
        cur.execute('SELECT * FROM registro_lotacao WHERE id_lotacao = ?', (lotacao_id,))
        lotacao = dict_from_row(cur.fetchone())
        conn.close()
        return jsonify(lotacao), 201
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/lotacao/<int:id>', methods=['PUT'])
def update_lotacao(id):
    """Atualiza um registro de lotação"""
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            '''UPDATE registro_lotacao SET id_viagem = ?, id_parada_origem = ?, 
               id_parada_destino = ?, data_hora = ?, qtd_pessoas = ? 
               WHERE id_lotacao = ?''',
            (data['id_viagem'], data['id_parada_origem'], data.get('id_parada_destino'),
             data['data_hora'], data['qtd_pessoas'], id)
        )
        conn.commit()
        if cur.rowcount > 0:
            cur.execute('SELECT * FROM registro_lotacao WHERE id_lotacao = ?', (id,))
            lotacao = dict_from_row(cur.fetchone())
            conn.close()
            return jsonify(lotacao)
        conn.close()
        return jsonify({'error': 'Registro não encontrado'}), 404
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/lotacao/<int:id>', methods=['DELETE'])
def delete_lotacao(id):
    """Deleta um registro de lotação"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM registro_lotacao WHERE id_lotacao = ?', (id,))
    affected = cur.rowcount
    conn.commit()
    conn.close()
    if affected > 0:
        return jsonify({'message': 'Registro deletado com sucesso'}), 200
    return jsonify({'error': 'Registro não encontrado'}), 404

# ==================== ENDPOINTS DE ANÁLISE ====================

@app.route('/api/analytics/lotacao-por-linha', methods=['GET'])
def lotacao_por_linha():
    """Retorna dados de lotação agregados por linha"""
    conn = get_db_connection()
    cur = conn.cursor()
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
    data = [dict_from_row(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(data)

@app.route('/api/analytics/lotacao-por-trecho', methods=['GET'])
def lotacao_por_trecho():
    """Retorna dados de lotação por trecho (origem-destino)"""
    conn = get_db_connection()
    cur = conn.cursor()
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
    data = [dict_from_row(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(data)

@app.route('/api/analytics/lotacao-horaria', methods=['GET'])
def lotacao_horaria():
    """Retorna dados de lotação por horário do dia"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT 
            CAST(strftime('%H', rl.data_hora) AS INTEGER) as hora,
            AVG(rl.qtd_pessoas) as media_pessoas,
            COUNT(rl.id_lotacao) as total_registros
        FROM registro_lotacao rl
        GROUP BY CAST(strftime('%H', rl.data_hora) AS INTEGER)
        ORDER BY hora
    ''')
    data = [dict_from_row(row) for row in cur.fetchall()]
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
