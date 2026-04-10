import requests

def validacao(cep):

    if len(cep) == 8:
        return buscar_endereco(cep)

def buscar_endereco(cep):
    cep = ''.join(filter(str.isdigit, cep))

    if len(cep) != 8:
        raise ValueError("CEP inválido")

    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        raise ValueError("Erro ao consultar o CEP")

    data = response.json()

    if data.get("erro"):
        raise ValueError("CEP não encontrado")

    values = {
        "cep": data.get("cep", ""),
        "logradouro": data.get("logradouro", ""),
        "bairro": data.get("bairro", ""),
        "cidade": data.get("localidade", ""),
        "estado": data.get("uf", ""),
        "complemento": data.get("complemento", "")
    }

    print(values)

    return values