#!/bin/bash

# Script de inicialização do Dashboard com SQLite

echo "═══════════════════════════════════════════════════════════"
echo "  🚌 Dashboard de Transporte Público (SQLite)"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Verificar se o banco existe
if [ ! -f "transit.db" ]; then
    echo "⚠️  Banco de dados não encontrado!"
    echo ""
    echo "Execute primeiro: ./init_db.sh"
    echo ""
    exit 1
fi

# Verificar se o virtual environment existe
if [ ! -d ".venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv .venv
    echo "✓ Ambiente virtual criado"
    echo ""
fi

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source .venv/bin/activate

# Instalar dependências
echo "📥 Instalando dependências..."
pip install -q Flask Flask-CORS
echo "✓ Dependências instaladas"
echo ""

echo "═══════════════════════════════════════════════════════════"
echo "  ✅ Iniciando aplicação"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "🌐 Dashboard: http://localhost:5000"
echo "🔌 API: http://localhost:5000/api"
echo ""
echo "Pressione Ctrl+C para parar o servidor"
echo ""

# Iniciar aplicação
python app_sqlite.py
