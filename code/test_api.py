"""
Script de teste para a API do Dashboard de Transporte Público
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000/api"

def print_response(title, response):
    """Imprime resposta formatada"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    try:
        print(f"Resposta:\n{json.dumps(response.json(), indent=2, default=str)}")
    except:
        print(f"Resposta: {response.text}")

def test_health():
    """Testa endpoint de health check"""
    print("\n🏥 Testando Health Check...")
    response = requests.get("http://localhost:5000/health")
    print_response("Health Check", response)
    return response.status_code == 200

def test_onibus():
    """Testa CRUD de ônibus"""
    print("\n🚌 Testando CRUD de Ônibus...")
    
    # Listar
    response = requests.get(f"{BASE_URL}/onibus")
    print_response("Listar Ônibus", response)
    
    # Criar
    novo_onibus = {
        "placa": f"TEST-{datetime.now().strftime('%H%M')}",
        "capacidade": 50,
        "data_ultima_manutencao": "2024-10-15 10:00:00"
    }
    response = requests.post(f"{BASE_URL}/onibus", json=novo_onibus)
    print_response("Criar Ônibus", response)
    
    if response.status_code == 201:
        onibus_id = response.json()['id_onibus']
        
        # Buscar por ID
        response = requests.get(f"{BASE_URL}/onibus/{onibus_id}")
        print_response(f"Buscar Ônibus #{onibus_id}", response)
        
        # Atualizar
        atualizado = novo_onibus.copy()
        atualizado['capacidade'] = 55
        response = requests.put(f"{BASE_URL}/onibus/{onibus_id}", json=atualizado)
        print_response(f"Atualizar Ônibus #{onibus_id}", response)
        
        # Deletar
        response = requests.delete(f"{BASE_URL}/onibus/{onibus_id}")
        print_response(f"Deletar Ônibus #{onibus_id}", response)

def test_linhas():
    """Testa CRUD de linhas"""
    print("\n🚏 Testando CRUD de Linhas...")
    
    # Listar
    response = requests.get(f"{BASE_URL}/linhas")
    print_response("Listar Linhas", response)
    
    # Criar
    nova_linha = {
        "nome": f"Linha Teste - {datetime.now().strftime('%H:%M:%S')}"
    }
    response = requests.post(f"{BASE_URL}/linhas", json=nova_linha)
    print_response("Criar Linha", response)
    
    if response.status_code == 201:
        linha_id = response.json()['id_linha']
        
        # Buscar por ID
        response = requests.get(f"{BASE_URL}/linhas/{linha_id}")
        print_response(f"Buscar Linha #{linha_id}", response)
        
        # Deletar
        response = requests.delete(f"{BASE_URL}/linhas/{linha_id}")
        print_response(f"Deletar Linha #{linha_id}", response)

def test_paradas():
    """Testa CRUD de paradas"""
    print("\n📍 Testando CRUD de Paradas...")
    
    # Listar
    response = requests.get(f"{BASE_URL}/paradas")
    print_response("Listar Paradas", response)
    
    # Criar
    nova_parada = {
        "nome": f"Parada Teste {datetime.now().strftime('%H:%M')}",
        "localizacao": "Rua Teste, 123"
    }
    response = requests.post(f"{BASE_URL}/paradas", json=nova_parada)
    print_response("Criar Parada", response)
    
    if response.status_code == 201:
        parada_id = response.json()['id_parada']
        
        # Buscar por ID
        response = requests.get(f"{BASE_URL}/paradas/{parada_id}")
        print_response(f"Buscar Parada #{parada_id}", response)
        
        # Deletar
        response = requests.delete(f"{BASE_URL}/paradas/{parada_id}")
        print_response(f"Deletar Parada #{parada_id}", response)

def test_viagens():
    """Testa CRUD de viagens"""
    print("\n🚍 Testando CRUD de Viagens...")
    
    # Listar
    response = requests.get(f"{BASE_URL}/viagens")
    print_response("Listar Viagens", response)
    
    viagens = response.json()
    if viagens:
        # Buscar primeira viagem
        viagem_id = viagens[0]['id_viagem']
        response = requests.get(f"{BASE_URL}/viagens/{viagem_id}")
        print_response(f"Buscar Viagem #{viagem_id}", response)

def test_lotacao():
    """Testa CRUD de registros de lotação"""
    print("\n👥 Testando CRUD de Registros de Lotação...")
    
    # Listar
    response = requests.get(f"{BASE_URL}/lotacao")
    print_response("Listar Registros de Lotação", response)

def test_analytics():
    """Testa endpoints de análise"""
    print("\n📊 Testando Endpoints de Análise...")
    
    # Lotação por linha
    response = requests.get(f"{BASE_URL}/analytics/lotacao-por-linha")
    print_response("Lotação por Linha", response)
    
    # Lotação por trecho
    response = requests.get(f"{BASE_URL}/analytics/lotacao-por-trecho")
    print_response("Lotação por Trecho (Top 20)", response)
    
    # Lotação por horário
    response = requests.get(f"{BASE_URL}/analytics/lotacao-horaria")
    print_response("Lotação por Horário", response)

def main():
    """Executa todos os testes"""
    print("="*60)
    print("🧪 TESTES DA API - Dashboard de Transporte Público")
    print("="*60)
    
    try:
        # Health check
        if not test_health():
            print("\n❌ API não está respondendo!")
            print("Certifique-se de que o servidor está rodando em http://localhost:5000")
            return
        
        print("\n✅ API está online!")
        
        # Testes CRUD
        test_onibus()
        test_linhas()
        test_paradas()
        test_viagens()
        test_lotacao()
        
        # Testes de análise
        test_analytics()
        
        print("\n" + "="*60)
        print("✅ Todos os testes concluídos!")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Erro de conexão!")
        print("Certifique-se de que o servidor está rodando em http://localhost:5000")
    except Exception as e:
        print(f"\n❌ Erro durante os testes: {e}")

if __name__ == '__main__':
    main()
