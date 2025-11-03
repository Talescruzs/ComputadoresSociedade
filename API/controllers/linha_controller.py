from API.models import linha_model

def listar():
    return linha_model.list_all(), 200

def obter(id_):
    row = linha_model.get_by_id(id_); return (row, 200) if row else ({"error": "Linha não encontrada"}, 404)

def criar(payload):
    try:
        row = linha_model.create(payload); return row, 201
    except Exception as e:
        return {"error": str(e)}, 400

def atualizar(id_, payload):
    try:
        row = linha_model.update(id_, payload)
        return (row, 200) if row else ({"error": "Linha não encontrada"}, 404)
    except Exception as e:
        return {"error": str(e)}, 400

def deletar(id_):
    ok = linha_model.delete(id_); return ({"message": "Linha deletada com sucesso"}, 200) if ok else ({"error": "Linha não encontrada"}, 404)
