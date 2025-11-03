from API.models import onibus_model

def listar():
    return onibus_model.list_all(), 200

def obter(id_):
    row = onibus_model.get_by_id(id_); return (row, 200) if row else ({"error": "Ônibus não encontrado"}, 404)

def criar(payload):
    try:
        row = onibus_model.create(payload); return row, 201
    except Exception as e:
        return {"error": str(e)}, 400

def atualizar(id_, payload):
    try:
        row = onibus_model.update(id_, payload)
        return (row, 200) if row else ({"error": "Ônibus não encontrado"}, 404)
    except Exception as e:
        return {"error": str(e)}, 400

def deletar(id_):
    ok = onibus_model.delete(id_); return ({"message": "Ônibus deletado com sucesso"}, 200) if ok else ({"error": "Ônibus não encontrado"}, 404)
