import re

from domain.Modulo_Ambulancia.ambulancia import Ambulancia
from domain.Modulo_Chamada.prioridade import Prioridade
from domain.Modulo_Chamada.status import Status
from .triagem import ErroConfirmacaoTriagem


def ler_campos_confirmacao(
    prioridade: str, quantidade_digitada: str, placas_digitadas: str,
) -> tuple[int, list[str]]:
    try:
        quantidade = int(quantidade_digitada)
    except ValueError:
        quantidade = 0

    if quantidade <= 0:
        raise ErroConfirmacaoTriagem("Digite uma quantidade inteira maior que zero.")

    placas = [placa for placa in re.split(r"[\s,;|]+", placas_digitadas) if placa]
    if not prioridade.strip() or not placas:
        raise ErroConfirmacaoTriagem("Preencha a prioridade e as placas das ambulâncias.")
    return quantidade, placas


def resolver_ambulancias_por_placa(
    placas_ambulancias: list[str], quantidade: int, frota: list[Ambulancia],
) -> list[Ambulancia]:
    placas = [placa.strip().upper() for placa in placas_ambulancias]
    if len(set(placas)) != len(placas):
        raise ErroConfirmacaoTriagem("Digite cada placa uma única vez.")

    por_placa = {ambulancia.placa.strip().upper(): ambulancia for ambulancia in frota}
    if quantidade > len(_ambulancias_disponiveis(por_placa.values())):
        raise ErroConfirmacaoTriagem("A frota disponível é insuficiente para essa quantidade.")
    if len(placas) != quantidade:
        raise ErroConfirmacaoTriagem("A quantidade deve corresponder ao número de placas.")

    selecionadas = []
    for placa in placas:
        ambulancia = por_placa.get(placa)
        if ambulancia is None:
            raise ErroConfirmacaoTriagem(f"Placa inexistente ({placa}).")
        if ambulancia.status != "Disponivel":
            raise ErroConfirmacaoTriagem(f"A ambulância de placa {placa} está indisponível.")
        selecionadas.append(ambulancia)
    return selecionadas


def validar_confirmacao(dados_triagem, triagens_pendentes, chamadas, frota):
    chamada = _localizar_chamada_pendente(dados_triagem.get("id"), triagens_pendentes, chamadas)
    prioridade = dados_triagem.get("prioridade")
    if prioridade not in (opcao.value for opcao in Prioridade):
        raise ErroConfirmacaoTriagem("Selecione uma prioridade válida.")

    ambulancias = _validar_ambulancias_para_alocacao(
        dados_triagem.get("qtd_ambulancias"), dados_triagem.get("ambulancias"), frota,
    )
    return chamada, prioridade, ambulancias


def _localizar_chamada_pendente(triagem_id, triagens_pendentes, chamadas):
    chamada = next(
        (chamada for triagem, chamada in triagens_pendentes
         if triagem.id == triagem_id and triagem.qtd_ambulancias is not None),
        None,
    )
    if chamada is None or chamada not in chamadas or chamada.status != Status.PENDENTE.value:
        raise ErroConfirmacaoTriagem("A chamada precisa estar pendente para ser alocada.")
    return chamada


def _validar_ambulancias_para_alocacao(quantidade, ambulancias, frota):
    if (
        type(quantidade) is not int or quantidade <= 0
        or not isinstance(ambulancias, list) or len(ambulancias) != quantidade
    ):
        raise ErroConfirmacaoTriagem("A quantidade deve corresponder às ambulâncias selecionadas.")
    if not all(isinstance(ambulancia, Ambulancia) for ambulancia in ambulancias):
        raise ErroConfirmacaoTriagem("Selecione ambulâncias válidas.")

    ids_selecionados = {ambulancia.id for ambulancia in ambulancias}
    if len(ids_selecionados) != quantidade:
        raise ErroConfirmacaoTriagem("Selecione cada ambulância uma única vez.")

    disponiveis = _ambulancias_disponiveis(frota)
    if quantidade > len(disponiveis):
        raise ErroConfirmacaoTriagem("A frota disponível é insuficiente para essa quantidade.")
    if not ids_selecionados.issubset(disponiveis):
        raise ErroConfirmacaoTriagem("Uma ou mais ambulâncias selecionadas estão indisponíveis.")

    return [disponiveis[ambulancia.id] for ambulancia in ambulancias]


def _ambulancias_disponiveis(frota):
    return {
        ambulancia.id: ambulancia for ambulancia in frota
        if ambulancia.status == "Disponivel"
    }
