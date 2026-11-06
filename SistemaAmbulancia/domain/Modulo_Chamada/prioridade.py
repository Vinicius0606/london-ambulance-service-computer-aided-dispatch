from enum import Enum

class Prioridade(Enum):
    TRANSPORTE = "Transporte"
    MODERADA = "Moderada"
    ALTA = "Alta"
    EXTREMA = "Extrema"

    @property
    def codigo(self) -> int:
        return _CODIGOS_PRIORIDADE[self]


_CODIGOS_PRIORIDADE = {
    Prioridade.TRANSPORTE: 1,
    Prioridade.MODERADA: 2,
    Prioridade.ALTA: 3,
    Prioridade.EXTREMA: 4,
}


def normalizar_prioridade(valor) -> Prioridade | None:
    if isinstance(valor, tuple):
        valor = valor[0] if valor else None
    if isinstance(valor, Prioridade):
        return valor
    if type(valor) is int:
        valor = str(valor)
    if not isinstance(valor, str):
        return None

    valor = valor.strip()
    return next(
        (prioridade for prioridade, codigo in _CODIGOS_PRIORIDADE.items()
         if valor in (prioridade.value, str(codigo))),
        None,
    )
