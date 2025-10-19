#!/bin/bash

# Script de inicialização do Dashboard de Transporte Público

echo "=== Dashboard de Transporte Público ==="
echo ""

# Verificar se o virtual environment existe
if [ ! -d ".venv" ]; then
    echo "Criando ambiente virtual..."
    uv venv
    echo "✓ Ambiente virtual criado"
fi

# Ativar ambiente virtual
echo "Ativando ambiente virtual..."
source .venv/bin/activate

# Instalar dependências
echo "Instalando dependências..."
uv pip install -r requirements.txt
echo "✓ Dependências instaladas"

# Verificar se o arquivo .env existe
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠ Arquivo .env não encontrado!"
    echo "Copiando .env.example para .env..."
    cp .env.example .env
    echo "Por favor, edite o arquivo .env com suas credenciais do PostgreSQL"
    echo ""
fi

# Verificar se PostgreSQL está rodando
if ! pg_isready -q; then
    echo ""
    echo "⚠ PostgreSQL não está rodando!"
    echo "Por favor, inicie o PostgreSQL antes de executar a aplicação"
    echo ""
    exit 1
fi

echo ""
echo "=== Informações Importantes ==="
echo "1. Certifique-se de que o banco 'transit_db' existe"
echo "2. Execute 'psql -U postgres -d transit_db -f schema.sql' para criar as tabelas"
echo "3. Execute 'python populate_db.py' para popular com dados de exemplo"
echo ""
echo "Iniciando aplicação Flask..."
echo "Dashboard disponível em: http://localhost:5000"
echo "API disponível em: http://localhost:5000/api"
echo ""
echo "Pressione Ctrl+C para parar o servidor"
echo ""

# Iniciar aplicação
python app.py
