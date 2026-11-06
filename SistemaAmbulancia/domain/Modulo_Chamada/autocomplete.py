import requests
from .endereco import normalizar_coordenadas


def buscar_por_cep(cep):
    cep = ''.join(filter(str.isdigit, cep))
    if len(cep) != 8:
        return None

    url = f"https://brasilapi.com.br/api/cep/v2/{cep}"
    try:
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()
        data = resposta.json()
    except (requests.exceptions.RequestException, ValueError):
        return None

    if not isinstance(data, dict):
        return None

    localizacao = data.get("location")
    coordenadas = localizacao.get("coordinates") if isinstance(localizacao, dict) else None
    coordenadas = coordenadas if isinstance(coordenadas, dict) else {}

    return {
        "cep": data.get("cep", ""),
        "logradouro": data.get("street", ""),
        "bairro": data.get("neighborhood", ""),
        "cidade": data.get("city", ""),
        "estado": data.get("state", ""),
        "complemento": "",
        "latitude": coordenadas.get("latitude"),
        "longitude": coordenadas.get("longitude"),
    }


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

    try:
        for endereco in tentativas:
            latitude, longitude = _tentar_busca(endereco)
            if latitude is not None and longitude is not None:
                return latitude, longitude
    except (requests.exceptions.RequestException, ValueError):
        pass

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

    resposta = requests.get(url, params=params, headers=headers, timeout=10)
    resposta.raise_for_status()
    resultados = resposta.json()
    if not isinstance(resultados, list) or not resultados or not isinstance(resultados[0], dict):
        return None, None

    ponto = resultados[0]
    return normalizar_coordenadas(ponto.get("lat"), ponto.get("lon")) or (None, None)