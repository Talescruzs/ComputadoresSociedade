from FRONT.services.api_client import api_get, api_post

def dashboard():
    onibus = api_get("/onibus") or []
    linhas = api_get("/linhas") or []
    paradas = api_get("/paradas") or []
    metrics = {
        "por_linha": api_get("/analytics/lotacao-por-linha") or [],
        "horaria": api_get("/analytics/lotacao-horaria") or [],
    }
    return {"onibus": onibus, "linhas": linhas, "paradas": paradas, "metrics": metrics}

def criar_onibus(data):
    payload = {
        "placa": data.get("placa", "").strip(),
        "capacidade": int(data.get("capacidade", "0") or 0),
        "data_ultima_manutencao": data.get("data_ultima_manutencao") or None,
    }
    api_post("/onibus", payload)
