import pytest

from domain.Modulo_Ambulancia.ambulancia import Ambulancia
from domain.Modulo_Ambulancia.atendimento import Atendimento
from domain.Modulo_Ambulancia.status import Status as StatusDespacho
from domain.Modulo_Chamada.chamada import Chamada
from domain.Modulo_Chamada.endereco import Endereco
from domain.Modulo_Chamada.prioridade import Prioridade
from domain.Modulo_Chamada.status import Status as StatusChamada
from domain.Modulo_Triagem.tipos_definir_prioridade.definir_prioridade_pontuacao import (
    Definir_prioridade_pontuacao,
)
from domain.Modulo_Triagem.tipos_escolher_ambulancia.escolher_ambulancia_hipotenusa import (
    Escolher_ambulancia_hipotenusa,
)
from domain.Modulo_Triagem.triagem import ErroConfirmacaoTriagem, Triagem
from domain.Modulo_Triagem.validacao_confirmacao import validar_confirmacao
from events.gerenciador_eventos import Gerenciador_eventos


@pytest.fixture
def eventos():
    return Gerenciador_eventos()


@pytest.fixture
def frota(eventos):
    return [
        Ambulancia(1, "AAA1001", 3, 4, eventos),
        Ambulancia(2, "AAA1002", 1, 0, eventos),
        Ambulancia(3, "AAA1003", 0, 0, eventos, status="Atendendo"),
    ]


@pytest.fixture
def chamada(eventos):
    endereco = Endereco("70000000", "Rua de teste", "Centro", "Brasília", "DF", 0, 0)
    return Chamada(endereco, "Ocorrência de teste", eventos, id=10, veio_do_banco_de_dados=True)


@pytest.fixture
def triagem_pendente(chamada, eventos):
    triagem = Triagem(21, chamada.descricao, eventos, 0, 0)
    triagem.qtd_ambulancias = 2
    return triagem, chamada


@pytest.mark.parametrize(
    ("dados", "prioridade"),
    [
        pytest.param({"quantidade_vitimas": 0}, 1, id="transporte"),
        pytest.param({}, 2, id="moderada"),
        pytest.param({"suspeita_trauma": True}, 3, id="trauma"),
        pytest.param({"respira": False}, 4, id="extrema"),
    ],
)
def test_definir_prioridade(dados, prioridade):
    ocorrencia = {
        "respira": True,
        "sangramento_intenso": False,
        "suspeita_trauma": False,
        "inconsciente": False,
        "dificuldade_respiratoria": False,
        "quantidade_vitimas": 1,
    }
    ocorrencia.update(dados)

    assert Definir_prioridade_pontuacao().definir_prioridade(ocorrencia) == prioridade


@pytest.mark.parametrize(
    ("indices", "quantidade", "ids_esperados"),
    [
        pytest.param((0, 1), 2, [2, 1], id="ordem-por-proximidade"),
        pytest.param((2, 1), 1, [2], id="ignora-indisponivel"),
        pytest.param((0, 1), 3, [2, 1], id="frota-insuficiente"),
        pytest.param((2,), 1, [], id="nenhuma-disponivel"),
    ],
)
def test_selecionar_ambulancias(frota, indices, quantidade, ids_esperados):
    candidatas = [frota[indice] for indice in indices]

    resultado = Escolher_ambulancia_hipotenusa().escolher_ambulancias(
        candidatas, quantidade, 0, 0,
    )

    assert [ambulancia.id for ambulancia in resultado["ambulancias"]] == ids_esperados
    assert resultado["qtd_ambulancias"] == len(ids_esperados)


def test_confirmar_triagem_pendente(triagem_pendente, chamada, frota):
    dados = {
        "id": 21,
        "prioridade": Prioridade.ALTA.value,
        "qtd_ambulancias": 2,
        "ambulancias": frota[:2],
    }

    resultado = validar_confirmacao(dados, [triagem_pendente], [chamada], frota)

    assert resultado == (chamada, Prioridade.ALTA.value, frota[:2])


def test_rejeitar_triagem_inexistente(triagem_pendente, chamada, frota):
    dados = {
        "id": 99,
        "prioridade": Prioridade.ALTA.value,
        "qtd_ambulancias": 2,
        "ambulancias": frota[:2],
    }

    with pytest.raises(ErroConfirmacaoTriagem, match="chamada precisa estar pendente"):
        validar_confirmacao(dados, [triagem_pendente], [chamada], frota)


def test_rejeitar_ambulancia_repetida(triagem_pendente, chamada, frota):
    dados = {
        "id": 21,
        "prioridade": Prioridade.ALTA.value,
        "qtd_ambulancias": 2,
        "ambulancias": [frota[0], frota[0]],
    }

    with pytest.raises(ErroConfirmacaoTriagem, match="cada ambulância uma única vez"):
        validar_confirmacao(dados, [triagem_pendente], [chamada], frota)


def test_encerrar_atendimento_apos_ultimo_despacho(chamada, frota, eventos):
    atualizacoes = []
    finalizados = []
    eventos.adicionar_ouvinte_para_evento("Atualizar_despacho_Banco_dados", atualizacoes.append)
    eventos.adicionar_ouvinte_para_evento("Atendimento_finalizado", finalizados.append)

    chamada.atualizar_dados(prioridade=None, status=StatusChamada.ALOCADO.value)
    atendimento = Atendimento(31, chamada, 2, frota[:2], eventos)
    atendimento.criar_despachos()
    primeiro, segundo = atendimento.despachos
    primeiro.atualizar_ID(41)
    segundo.atualizar_ID(42)
    assert [ambulancia.status for ambulancia in frota[:2]] == ["Atendendo", "Atendendo"]

    eventos.emitir_evento("Ambulancia_chegou_no_hospital", primeiro)

    assert primeiro.status == StatusDespacho.FINALIZADO.value
    assert frota[0].status == "Disponivel"
    assert frota[1].status == "Atendendo"
    assert atendimento.hora_finalizacao is None
    assert chamada.status == StatusChamada.ALOCADO.value
    assert finalizados == []

    eventos.emitir_evento("Ambulancia_chegou_no_hospital", primeiro)
    eventos.emitir_evento("Ambulancia_chegou_no_hospital", segundo)
    eventos.emitir_evento("Ambulancia_chegou_no_hospital", segundo)

    assert segundo.status == StatusDespacho.FINALIZADO.value
    assert frota[1].status == "Disponivel"
    assert atendimento.hora_finalizacao is not None
    assert chamada.status == StatusChamada.FINALIZADO.value
    assert finalizados == [atendimento]
    assert [(dados["ID"], dados["status"]) for dados in atualizacoes] == [
        (41, StatusDespacho.FINALIZADO.value),
        (42, StatusDespacho.FINALIZADO.value),
    ]
