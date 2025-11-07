from API.models import parada_model

def listar():
    return parada_model.list_all(), 200

def obter(id_):
    row = parada_model.get_by_id(id_); return (row, 200) if row else ({"error": "Parada não encontrada"}, 404)

def criar(payload):
    try:
        row = parada_model.create(payload); return row, 201
    except Exception as e:
        return {"error": str(e)}, 400

def atualizar(id_, payload):
    try:
        row = parada_model.update(id_, payload)
        return (row, 200) if row else ({"error": "Parada não encontrada"}, 404)
    except Exception as e:
        return {"error": str(e)}, 400

def deletar(id_):
    ok = parada_model.delete(id_); return ({"message": "Parada deletada com sucesso"}, 200) if ok else ({"error": "Parada não encontrada"}, 404)

def listar_pessoas_total():
    data = parada_model.pessoas_total_por_parada()
    return data, 200

def listar_pessoas_por_hora(id_parada: int):
    data = parada_model.pessoas_por_hora_parada(id_parada)
    return data, 200