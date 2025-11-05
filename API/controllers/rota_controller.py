from API.models import rota_model as model

def get_rota_por_linha(id_linha: int):
    data = model.rota_por_linha(id_linha)
    return data, 200

def get_linhas_por_parada(id_parada: int):
    data = model.linhas_por_parada(id_parada)
    return data, 200
