from API.models import lotacao_model

def listar():
    return lotacao_model.list_all(), 200

def obter(id_):
    row = lotacao_model.get_by_id(id_); return (row, 200) if row else ({"error": "Registro não encontrado"}, 404)

def criar(payload):
    try:
        row = lotacao_model.create(payload); return row, 201
    except Exception as e:
        return {"error": str(e)}, 400

def atualizar(id_, payload):
    try:
        row = lotacao_model.update(id_, payload)
        return (row, 200) if row else ({"error": "Registro não encontrado"}, 404)
    except Exception as e:
        return {"error": str(e)}, 400

def deletar(id_):
    ok = lotacao_model.delete(id_); return ({"message": "Registro deletado com sucesso"}, 200) if ok else ({"error": "Registro não encontrado"}, 404)

def analytics_linha():
    return lotacao_model.analytics_lotacao_por_linha(), 200

def analytics_trecho():
    return lotacao_model.analytics_lotacao_por_trecho(), 200

def analytics_horaria():
    return lotacao_model.analytics_lotacao_horaria(), 200
