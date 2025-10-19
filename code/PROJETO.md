# 🚌 Sistema Completo de Dashboard de Transporte Público

## 📋 Visão Geral

Sistema completo desenvolvido baseado no esquema de banco de dados fornecido, incluindo:
- ✅ API REST Flask com CRUD completo
- ✅ Schema SQL PostgreSQL
- ✅ Dashboard visual interativo
- ✅ Análises e estatísticas
- ✅ Documentação completa
- ✅ Scripts de automação

---

## 📁 Estrutura do Projeto

```
flask_transit_dashboard/
├── app.py                      # API Flask principal
├── schema.sql                  # Schema do banco de dados
├── populate_db.py              # Script para popular com dados
├── test_api.py                 # Testes automatizados
├── start.sh                    # Script de inicialização
├── requirements.txt            # Dependências Python
├── .env.example                # Exemplo de configuração
├── .gitignore                  # Arquivo de ignore do Git
├── README.md                   # Documentação principal
├── API_EXAMPLES.md             # Exemplos de uso da API
├── templates/
│   └── dashboard.html          # Interface do dashboard
└── static/
    ├── css/
    │   └── style.css           # Estilos personalizados
    └── js/
        └── dashboard.js        # Lógica do dashboard
```

---

## 🗄️ Esquema de Banco de Dados

Baseado no diagrama fornecido, foram criadas as seguintes tabelas:

### 📊 Modelo de Dados

```sql
onibus
├── id_onibus (PK)
├── placa
├── capacidade
└── data_ultima_manutencao

linha
├── id_linha (PK)
└── nome

parada
├── id_parada (PK)
├── nome
└── localizacao

rota
├── id_rota (PK)
├── id_linha (FK)
├── id_parada (FK)
├── ordem
└── esta_ativa

viagem
├── id_viagem (PK)
├── id_onibus (FK)
├── id_linha (FK)
├── data_hora_inicio
├── data_hora_fim
└── status

registro_lotacao
├── id_lotacao (PK)
├── id_viagem (FK)
├── id_parada_origem (FK)
├── id_parada_destino (FK)
├── data_hora
└── qtd_pessoas
```

---

## 🔌 API REST - Endpoints

### Recursos Principais

#### 🚌 Ônibus
- `GET /api/onibus` - Listar todos
- `GET /api/onibus/<id>` - Buscar por ID
- `POST /api/onibus` - Criar
- `PUT /api/onibus/<id>` - Atualizar
- `DELETE /api/onibus/<id>` - Deletar

#### 🚏 Linhas
- `GET /api/linhas` - Listar todas
- `GET /api/linhas/<id>` - Buscar por ID
- `POST /api/linhas` - Criar
- `PUT /api/linhas/<id>` - Atualizar
- `DELETE /api/linhas/<id>` - Deletar

#### 📍 Paradas
- `GET /api/paradas` - Listar todas
- `GET /api/paradas/<id>` - Buscar por ID
- `POST /api/paradas` - Criar
- `PUT /api/paradas/<id>` - Atualizar
- `DELETE /api/paradas/<id>` - Deletar

#### 🚍 Viagens
- `GET /api/viagens` - Listar todas (com JOIN)
- `GET /api/viagens/<id>` - Buscar por ID
- `POST /api/viagens` - Criar
- `PUT /api/viagens/<id>` - Atualizar
- `DELETE /api/viagens/<id>` - Deletar

#### 👥 Registros de Lotação
- `GET /api/lotacao` - Listar todos (com JOINs)
- `GET /api/lotacao/<id>` - Buscar por ID
- `POST /api/lotacao` - Criar
- `PUT /api/lotacao/<id>` - Atualizar
- `DELETE /api/lotacao/<id>` - Deletar

### Endpoints de Análise 📊

#### `/api/analytics/lotacao-por-linha`
Retorna estatísticas agregadas por linha:
- Média de pessoas
- Máximo de pessoas
- Mínimo de pessoas
- Total de registros

#### `/api/analytics/lotacao-por-trecho`
Top 20 trechos mais lotados (origem → destino):
- Nome da linha
- Parada origem e destino
- Média e máximo de pessoas
- Total de registros

#### `/api/analytics/lotacao-horaria`
Padrão de lotação ao longo do dia:
- Média de pessoas por hora
- Total de registros por hora

---

## 📊 Dashboard Visual

### Funcionalidades

1. **Cards de Resumo**
   - Total de Linhas
   - Total de Ônibus
   - Viagens Ativas
   - Total de Paradas

2. **Gráficos Interativos** (Chart.js)
   - 📊 **Lotação por Linha**: Gráfico de barras comparando média e máximo
   - 📈 **Lotação Horária**: Gráfico de linha mostrando padrão ao longo do dia
   - 📊 **Top 10 Trechos**: Gráfico horizontal dos trechos mais lotados

3. **Tabela de Registros Recentes**
   - Últimos 20 registros de lotação
   - Data/hora, linha, origem, destino
   - Quantidade de pessoas
   - Status visual (Normal/Moderado/Lotado)

4. **Mapa Visual de Lotação**
   - Visualização por linha
   - Barras de lotação por trecho
   - Código de cores:
     - 🟢 Verde: Normal (< 30 pessoas)
     - 🟡 Amarelo: Moderado (30-49 pessoas)
     - 🔴 Vermelho: Lotado (≥ 50 pessoas)

5. **Atualização Automática**
   - Dashboard atualiza a cada 30 segundos
   - Timestamp da última atualização

### Design

- Interface responsiva (Bootstrap 5)
- Tema profissional com cards
- Gráficos interativos com tooltips
- Cores semânticas para status
- Animações suaves

---

## 🚀 Guia de Instalação

### 1. Pré-requisitos

```bash
- PostgreSQL 12+
- Python 3.8+
- pip ou uv
```

### 2. Configurar Banco de Dados

```bash
# Criar banco
sudo -u postgres createdb transit_db

# Executar schema
sudo -u postgres psql -d transit_db -f schema.sql
```

### 3. Instalar Dependências

```bash
# Usando o script de inicialização (recomendado)
./start.sh

# Ou manualmente
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### 4. Configurar Variáveis

```bash
cp .env.example .env
# Editar .env com suas credenciais
```

### 5. Popular com Dados de Exemplo (Opcional)

```bash
python populate_db.py
```

### 6. Iniciar Aplicação

```bash
# Usando script
./start.sh

# Ou manualmente
python app.py
```

🌐 **Dashboard**: http://localhost:5000
🔌 **API**: http://localhost:5000/api

---

## 🧪 Testes

### Testar API Completa

```bash
python test_api.py
```

Este script testa:
- ✅ Health check
- ✅ CRUD de todos os recursos
- ✅ Endpoints de análise
- ✅ Validações de erro

### Testar com cURL

```bash
# Listar linhas
curl http://localhost:5000/api/linhas

# Criar ônibus
curl -X POST http://localhost:5000/api/onibus \
  -H "Content-Type: application/json" \
  -d '{"placa": "XYZ-9999", "capacidade": 50}'

# Ver análises
curl http://localhost:5000/api/analytics/lotacao-por-linha
```

Veja `API_EXAMPLES.md` para mais exemplos.

---

## 📈 Casos de Uso

### Cenário 1: Monitoramento em Tempo Real

1. Sistema registra lotação a cada parada
2. Dashboard atualiza automaticamente
3. Gestor visualiza trechos críticos
4. Decisão de adicionar veículos em horários de pico

### Cenário 2: Análise Histórica

1. Consultar `lotacao-por-horario`
2. Identificar padrões (picos às 7h e 18h)
3. Ajustar grade horária
4. Otimizar alocação de frota

### Cenário 3: Planejamento de Rotas

1. Analisar `lotacao-por-trecho`
2. Identificar trechos subutilizados
3. Redesenhar rotas
4. Melhorar eficiência operacional

---

## 🎨 Capturas de Tela (Conceito)

### Dashboard Principal
```
┌─────────────────────────────────────────────────────────┐
│  🚌 Dashboard de Transporte Público     16:30:45        │
├─────────────────────────────────────────────────────────┤
│  [Total Linhas] [Total Ônibus] [Viagens] [Paradas]     │
│       3              3            5          6          │
├──────────────────┬──────────────────────────────────────┤
│  📊 Lotação/Linha│  📈 Lotação Horária                  │
│  [Gráfico Barras]│  [Gráfico Linha]                     │
├──────────────────┴──────────────────────────────────────┤
│  📊 Top 10 Trechos Mais Lotados                         │
│  [Gráfico Horizontal]                                   │
├─────────────────────────────────────────────────────────┤
│  📋 Registros Recentes                                  │
│  [Tabela com últimos registros]                         │
├─────────────────────────────────────────────────────────┤
│  🗺️ Mapa de Lotação por Linha                          │
│  Linha 100: [======45%====    ] 28 pessoas             │
│  Linha 200: [===========80%===] 48 pessoas             │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 Tecnologias Utilizadas

### Backend
- **Flask 3.0.0**: Framework web minimalista
- **psycopg2**: Driver PostgreSQL
- **Flask-CORS**: Suporte CORS
- **python-dotenv**: Gerenciamento de variáveis

### Frontend
- **Bootstrap 5**: Framework CSS responsivo
- **Chart.js 4.4**: Biblioteca de gráficos
- **JavaScript Vanilla**: Lógica do dashboard

### Banco de Dados
- **PostgreSQL**: Sistema de banco relacional

---

## 📝 Próximos Passos

### Melhorias Sugeridas

1. **Autenticação e Autorização**
   - JWT tokens
   - Níveis de acesso (admin, operador, visualizador)

2. **WebSocket para Tempo Real**
   - Atualização instantânea do dashboard
   - Notificações de lotação crítica

3. **Aplicativo Mobile**
   - App para motoristas registrarem lotação
   - API já está pronta!

4. **Relatórios Avançados**
   - Exportação PDF/Excel
   - Relatórios agendados por email

5. **Integração GPS**
   - Rastreamento de veículos
   - Localização em tempo real

6. **Machine Learning**
   - Predição de lotação
   - Otimização de rotas

---

## 📄 Licença

MIT

---

## 👨‍💻 Suporte

Para dúvidas ou problemas:
1. Consulte `README.md`
2. Veja exemplos em `API_EXAMPLES.md`
3. Execute `python test_api.py` para diagnóstico

---

## ✅ Checklist de Implementação

- [x] Schema SQL completo
- [x] API REST com CRUD para todas as entidades
- [x] Endpoints de análise
- [x] Dashboard HTML/CSS/JS
- [x] Gráficos interativos
- [x] Visualização de lotação por trecho
- [x] Documentação completa
- [x] Scripts de automação
- [x] Testes automatizados
- [x] Dados de exemplo
- [x] README detalhado
- [x] Guia de API

**🎉 Projeto 100% Completo!**
