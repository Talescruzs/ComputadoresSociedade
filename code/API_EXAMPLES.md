# Exemplos de Uso da API

Este documento contém exemplos práticos de como usar cada endpoint da API.

## Índice

1. [Ônibus](#ônibus)
2. [Linhas](#linhas)
3. [Paradas](#paradas)
4. [Viagens](#viagens)
5. [Registros de Lotação](#registros-de-lotação)
6. [Análises](#análises)

---

## Ônibus

### Listar todos os ônibus

```bash
curl -X GET http://localhost:5000/api/onibus
```

**Resposta:**
```json
[
  {
    "id_onibus": 1,
    "placa": "ABC-1234",
    "capacidade": 50,
    "data_ultima_manutencao": "2024-09-15T10:00:00"
  }
]
```

### Buscar ônibus por ID

```bash
curl -X GET http://localhost:5000/api/onibus/1
```

### Criar novo ônibus

```bash
curl -X POST http://localhost:5000/api/onibus \
  -H "Content-Type: application/json" \
  -d '{
    "placa": "XYZ-9999",
    "capacidade": 50,
    "data_ultima_manutencao": "2024-10-01 10:00:00"
  }'
```

### Atualizar ônibus

```bash
curl -X PUT http://localhost:5000/api/onibus/1 \
  -H "Content-Type: application/json" \
  -d '{
    "placa": "ABC-1234",
    "capacidade": 55,
    "data_ultima_manutencao": "2024-10-15 14:00:00"
  }'
```

### Deletar ônibus

```bash
curl -X DELETE http://localhost:5000/api/onibus/1
```

---

## Linhas

### Listar todas as linhas

```bash
curl -X GET http://localhost:5000/api/linhas
```

**Resposta:**
```json
[
  {
    "id_linha": 1,
    "nome": "Linha 100 - Centro/Terminal"
  }
]
```

### Buscar linha por ID

```bash
curl -X GET http://localhost:5000/api/linhas/1
```

### Criar nova linha

```bash
curl -X POST http://localhost:5000/api/linhas \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Linha 400 - Bairro Norte/Sul"
  }'
```

### Atualizar linha

```bash
curl -X PUT http://localhost:5000/api/linhas/1 \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Linha 100 - Centro/Terminal (Expressa)"
  }'
```

### Deletar linha

```bash
curl -X DELETE http://localhost:5000/api/linhas/1
```

---

## Paradas

### Listar todas as paradas

```bash
curl -X GET http://localhost:5000/api/paradas
```

**Resposta:**
```json
[
  {
    "id_parada": 1,
    "nome": "Terminal Central",
    "localizacao": "Av. Principal, 100"
  }
]
```

### Buscar parada por ID

```bash
curl -X GET http://localhost:5000/api/paradas/1
```

### Criar nova parada

```bash
curl -X POST http://localhost:5000/api/paradas \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Estação Universitária",
    "localizacao": "Campus Universitário, s/n"
  }'
```

### Atualizar parada

```bash
curl -X PUT http://localhost:5000/api/paradas/1 \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Terminal Central - Reformado",
    "localizacao": "Av. Principal, 100"
  }'
```

### Deletar parada

```bash
curl -X DELETE http://localhost:5000/api/paradas/1
```

---

## Viagens

### Listar todas as viagens

```bash
curl -X GET http://localhost:5000/api/viagens
```

**Resposta:**
```json
[
  {
    "id_viagem": 1,
    "id_onibus": 1,
    "id_linha": 1,
    "data_hora_inicio": "2024-10-19T08:00:00",
    "data_hora_fim": null,
    "status": "em_andamento",
    "placa": "ABC-1234",
    "linha_nome": "Linha 100 - Centro/Terminal"
  }
]
```

### Buscar viagem por ID

```bash
curl -X GET http://localhost:5000/api/viagens/1
```

### Criar nova viagem

```bash
curl -X POST http://localhost:5000/api/viagens \
  -H "Content-Type: application/json" \
  -d '{
    "id_onibus": 1,
    "id_linha": 1,
    "data_hora_inicio": "2024-10-19 08:00:00",
    "status": "em_andamento"
  }'
```

**Nota:** Se `data_hora_inicio` não for fornecido, será usado o timestamp atual.

### Atualizar viagem (finalizar)

```bash
curl -X PUT http://localhost:5000/api/viagens/1 \
  -H "Content-Type: application/json" \
  -d '{
    "id_onibus": 1,
    "id_linha": 1,
    "data_hora_inicio": "2024-10-19 08:00:00",
    "data_hora_fim": "2024-10-19 10:30:00",
    "status": "finalizada"
  }'
```

### Deletar viagem

```bash
curl -X DELETE http://localhost:5000/api/viagens/1
```

---

## Registros de Lotação

### Listar todos os registros

```bash
curl -X GET http://localhost:5000/api/lotacao
```

**Resposta:**
```json
[
  {
    "id_lotacao": 1,
    "id_viagem": 1,
    "id_parada_origem": 1,
    "id_parada_destino": 2,
    "data_hora": "2024-10-19T08:15:00",
    "qtd_pessoas": 35,
    "parada_origem_nome": "Terminal Central",
    "parada_destino_nome": "Praça da Matriz",
    "id_linha": 1,
    "linha_nome": "Linha 100 - Centro/Terminal"
  }
]
```

### Buscar registro por ID

```bash
curl -X GET http://localhost:5000/api/lotacao/1
```

### Criar novo registro de lotação

```bash
curl -X POST http://localhost:5000/api/lotacao \
  -H "Content-Type: application/json" \
  -d '{
    "id_viagem": 1,
    "id_parada_origem": 1,
    "id_parada_destino": 2,
    "qtd_pessoas": 42
  }'
```

**Nota:** 
- `data_hora` é opcional (padrão: timestamp atual)
- `id_parada_destino` é opcional (para registros em uma única parada)

### Atualizar registro

```bash
curl -X PUT http://localhost:5000/api/lotacao/1 \
  -H "Content-Type: application/json" \
  -d '{
    "id_viagem": 1,
    "id_parada_origem": 1,
    "id_parada_destino": 2,
    "data_hora": "2024-10-19 08:15:00",
    "qtd_pessoas": 45
  }'
```

### Deletar registro

```bash
curl -X DELETE http://localhost:5000/api/lotacao/1
```

---

## Análises

### Lotação por Linha

Retorna estatísticas agregadas por linha.

```bash
curl -X GET http://localhost:5000/api/analytics/lotacao-por-linha
```

**Resposta:**
```json
[
  {
    "id_linha": 1,
    "linha_nome": "Linha 100 - Centro/Terminal",
    "media_pessoas": 38.5,
    "max_pessoas": 58,
    "min_pessoas": 12,
    "total_registros": 45
  }
]
```

### Lotação por Trecho

Retorna os 20 trechos mais lotados (origem → destino).

```bash
curl -X GET http://localhost:5000/api/analytics/lotacao-por-trecho
```

**Resposta:**
```json
[
  {
    "linha_nome": "Linha 100 - Centro/Terminal",
    "parada_origem": "Terminal Central",
    "parada_destino": "Praça da Matriz",
    "media_pessoas": 42.3,
    "max_pessoas": 58,
    "total_registros": 15
  }
]
```

### Lotação por Horário

Retorna a média de pessoas por hora do dia.

```bash
curl -X GET http://localhost:5000/api/analytics/lotacao-horaria
```

**Resposta:**
```json
[
  {
    "hora": 7,
    "media_pessoas": 45.2,
    "total_registros": 12
  },
  {
    "hora": 8,
    "media_pessoas": 52.8,
    "total_registros": 18
  }
]
```

---

## Fluxo de Trabalho Típico

### 1. Configurar Infraestrutura

```bash
# Criar linha
curl -X POST http://localhost:5000/api/linhas \
  -H "Content-Type: application/json" \
  -d '{"nome": "Linha 500 - Teste"}'

# Criar paradas
curl -X POST http://localhost:5000/api/paradas \
  -H "Content-Type: application/json" \
  -d '{"nome": "Parada A", "localizacao": "Rua A, 123"}'

curl -X POST http://localhost:5000/api/paradas \
  -H "Content-Type: application/json" \
  -d '{"nome": "Parada B", "localizacao": "Rua B, 456"}'

# Criar ônibus
curl -X POST http://localhost:5000/api/onibus \
  -H "Content-Type: application/json" \
  -d '{"placa": "TEST-001", "capacidade": 50}'
```

### 2. Iniciar Viagem

```bash
curl -X POST http://localhost:5000/api/viagens \
  -H "Content-Type: application/json" \
  -d '{
    "id_onibus": 1,
    "id_linha": 1,
    "status": "em_andamento"
  }'
```

### 3. Registrar Lotação

```bash
# Registrar lotação no primeiro trecho
curl -X POST http://localhost:5000/api/lotacao \
  -H "Content-Type: application/json" \
  -d '{
    "id_viagem": 1,
    "id_parada_origem": 1,
    "id_parada_destino": 2,
    "qtd_pessoas": 35
  }'

# Registrar lotação no segundo trecho
curl -X POST http://localhost:5000/api/lotacao \
  -H "Content-Type: application/json" \
  -d '{
    "id_viagem": 1,
    "id_parada_origem": 2,
    "id_parada_destino": 3,
    "qtd_pessoas": 42
  }'
```

### 4. Visualizar Análises

```bash
# Ver estatísticas por linha
curl -X GET http://localhost:5000/api/analytics/lotacao-por-linha

# Ver trechos mais lotados
curl -X GET http://localhost:5000/api/analytics/lotacao-por-trecho
```

---

## Testando a API com Python

```python
import requests
import json

BASE_URL = "http://localhost:5000/api"

# Listar todas as linhas
response = requests.get(f"{BASE_URL}/linhas")
print(json.dumps(response.json(), indent=2))

# Criar nova parada
nova_parada = {
    "nome": "Nova Parada",
    "localizacao": "Teste, 999"
}
response = requests.post(f"{BASE_URL}/paradas", json=nova_parada)
print(response.json())

# Buscar análises
response = requests.get(f"{BASE_URL}/analytics/lotacao-por-linha")
for linha in response.json():
    print(f"{linha['linha_nome']}: média {linha['media_pessoas']} pessoas")
```

---

## Notas Importantes

1. **Formato de Data/Hora**: Use o formato ISO 8601 ou `YYYY-MM-DD HH:MM:SS`
2. **IDs**: Todos os IDs são inteiros gerados automaticamente
3. **Validação**: A API retorna erro 400 para dados inválidos
4. **Cascade**: Deletar uma linha/ônibus/parada deleta registros relacionados
5. **CORS**: A API aceita requisições de qualquer origem
