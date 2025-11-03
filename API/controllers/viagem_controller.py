from API.models import viagem_model

def listar():
    return viagem_model.list_all(), 200

def obter(id_):
    row = viagem_model.get_by_id(id_); return (row, 200) if row else ({"error": "Viagem não encontrada"}, 404)

def criar(payload):
    try:
        row = viagem_model.create(payload); return row, 201
    except Exception as e:
        return {"error": str(e)}, 400

def atualizar(id_, payload):
    try:
        row = viagem_model.update(id_, payload)
        return (row, 200) if row else ({"error": "Viagem não encontrada"}, 404)
    except Exception as e:
        return {"error": str(e)}, 400

def deletar(id_):
    ok = viagem_model.delete(id_); return ({"message": "Viagem deletada com sucesso"}, 200) if ok else ({"error": "Viagem não encontrada"}, 404)
