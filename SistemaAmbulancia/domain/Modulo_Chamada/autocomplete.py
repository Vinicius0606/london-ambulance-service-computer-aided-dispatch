import requests


def buscar_por_cep(cep):
    cep = ''.join(filter(str.isdigit, cep))

    if len(cep) != 8:
        print("CEP inválido!")
        return None

    url = f"https://brasilapi.com.br/api/cep/v2/{cep}"
    resposta = requests.get(url, timeout=10)

    if resposta.status_code != 200:
        raise ValueError("Erro ao consultar o CEP")

    data = resposta.json()

    valores = {
        "cep": data.get("cep", ""),
        "logradouro": data.get("street", ""),
        "bairro": data.get("neighborhood", ""),
        "cidade": data.get("city", ""),
        "estado": data.get("state", ""),
        "complemento": "",
        "latitude": (
            data.get("location", {})
            .get("coordinates", {})
            .get("latitude")
        ),
        "longitude": (
            data.get("location", {})
            .get("coordinates", {})
            .get("longitude")
        )
    }

    return valores

def buscar_por_endereco(logradouro, bairro, cidade, estado, cep=""):
    tentativas = []

    if logradouro and bairro and cidade and cep:
        tentativas.append(f"{logradouro}, {bairro}, {cidade}, {estado}, Brasil, {cep}")

    if logradouro and bairro and cidade:
        tentativas.append(f"{logradouro}, {bairro}, {cidade}, {estado}, Brasil")

    if logradouro and cidade:
        tentativas.append(f"{logradouro}, {cidade}, {estado}, Brasil")

    if bairro and cidade and cep:
        tentativas.append(f"{bairro}, {cidade}, {estado}, Brasil, {cep}")

    if bairro and cidade:
        tentativas.append(f"{bairro}, {cidade}, {estado}, Brasil")

    if cidade and estado:
        tentativas.append(f"{cidade}, {estado}, Brasil")

    for endereco in tentativas:
        lat, lon = _tentar_busca(endereco)
        if lat is not None and lon is not None:
            return lat, lon

    return None, None

def _tentar_busca(endereco):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": endereco,
        "format": "json",
        "limit": 1,
        "countrycodes": "br"
    }
    headers = {
        "User-Agent": "SistemaAmbulancia/1.0"
    }

    response = requests.get(url, params=params, headers=headers, timeout=10)

    if response.status_code != 200:
        return None, None

    resultados = response.json()

    if not resultados:
        return None, None

    return float(resultados[0]["lat"]), float(resultados[0]["lon"])