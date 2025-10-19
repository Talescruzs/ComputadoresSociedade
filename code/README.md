# Dashboard de Transporte Público

Sistema completo de gerenciamento de transporte público com API REST e dashboard visual.

## Características

- **API REST completa** com operações CRUD para:
  - Ônibus
  - Linhas
  - Paradas
  - Rotas
  - Viagens
  - Registros de Lotação

- **Dashboard Visual** com:
  - Cards de resumo com estatísticas principais
  - Gráfico de lotação média por linha
  - Gráfico de lotação por horário do dia
  - Top 10 trechos mais lotados
  - Tabela de registros recentes
  - Mapa visual de lotação por linha e trecho

- **Endpoints de Análise**:
  - `/api/analytics/lotacao-por-linha` - Dados agregados por linha
  - `/api/analytics/lotacao-por-trecho` - Dados por trecho (origem-destino)
  - `/api/analytics/lotacao-horaria` - Dados por horário do dia

## Requisitos

- Python 3.8+
- PostgreSQL 12+
- pip ou uv

## Instalação

### 1. Configurar o banco de dados PostgreSQL

```bash
# Criar banco de dados
sudo -u postgres createdb transit_db

# Ou via psql
sudo -u postgres psql
CREATE DATABASE transit_db;
\q
```

### 2. Executar o schema SQL

```bash
sudo -u postgres psql -d transit_db -f schema.sql
```

### 3. Criar ambiente virtual e instalar dependências

```bash
# Usando uv (recomendado)
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Ou usando pip
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

```bash
cp .env.example .env
# Editar .env com suas credenciais do PostgreSQL
```

### 5. Executar a aplicação

```bash
python app.py
```

A aplicação estará disponível em `http://localhost:5000`

## Estrutura do Banco de Dados

### Tabelas

- **onibus**: Informações sobre os veículos
- **linha**: Linhas de transporte
- **parada**: Pontos de parada
- **rota**: Associação entre linhas e paradas
- **viagem**: Viagens realizadas
- **registro_lotacao**: Registros de lotação por viagem e trecho

## Endpoints da API

### Ônibus
- `GET /api/onibus` - Listar todos
- `GET /api/onibus/<id>` - Buscar por ID
- `POST /api/onibus` - Criar novo
- `PUT /api/onibus/<id>` - Atualizar
- `DELETE /api/onibus/<id>` - Deletar

### Linhas
- `GET /api/linhas` - Listar todas
- `GET /api/linhas/<id>` - Buscar por ID
- `POST /api/linhas` - Criar nova
- `PUT /api/linhas/<id>` - Atualizar
- `DELETE /api/linhas/<id>` - Deletar

### Paradas
- `GET /api/paradas` - Listar todas
- `GET /api/paradas/<id>` - Buscar por ID
- `POST /api/paradas` - Criar nova
- `PUT /api/paradas/<id>` - Atualizar
- `DELETE /api/paradas/<id>` - Deletar

### Viagens
- `GET /api/viagens` - Listar todas
- `GET /api/viagens/<id>` - Buscar por ID
- `POST /api/viagens` - Criar nova
- `PUT /api/viagens/<id>` - Atualizar
- `DELETE /api/viagens/<id>` - Deletar

### Registros de Lotação
- `GET /api/lotacao` - Listar todos
- `GET /api/lotacao/<id>` - Buscar por ID
- `POST /api/lotacao` - Criar novo
- `PUT /api/lotacao/<id>` - Atualizar
- `DELETE /api/lotacao/<id>` - Deletar

### Análises
- `GET /api/analytics/lotacao-por-linha` - Estatísticas por linha
- `GET /api/analytics/lotacao-por-trecho` - Estatísticas por trecho
- `GET /api/analytics/lotacao-horaria` - Estatísticas por horário

## Exemplos de Uso da API

### Criar um novo ônibus
```bash
curl -X POST http://localhost:5000/api/onibus \
  -H "Content-Type: application/json" \
  -d '{
    "placa": "XYZ-9999",
    "capacidade": 50,
    "data_ultima_manutencao": "2024-10-01 10:00:00"
  }'
```

### Criar uma nova viagem
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

## Dashboard

O dashboard é atualizado automaticamente a cada 30 segundos e exibe:

1. **Cards de Resumo**: Total de linhas, ônibus, viagens ativas e paradas
2. **Gráfico de Lotação por Linha**: Compara média e máximo de pessoas
3. **Gráfico de Lotação Horária**: Mostra padrões ao longo do dia
4. **Top 10 Trechos**: Trechos mais lotados em ordem decrescente
5. **Registros Recentes**: Últimos 20 registros de lotação
6. **Mapa Visual**: Representação visual da lotação por linha e trecho

## Tecnologias Utilizadas

- **Backend**: Flask, PostgreSQL, psycopg2
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5, Chart.js
- **Visualização**: Chart.js para gráficos interativos

## Licença

MIT
