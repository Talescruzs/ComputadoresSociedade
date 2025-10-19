# 🚀 Guia Rápido - Versão SQLite

## Por que SQLite?

SQLite é mais simples porque:
- ✅ Não requer instalação de servidor
- ✅ Não precisa de configuração
- ✅ Banco de dados em um único arquivo
- ✅ Perfeito para desenvolvimento e testes

---

## 📦 Instalação em 3 Passos

### 1. Criar banco de dados

```bash
./init_db.sh
```

Este script irá:
- Criar o arquivo `transit.db`
- Executar o schema SQL
- Inserir dados de exemplo

### 2. Iniciar aplicação

```bash
./start_sqlite.sh
```

Este script irá:
- Criar ambiente virtual (se necessário)
- Instalar dependências
- Iniciar o servidor Flask

### 3. Acessar

- **Dashboard**: http://localhost:5000
- **API**: http://localhost:5000/api

---

## 📊 Popular com Mais Dados (Opcional)

```bash
source .venv/bin/activate
python populate_db_sqlite.py
```

Isso criará:
- 10 viagens aleatórias
- ~50 registros de lotação
- Simulando horários de pico

---

## 🧪 Testar API

```bash
# Listar linhas
curl http://localhost:5000/api/linhas

# Criar nova viagem
curl -X POST http://localhost:5000/api/viagens \
  -H "Content-Type: application/json" \
  -d '{"id_onibus": 1, "id_linha": 1, "status": "em_andamento"}'

# Ver análises
curl http://localhost:5000/api/analytics/lotacao-por-linha
```

---

## 📁 Arquivos SQLite

```
flask_transit_dashboard/
├── schema_sqlite.sql       # Schema adaptado para SQLite
├── app_sqlite.py           # API adaptada para SQLite
├── init_db.sh              # Script de inicialização do banco
├── start_sqlite.sh         # Script de inicialização da app
├── populate_db_sqlite.py   # Populador de dados
└── transit.db              # Banco de dados (criado automaticamente)
```

---

## 🔄 Diferenças do PostgreSQL

| Característica | PostgreSQL | SQLite |
|---------------|-----------|--------|
| Instalação | Requer servidor | Nenhuma |
| Configuração | Usuário/senha | Nenhuma |
| Arquivo | Múltiplos | Único (.db) |
| Concorrência | Alta | Limitada |
| Uso ideal | Produção | Desenvolvimento/Testes |

---

## 💡 Comandos Úteis

### Ver estrutura do banco

```bash
sqlite3 transit.db ".schema"
```

### Ver dados

```bash
sqlite3 transit.db "SELECT * FROM linha;"
```

### Resetar banco

```bash
rm transit.db
./init_db.sh
```

---

## ⚠️ Solução de Problemas

### Erro: "unable to open database file"

```bash
# Certifique-se de estar no diretório correto
cd /home/vboxuser/Workspace/flask_transit_dashboard
./init_db.sh
```

### Erro: "permission denied"

```bash
chmod +x init_db.sh start_sqlite.sh
```

### Erro: "Flask not found"

```bash
source .venv/bin/activate
pip install Flask Flask-CORS
```

---

## 🔄 Migrar para PostgreSQL

Quando estiver pronto para produção, você pode migrar para PostgreSQL usando o `schema.sql` e `app.py` originais.

---

## 🎉 Tudo Pronto!

Sua aplicação está rodando com SQLite. Todos os recursos funcionam normalmente:

- ✅ API REST completa
- ✅ Dashboard visual
- ✅ Gráficos interativos
- ✅ Análises de lotação

**Próximo passo**: Abra http://localhost:5000 e explore! 🚌
