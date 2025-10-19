# 🚀 Guia Rápido de Início

## Setup em 4 Passos

### 1. Configurar Banco de Dados

```bash
# Criar banco
sudo -u postgres createdb transit_db

# Executar schema
sudo -u postgres psql -d transit_db -f schema.sql
```

### 2. Configurar Variáveis

```bash
cp .env.example .env
# Editar .env se necessário (padrão: postgres/postgres)
```

### 3. Iniciar Aplicação

```bash
./start.sh
```

O script irá:
- ✅ Criar ambiente virtual
- ✅ Instalar dependências
- ✅ Verificar PostgreSQL
- ✅ Iniciar aplicação

### 4. Popular com Dados (Opcional)

Em outro terminal:

```bash
cd /home/vboxuser/Workspace/flask_transit_dashboard
source .venv/bin/activate
python populate_db.py
```

---

## ✅ Verificação

### Dashboard
Abra: **http://localhost:5000**

Você deve ver:
- 4 cards com estatísticas
- 3 gráficos
- Tabela de registros
- Mapa de lotação

### API
Teste: **http://localhost:5000/api/linhas**

```bash
curl http://localhost:5000/api/linhas
```

Resposta esperada:
```json
[
  {
    "id_linha": 1,
    "nome": "Linha 100 - Centro/Terminal"
  },
  {
    "id_linha": 2,
    "nome": "Linha 200 - Aeroporto/Rodoviária"
  },
  {
    "id_linha": 3,
    "nome": "Linha 300 - Shopping/Hospital"
  }
]
```

---

## 🧪 Testar API

```bash
python test_api.py
```

---

## 📖 Exemplos Rápidos

### Criar nova viagem

```bash
curl -X POST http://localhost:5000/api/viagens \
  -H "Content-Type: application/json" \
  -d '{
    "id_onibus": 1,
    "id_linha": 1,
    "status": "em_andamento"
  }'
```

### Registrar lotação

```bash
curl -X POST http://localhost:5000/api/lotacao \
  -H "Content-Type: application/json" \
  -d '{
    "id_viagem": 1,
    "id_parada_origem": 1,
    "id_parada_destino": 2,
    "qtd_pessoas": 35
  }'
```

### Ver análises

```bash
curl http://localhost:5000/api/analytics/lotacao-por-linha
```

---

## 📂 Estrutura

```
flask_transit_dashboard/
├── app.py              # API Flask
├── schema.sql          # Banco de dados
├── start.sh            # Inicialização
├── templates/          # Dashboard HTML
└── static/             # CSS + JavaScript
```

---

## 🔧 Solução de Problemas

### PostgreSQL não está rodando

```bash
sudo systemctl start postgresql
# ou
sudo service postgresql start
```

### Porta 5000 em uso

Edite `app.py`, linha final:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Mudar porta
```

### Erro de conexão com banco

Verifique credenciais em `.env`:
```
DB_NAME=transit_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

---

## 📚 Mais Informações

- **Guia Completo**: `README.md`
- **Exemplos de API**: `API_EXAMPLES.md`
- **Visão Geral**: `PROJETO.md`

---

## 🎉 Pronto!

Dashboard: http://localhost:5000
API: http://localhost:5000/api

Aproveite! 🚌
