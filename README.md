# ComputadoresSociedade
Repositorio destinado a armazenar os codigos do aplicativo da cadeira de computadores e sociedade.

# Para rodar

## Instalar dependências (requirements.txt)
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

(Ative sempre o venv antes de executar scripts.)

## Banco de dados
```bash
python3 DB/init_db.py
python3 DB/populate_db.py
```

## API
```bash
source .venv/bin/activate
python3 API/app.py
```

## FRONT
```bash
source .venv/bin/activate
python3 FRONT/app.py
```