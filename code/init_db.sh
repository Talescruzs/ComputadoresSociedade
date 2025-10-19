#!/bin/bash

# Script de inicialização do banco de dados SQLite

echo "═══════════════════════════════════════════════════════════"
echo "  🗄️  Inicializando banco de dados SQLite"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Remover banco antigo se existir
if [ -f "transit.db" ]; then
    echo "⚠️  Banco de dados existente encontrado"
    read -p "Deseja apagar e criar um novo? (s/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        rm transit.db
        echo "✓ Banco antigo removido"
    else
        echo "Mantendo banco existente"
        exit 0
    fi
fi

# Criar banco de dados
echo "Criando banco de dados..."
sqlite3 transit.db < schema_sqlite.sql

if [ $? -eq 0 ]; then
    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo "  ✅ Banco de dados criado com sucesso!"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
    echo "📊 Dados incluídos:"
    echo "  • 3 ônibus"
    echo "  • 3 linhas"
    echo "  • 6 paradas"
    echo "  • 9 rotas"
    echo ""
    echo "🚀 Próximo passo:"
    echo "  Execute: ./start_sqlite.sh"
    echo ""
else
    echo ""
    echo "❌ Erro ao criar banco de dados"
    exit 1
fi
