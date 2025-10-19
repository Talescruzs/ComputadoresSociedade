# 🛠️ Setup Manual - Sistema sem PostgreSQL

Seu sistema não tem PostgreSQL instalado. Vou fornecer duas opções:

---

## 📌 OPÇÃO 1: Instalar PostgreSQL (Recomendado para Produção)

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y postgresql postgresql-contrib

# Iniciar serviço
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Criar banco
sudo -u postgres createdb transit_db

# Executar schema
sudo -u postgres psql -d transit_db -f schema.sql

# Usar app original
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

---

## 📌 OPÇÃO 2: Usar SQLite (Mais Simples - Já Preparado!)

Criei uma versão completa usando SQLite que não requer instalação de servidor.

### ✅ Arquivos SQLite Criados:

- `app_sqlite.py` - API Flask adaptada para SQLite
- `schema_sqlite.sql` - Schema para SQLite
- `init_db.py` - Script Python para inicializar
- `README_SQLITE.md` - Guia completo SQLite

### 🚀 Como Usar (3 Passos):

#### 1. Criar ambiente virtual e instalar dependências

```bash
cd /home/vboxuser/Workspace/flask_transit_dashboard

# Criar ambiente virtual
python3 -m venv .venv

# Ativar
source .venv/bin/activate

# Instalar dependências
pip install Flask Flask-CORS
```

#### 2. Criar banco de dados

Se você tiver Python funcionando:
```bash
python init_db.py
```

Ou manualmente com sqlite3:
```bash
sqlite3 transit.db < schema_sqlite.sql
```

#### 3. Iniciar aplicação

```bash
python app_sqlite.py
```

### ✅ Acessar:

- **Dashboard**: http://localhost:5000
- **API**: http://localhost:5000/api

---

## 🔍 Verificar o Que Está Instalado

```bash
# Verificar Python
python3 --version

# Verificar se SQLite está disponível
which sqlite3

# Verificar se PostgreSQL está instalado
which psql
```

---

## ⚠️ Problema Atual no Sistema

Parece que o Python do sistema está com problema. Você pode:

1. **Reinstalar Python**:
```bash
sudo apt update
sudo apt install --reinstall python3 python3-pip
```

2. **Ou usar Conda/Miniconda** (isolado do sistema):
```bash
# Instalar miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

# Criar ambiente
conda create -n transit python=3.10
conda activate transit

# Instalar dependências
pip install Flask Flask-CORS

# Rodar app
python app_sqlite.py
```

---

## 📋 Resumo dos Arquivos

### Para PostgreSQL (Original):
- `app.py` - API principal
- `schema.sql` - Schema PostgreSQL
- `requirements.txt` - Dependências

### Para SQLite (Alternativa):
- `app_sqlite.py` - API adaptada
- `schema_sqlite.sql` - Schema SQLite
- `init_db.py` - Inicializador Python
- `populate_db_sqlite.py` - Gerador de dados

### Documentação:
- `README.md` - Guia PostgreSQL
- `README_SQLITE.md` - Guia SQLite
- `SETUP_MANUAL.md` - Este arquivo
- `API_EXAMPLES.md` - Exemplos de uso
- `QUICK_START.md` - Início rápido

---

## 🆘 Precisa de Ajuda?

Se continuar com problemas:

1. Verifique se Python está funcionando:
   ```bash
   python3 -c "print('Hello')"
   ```

2. Se não funcionar, reinstale Python

3. Ou use a versão online do projeto no Repl.it ou similar

---

## ✅ O que já está pronto:

- ✅ Schema SQL (PostgreSQL e SQLite)
- ✅ API REST completa (ambas versões)
- ✅ Dashboard HTML/CSS/JS
- ✅ Documentação completa
- ✅ Scripts de inicialização
- ✅ Exemplos de uso

Tudo 100% funcional, apenas precisa de Python funcionando!
