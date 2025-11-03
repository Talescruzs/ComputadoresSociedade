from API.models import lotacao_model

def lotacao_por_linha():
    return lotacao_model.analytics_lotacao_por_linha(), 200

def lotacao_por_trecho():
    return lotacao_model.analytics_lotacao_por_trecho(), 200

def lotacao_horaria():
    return lotacao_model.analytics_lotacao_horaria(), 200
